from app.validator import validate_model

def test_invalid_payload_type():
    report = validate_model("this is a string, not a dict")
    assert report.ok is False
    assert len(report.issues) == 1
    assert report.issues[0].path == "$"
    assert report.issues[0].message == "Payload must be a JSON object"
    assert report.issues[0].severity == "error"

def test_missing_required_fields():
    report = validate_model({})
    assert report.ok is False
    assert len(report.issues) == 4

    paths = {i.path for i in report.issues}
    assert paths == {"$.name", "$.version", "$.nodes", "$.edges"} 

def test_accepts_minimal_valid_payload():
    payload = {
        "name": "Test Model",
        "version": "1.0",
        "nodes": [],
        "edges": [],
    }
    report = validate_model(payload)
    assert report.ok is True
    assert report.issues == []  