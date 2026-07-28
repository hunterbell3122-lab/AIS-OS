from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

CHECKLIST_PATH = Path(__file__).parent / "checklist.json"

# Answer values: True = compliant, False = fails the item, None = not applicable
# (excluded from scoring — e.g. an HVHZ question for a contractor outside Miami-Dade/Broward).
Answer = bool | None


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


SEVERITY_WEIGHT = {
    Severity.CRITICAL: 5,
    Severity.HIGH: 3,
    Severity.MEDIUM: 2,
    Severity.LOW: 1,
}

# A domain fails outright if any critical item fails, or if realized weighted
# risk exceeds this share of the domain's total possible weight.
FAIL_THRESHOLD = 0.34


class DomainStatus(Enum):
    PASS = "pass"
    AT_RISK = "at_risk"
    FAIL = "fail"


@dataclass
class DomainResult:
    domain_id: str
    domain_name: str
    status: DomainStatus
    weighted_fail_score: int
    max_possible_score: int
    failed_question_ids: list[str] = field(default_factory=list)
    critical_fail: bool = False


@dataclass
class AuditResult:
    domain_results: list[DomainResult]
    overall_risk_score: float
    overall_status: DomainStatus


def load_checklist(path: Path = CHECKLIST_PATH) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def score_domain(domain: dict, answers: dict[str, Answer]) -> DomainResult:
    max_possible = 0
    fail_score = 0
    failed_ids: list[str] = []
    critical_fail = False

    for question in domain["questions"]:
        qid = question["id"]
        if qid not in answers:
            raise ValueError(f"Missing answer for question {qid}")

        answer = answers[qid]
        if answer is None:
            continue

        weight = SEVERITY_WEIGHT[Severity(question["severity"])]
        max_possible += weight

        if answer is False:
            fail_score += weight
            failed_ids.append(qid)
            if question["severity"] == Severity.CRITICAL.value:
                critical_fail = True

    if fail_score == 0:
        status = DomainStatus.PASS
    elif critical_fail or (max_possible and fail_score / max_possible > FAIL_THRESHOLD):
        status = DomainStatus.FAIL
    else:
        status = DomainStatus.AT_RISK

    return DomainResult(
        domain_id=domain["id"],
        domain_name=domain["name"],
        status=status,
        weighted_fail_score=fail_score,
        max_possible_score=max_possible,
        failed_question_ids=failed_ids,
        critical_fail=critical_fail,
    )


def score_audit(checklist: dict, answers: dict[str, Answer]) -> AuditResult:
    domain_results = [score_domain(domain, answers) for domain in checklist["domains"]]

    total_fail = sum(r.weighted_fail_score for r in domain_results)
    total_max = sum(r.max_possible_score for r in domain_results)
    overall_risk_score = round((total_fail / total_max) * 100, 1) if total_max else 0.0

    if any(r.status == DomainStatus.FAIL for r in domain_results):
        overall_status = DomainStatus.FAIL
    elif any(r.status == DomainStatus.AT_RISK for r in domain_results):
        overall_status = DomainStatus.AT_RISK
    else:
        overall_status = DomainStatus.PASS

    return AuditResult(
        domain_results=domain_results,
        overall_risk_score=overall_risk_score,
        overall_status=overall_status,
    )
