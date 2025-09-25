"""LangGraph pipeline to interpret natural language queries."""
from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Dict

from dateparser.search import search_dates
from langgraph.graph import END, StateGraph

from provisioning_api.db.sql.queries import build_sql

State = Dict[str, Any]


def _normalise_datetime(value: datetime) -> str:
    return value.replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")


def parse_text(state: State) -> State:
    text: str = state.get("text", "")
    filters = dict(state.get("filters", {}))
    errors = list(state.get("errors", []))

    date_matches = search_dates(text, languages=["es"]) or []
    if date_matches:
        dates = sorted({match[1] for match in date_matches})
        start = dates[0]
        end = dates[-1]
        filters["start_date"] = _normalise_datetime(start)
        filters["end_date"] = _normalise_datetime(end)

    ne_match = re.search(r"\b([A-Z]{3}\d+)\b", text.upper())
    if ne_match:
        filters["pri_ne_id"] = ne_match.group(1)

    pri_id_match = re.search(r"pri[_\s-]*id\s*(\d+)", text.lower())
    if pri_id_match:
        filters["pri_id"] = int(pri_id_match.group(1))

    action_match = re.search(
        r"\b(alta|baja|modificacion|modificación|consulta|update|delete)\b",
        text.lower(),
    )
    if action_match:
        filters["pri_action"] = action_match.group(1).upper()

    filters.setdefault("limit", 200)
    filters.setdefault("offset", 0)

    return {**state, "filters": filters, "errors": errors}


def validate(state: State) -> State:
    filters = state.get("filters", {})
    errors = list(state.get("errors", []))

    required = ["start_date", "end_date", "pri_ne_id"]
    for field in required:
        if not filters.get(field):
            errors.append(f"Falta {field}")

    if "start_date" in filters and "end_date" in filters:
        try:
            start = datetime.strptime(filters["start_date"], "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(filters["end_date"], "%Y-%m-%d %H:%M:%S")
            if start > end:
                errors.append("start_date no puede ser mayor que end_date")
        except ValueError:
            errors.append("Formato de fecha inválido")

    return {**state, "errors": errors}


def prepare_sql(state: State) -> State:
    errors = state.get("errors", [])
    filters = state.get("filters", {})

    if errors:
        return {**state, "sql": None}

    base_filters: Dict[str, Any] = {
        "start_date": filters["start_date"],
        "end_date": filters["end_date"],
        "pri_ne_id": filters["pri_ne_id"],
        "limit": filters.get("limit", 200),
        "offset": filters.get("offset", 0),
    }
    if filters.get("pri_id") is not None:
        base_filters["pri_id"] = filters["pri_id"]
    if filters.get("pri_action"):
        base_filters["pri_action"] = filters["pri_action"].upper()

    select_sql, _, _, _ = build_sql(base_filters, include_pagination=False)
    return {**state, "filters": base_filters, "sql": select_sql}


graph = StateGraph(dict)
graph.add_node("parse_text", parse_text)
graph.add_node("validate", validate)
graph.add_node("prepare_sql", prepare_sql)

graph.set_entry_point("parse_text")
graph.add_edge("parse_text", "validate")
graph.add_edge("validate", "prepare_sql")
graph.add_edge("prepare_sql", END)

workflow = graph.compile()


def run_pipeline(text: str) -> Dict[str, Any]:
    """Run the natural language pipeline and return filters and SQL."""

    initial_state: State = {"text": text, "filters": {}, "errors": [], "sql": None}
    result = workflow.invoke(initial_state)
    return {
        "filters": result.get("filters", {}),
        "sql": result.get("sql"),
        "errors": result.get("errors", []),
    }
