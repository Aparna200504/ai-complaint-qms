from langgraph.graph import StateGraph, START, END

from app.graph.state import ComplaintState

from app.graph.nodes import (
    extract_text_node,
    extract_text_input_node,
    parse_complaint_node,
    validate_complaint_node,
    assess_risk_node,
    handle_error_node,
    finish_draft_node,
)

from app.graph.conditions import (
    route_after_parse,
    route_after_validation,
)


def route_input(state: ComplaintState) -> str:
    """
    Decide how the complaint entered the system.

    If complaint_text is provided:
        Use the direct text-input path.

    If file_path is provided:
        Use the document extraction path.

    Otherwise:
        Send the workflow to the error handler.
    """

    complaint_text = state.get("complaint_text")
    file_path = state.get("file_path")

    if complaint_text and complaint_text.strip():
        return "extract_text_input"

    if file_path:
        return "extract_text"

    return "handle_error"


def build_complaint_graph():
    graph = StateGraph(ComplaintState)

    # ---------------------------------------------------------
    # Register nodes
    # ---------------------------------------------------------

    graph.add_node(
        "extract_text",
        extract_text_node,
    )

    graph.add_node(
        "extract_text_input",
        extract_text_input_node,
    )

    graph.add_node(
        "parse_complaint",
        parse_complaint_node,
    )

    graph.add_node(
        "validate_complaint",
        validate_complaint_node,
    )

    graph.add_node(
        "assess_risk",
        assess_risk_node,
    )

    graph.add_node(
        "handle_error",
        handle_error_node,
    )

    graph.add_node("finish_draft", finish_draft_node)

    # ---------------------------------------------------------
    # START -> File extraction OR direct text input
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        START,
        route_input,
        {
            "extract_text": "extract_text",
            "extract_text_input": "extract_text_input",
            "handle_error": "handle_error",
        },
    )

    # ---------------------------------------------------------
    # File extraction -> Parsing
    # ---------------------------------------------------------

    graph.add_edge(
        "extract_text",
        "parse_complaint",
    )

    # ---------------------------------------------------------
    # Direct text input -> Parsing
    # ---------------------------------------------------------

    graph.add_edge(
        "extract_text_input",
        "parse_complaint",
    )

    # ---------------------------------------------------------
    # Parsing -> Validation OR Error
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "parse_complaint",
        route_after_parse,
        {
            "validate_complaint": "validate_complaint",
            "handle_error": "handle_error",
        },
    )

    # ---------------------------------------------------------
    # Validation -> Risk Assessment OR Error
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "validate_complaint",
        route_after_validation,
        {
            "assess_risk": "assess_risk",
            "finish_draft": "finish_draft",
            "handle_error": "handle_error",
        },
    )

    # ---------------------------------------------------------
    # Successful workflow
    # ---------------------------------------------------------

    graph.add_edge(
        "assess_risk",
        END,
    )

    graph.add_edge("finish_draft", END)

    # ---------------------------------------------------------
    # Error workflow
    # ---------------------------------------------------------

    graph.add_edge(
        "handle_error",
        END,
    )

    return graph.compile()


# Compiled LangGraph workflow
complaint_graph = build_complaint_graph()