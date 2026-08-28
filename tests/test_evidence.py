from morse.evidence import canonical_json, evidence_record, validate_record
from morse.runner import RunConfig, matrix


def test_evidence_record_validates():
    record = evidence_record(
        project="MORSE", run_id="x", topology="clover-3", regime="uniform",
        cycles=2, periods=[1, 1, 1], metrics={"x": 1}, seed=None,
    )
    validate_record(record)
    assert "schema_version" in record


def test_reference_matrix_has_8_conditions():
    records = matrix(RunConfig(cycles=8, anomaly_every=None))
    assert len(records) == 8
    assert len({(r["topology"], r["regime"]) for r in records}) == 8


def test_canonical_json_is_order_stable():
    assert canonical_json({"b": 2, "a": 1}) == canonical_json({"a": 1, "b": 2})
