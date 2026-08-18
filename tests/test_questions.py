"""
Structural tests for the practice question bank.

Runs with pytest (`pytest tests/`) or standalone (`python tests/test_questions.py`).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.questions import QUESTIONS, TOPICS, LEVELS, FORMATS  # noqa: E402


def test_unique_ids():
    ids = [q["id"] for q in QUESTIONS]
    assert len(ids) == len(set(ids))


def test_required_fields():
    for q in QUESTIONS:
        for key in ("id", "topic", "subtopic", "level", "fmt", "prompt", "worked", "source"):
            assert key in q and q[key] != "", f"{q.get('id')} missing {key}"
        assert q["topic"] in TOPICS, q["id"]
        assert q["level"] in LEVELS, q["id"]
        assert q["fmt"] in FORMATS, q["id"]


def test_numeric_shape():
    for q in QUESTIONS:
        if q["fmt"] == "numeric":
            for key in ("answer", "unit", "tol", "answer_label"):
                assert key in q, f"{q['id']} numeric missing {key}"
            assert q["tol"] > 0, q["id"]


def test_mcq_shape():
    for q in QUESTIONS:
        if q["fmt"] == "mcq":
            assert len(q["choices"]) >= 2, q["id"]
            assert 0 <= q["correct"] < len(q["choices"]), q["id"]


def test_reasonable_coverage():
    # a sanity floor so an accidental deletion is caught
    assert len(QUESTIONS) >= 40
    for t in TOPICS:
        assert sum(1 for q in QUESTIONS if q["topic"] == t) >= 5, f"thin topic: {t}"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
