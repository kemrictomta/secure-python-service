from typing import Any

from app.domain import Issue, Report


def validate_model(payload: Any) -> Report:
    """
    Validate a JSON payload and return a Report.
    Validation logic will be added step by step.
    """
    if not isinstance(payload, dict):
        return Report(
            ok=False,
            issues=[
                Issue(
                    path="$",
                    message="Payload must be a JSON object",
                    severity="error",
                )
            ],
        )

    # add a list to collect issues
    issues: list[Issue] = []  
     
    # loop over required fields
    required_fields = ["name", "version", "nodes", "edges"]
    for field in required_fields:
        if field not in payload:
            issues.append(
                Issue(
                    path=f"$.{field}",
                    message=f"Missing required field: {field}",
                    severity="error",
                )
            )
    if issues:
        return Report(ok=False, issues=issues)
    return Report(ok=True, issues=[])
