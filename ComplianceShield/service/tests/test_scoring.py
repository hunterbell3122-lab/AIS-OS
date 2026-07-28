import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from checklist.scoring import DomainStatus, load_checklist, score_audit, score_domain


class TestChecklistData(unittest.TestCase):
    def setUp(self):
        self.checklist = load_checklist()

    def test_six_domains(self):
        self.assertEqual(len(self.checklist["domains"]), 6)

    def test_question_count_in_target_range(self):
        total = sum(len(d["questions"]) for d in self.checklist["domains"])
        self.assertGreaterEqual(total, 80)
        self.assertLessEqual(total, 120)

    def test_question_ids_unique(self):
        ids = [q["id"] for d in self.checklist["domains"] for q in d["questions"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_question_has_valid_severity(self):
        valid = {"critical", "high", "medium", "low"}
        for domain in self.checklist["domains"]:
            for question in domain["questions"]:
                self.assertIn(question["severity"], valid)


def all_answers(checklist, value):
    return {
        q["id"]: value
        for domain in checklist["domains"]
        for q in domain["questions"]
    }


class TestDomainScoring(unittest.TestCase):
    def setUp(self):
        self.checklist = load_checklist()
        self.osha = next(d for d in self.checklist["domains"] if d["id"] == "osha")

    def test_all_pass_yields_pass_status(self):
        answers = {q["id"]: True for q in self.osha["questions"]}
        result = score_domain(self.osha, answers)
        self.assertEqual(result.status, DomainStatus.PASS)
        self.assertEqual(result.weighted_fail_score, 0)
        self.assertEqual(result.failed_question_ids, [])

    def test_all_fail_yields_fail_status(self):
        answers = {q["id"]: False for q in self.osha["questions"]}
        result = score_domain(self.osha, answers)
        self.assertEqual(result.status, DomainStatus.FAIL)
        self.assertTrue(result.critical_fail)
        self.assertEqual(len(result.failed_question_ids), len(self.osha["questions"]))

    def test_single_low_severity_fail_yields_at_risk(self):
        answers = {q["id"]: True for q in self.osha["questions"]}
        low_severity_q = next(q for q in self.osha["questions"] if q["severity"] == "low")
        answers[low_severity_q["id"]] = False
        result = score_domain(self.osha, answers)
        self.assertEqual(result.status, DomainStatus.AT_RISK)
        self.assertFalse(result.critical_fail)

    def test_single_critical_fail_forces_fail_status(self):
        answers = {q["id"]: True for q in self.osha["questions"]}
        critical_q = next(q for q in self.osha["questions"] if q["severity"] == "critical")
        answers[critical_q["id"]] = False
        result = score_domain(self.osha, answers)
        self.assertEqual(result.status, DomainStatus.FAIL)
        self.assertTrue(result.critical_fail)

    def test_not_applicable_excluded_from_scoring(self):
        answers = {q["id"]: True for q in self.osha["questions"]}
        na_result = score_domain(self.osha, answers)

        target_q = self.osha["questions"][0]
        answers[target_q["id"]] = None
        excluded_result = score_domain(self.osha, answers)

        self.assertLess(excluded_result.max_possible_score, na_result.max_possible_score)
        self.assertEqual(excluded_result.weighted_fail_score, 0)
        self.assertEqual(excluded_result.status, DomainStatus.PASS)

    def test_missing_answer_raises(self):
        answers = {q["id"]: True for q in self.osha["questions"][:-1]}
        with self.assertRaises(ValueError):
            score_domain(self.osha, answers)


class TestAuditScoring(unittest.TestCase):
    def setUp(self):
        self.checklist = load_checklist()

    def test_all_pass_overall(self):
        answers = all_answers(self.checklist, True)
        result = score_audit(self.checklist, answers)
        self.assertEqual(result.overall_status, DomainStatus.PASS)
        self.assertEqual(result.overall_risk_score, 0.0)
        self.assertTrue(all(r.status == DomainStatus.PASS for r in result.domain_results))

    def test_all_fail_overall(self):
        answers = all_answers(self.checklist, False)
        result = score_audit(self.checklist, answers)
        self.assertEqual(result.overall_status, DomainStatus.FAIL)
        self.assertEqual(result.overall_risk_score, 100.0)
        self.assertTrue(all(r.status == DomainStatus.FAIL for r in result.domain_results))

    def test_mixed_one_domain_failing_drives_overall_fail(self):
        answers = all_answers(self.checklist, True)
        failing_domain = self.checklist["domains"][0]
        for q in failing_domain["questions"]:
            answers[q["id"]] = False

        result = score_audit(self.checklist, answers)
        self.assertEqual(result.overall_status, DomainStatus.FAIL)
        self.assertGreater(result.overall_risk_score, 0.0)
        self.assertLess(result.overall_risk_score, 100.0)

        failing = next(r for r in result.domain_results if r.domain_id == failing_domain["id"])
        self.assertEqual(failing.status, DomainStatus.FAIL)
        other_domains = [r for r in result.domain_results if r.domain_id != failing_domain["id"]]
        self.assertTrue(all(r.status == DomainStatus.PASS for r in other_domains))


if __name__ == "__main__":
    unittest.main()
