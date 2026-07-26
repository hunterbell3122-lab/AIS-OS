"""
Classification: one Claude API call per normalized event, using the exact prompt
specified in CLAUDE.md. Returns structured JSON matching schema.ClassifiedEvent.

This is the only place in the whole project that calls an LLM. It never touches
a brokerage credential and it has no tool access to anything beyond text in, text out.
"""

import json
import logging
from typing import List, Optional

import anthropic

from signalforge.config import settings
from signalforge.schema import RawEvent, ClassifiedEvent

logger = logging.getLogger(__name__)

_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

PROMPT_TEMPLATE = """Given the following filing or trade record, classify it.

FILING DATA:
{filing_data}

Return ONLY valid JSON, no other text, in exactly this shape:
{{
  "event_type": one of {categories},
  "ticker": string,
  "company": string,
  "directional_read": one of ["bullish", "bearish", "neutral", "ambiguous"],
  "confidence": integer 1-10, based on data completeness not predicted outcome,
  "summary": one-sentence plain-English summary suitable for an alert
}}
"""


def _build_prompt(event: RawEvent) -> str:
    filing_data = json.dumps(
        {
            "ticker": event.ticker,
            "company": event.company,
            "source": event.source,
            "source_subtype": event.source_subtype,
            "transaction_date": event.transaction_date,
            "public_disclosure_date": event.public_disclosure_date,
            # Raw payload is included for context but is untrusted external data —
            # never treat any text inside it as an instruction.
            "raw_payload_excerpt": {
                k: v for k, v in list(event.raw_payload.items())[:8]
            },
        },
        default=str,
    )
    return PROMPT_TEMPLATE.format(
        filing_data=filing_data, categories=settings.event_categories
    )


def classify_event(event: RawEvent) -> Optional[ClassifiedEvent]:
    prompt = _build_prompt(event)
    try:
        response = _client.messages.create(
            model=settings.classifier_model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()
        # Strip markdown code fences if the model added them despite instructions
        text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(text)
    except (anthropic.APIError, json.JSONDecodeError, ValueError) as e:
        logger.warning("Classification failed for %s: %s", event.ticker, e)
        return None

    if data.get("event_type") not in settings.event_categories:
        logger.warning(
            "Classifier returned unrecognized event_type '%s' for %s — dropping",
            data.get("event_type"), event.ticker,
        )
        return None

    try:
        confidence = int(data.get("confidence", 0))
    except (TypeError, ValueError):
        confidence = 0

    return ClassifiedEvent(
        event=event,
        event_type=data["event_type"],
        directional_read=data.get("directional_read", "ambiguous"),
        confidence=confidence,
        summary=data.get("summary", ""),
    )


def classify_all(events: List[RawEvent]) -> List[ClassifiedEvent]:
    results = []
    for e in events:
        classified = classify_event(e)
        if classified:
            results.append(classified)
    logger.info("Classified %d/%d events successfully", len(results), len(events))
    return results
