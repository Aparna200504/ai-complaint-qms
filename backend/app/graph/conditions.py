from app.graph.state import ComplaintState


def route_after_parse(state: ComplaintState) -> str:
    """
    Route after complaint parsing.

    Successful parsing -> validation.
    Parsing failure -> error handler.
    """

    if state.get("error"):
        return "handle_error"

    if state.get("complaint") is None:
        return "handle_error"

    return "validate_complaint"


def route_after_validation(state):
    if state.get("error"):
        return "handle_error"

    validation_result = state.get("validation_result")

    if not validation_result:
        return "handle_error"

    if validation_result.get("valid") is True:
        return "assess_risk"

    return "finish_draft"