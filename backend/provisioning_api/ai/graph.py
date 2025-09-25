# backend/provisioning_api/ai/graph.py
from __future__ import annotations
from typing import TypedDict, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import re
import dateparser

from langgraph.graph import StateGraph, END
from provisioning_api.db.sql.queries import build_sql

class State(TypedDict, total=False):
    text: str
    filters: Dict[str, Any]
    errors: list[str]
    sql: str

# ----------------- helpers de tiempo -----------------

SPAN = Tuple[datetime, datetime]

def _day_bounds(d: datetime) -> SPAN:
    return d.replace(hour=0, minute=0, second=0, microsecond=0), d.replace(hour=23, minute=59, second=59, microsecond=0)

def _week_bounds(d: datetime) -> SPAN:
    # lunes-domingo
    start = (d - timedelta(days=d.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    end = (start + timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=0)
    return start, end

def _month_bounds(d: datetime) -> SPAN:
    start = d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if d.month == 12:
        nxt = d.replace(year=d.year + 1, month=1, day=1)
    else:
        nxt = d.replace(month=d.month + 1, day=1)
    end = (nxt - timedelta(seconds=1)).replace(microsecond=0)
    return start, end

def _quarter_bounds(d: datetime) -> SPAN:
    q = (d.month - 1) // 3
    first_month = q * 3 + 1
    start = d.replace(month=first_month, day=1, hour=0, minute=0, second=0, microsecond=0)
    # siguiente trimestre
    if first_month == 10:
        nxt = d.replace(year=d.year + 1, month=1, day=1)
    else:
        nxt = d.replace(month=first_month + 3, day=1)
    end = (nxt - timedelta(seconds=1)).replace(microsecond=0)
    return start, end

def _year_bounds(d: datetime) -> SPAN:
    start = d.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end = d.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=0)
    return start, end

def _parse_range_free(text: str, now: Optional[datetime] = None) -> SPAN:
    """
    Soporta en español (sin LLM):
    - “del X al Y”, “desde X hasta Y”, “entre X y Y”
    - “hoy”, “ayer”, “anteayer”
    - “últimos/ultimas N (días|semanas|meses|años|horas)”
    - “hace N (días|semanas|meses|años|horas)”  -> [now-N, now]
    - “esta semana/mes/trimestre/año”
    - “semana/mes/trimestre/año pasado(a)”
    - “este fin de semana”, “fin de semana pasado”
    - “principio/inicio/comienzo de <mes> [de <año>] ... (hasta hoy)”
    - “este mes hasta hoy”, “esta semana hasta hoy” (fin = hoy)
    """
    now = now or datetime.now()
    base_parse = lambda s: dateparser.parse(s, languages=["es"], settings={"PREFER_DATES_FROM": "past"})  # type: ignore

    t = re.sub(r"\s+", " ", text.strip().lower())

    # Rango explícito
    m = re.search(r"\b(?:del|desde)\s+(.+?)\s+(?:al|hasta)\s+(.+?)\b", t)
    if not m:
        m = re.search(r"\bentre\s+(.+?)\s+y\s+(.+?)\b", t)
    if m:
        s = base_parse(m.group(1))
        e = base_parse(m.group(2))
        if s and e:
            s0, e0 = _day_bounds(s) if s.time() == datetime.min.time() else (s, s)
            e0 = e.replace(microsecond=0)
            if e.time() == datetime.min.time():
                _, e0 = _day_bounds(e)
            return s0, e0

    # Hoy / Ayer / Anteayer
    if re.search(r"\bhoy\b", t):
        return _day_bounds(now)
    if re.search(r"\banteayer\b", t):
        return _day_bounds(now - timedelta(days=2))
    if re.search(r"\bayer\b", t) or re.search(r"\bay er\b", t):  # por si meten espacios raros
        return _day_bounds(now - timedelta(days=1))

    # Últimos N unidades
    m = re.search(r"\búltim[oa]s?\s+(\d+)\s+(d[ií]as?|semanas?|meses?|a[nñ]os?|horas?)\b", t)
    if m:
        n = int(m.group(1)); unit = m.group(2)
        delta = {"día": "days", "dias": "days", "días": "days", "semana": "weeks", "semanas": "weeks",
                 "mes": "months", "meses": "months", "año": "years", "años": "years", "hora": "hours", "horas": "hours"}
        u = "days"
        if "seman" in unit: u = "weeks"
        elif "mes" in unit: u = "months"
        elif "a" in unit and "ño" in unit: u = "years"
        elif "hora" in unit: u = "hours"
        end = now
        if u == "weeks": start = now - timedelta(weeks=n)
        elif u == "months":
            # retroceso mes a mes
            y, mth = now.year, now.month
            for _ in range(n):
                if mth == 1: y, mth = y - 1, 12
                else: mth -= 1
            start = now.replace(year=y, month=mth)
        elif u == "years": start = now.replace(year=now.year - n)
        elif u == "hours":
            start = now - timedelta(hours=n)
        else:
            start = now - timedelta(days=n)
        s0 = start.replace(minute=0, second=0, microsecond=0) if u == "hours" else _day_bounds(start)[0]
        e0 = end.replace(microsecond=0)
        return s0, e0

    # Hace N unidades (desde hace N hasta ahora)
    m = re.search(r"\bhace\s+(\d+)\s+(d[ií]as?|semanas?|meses?|a[nñ]os?|horas?)\b", t)
    if m:
        n = int(m.group(1)); unit = m.group(2)
        if "seman" in unit: start = now - timedelta(weeks=n)
        elif "mes" in unit:
            y, mth = now.year, now.month
            for _ in range(n):
                if mth == 1: y, mth = y - 1, 12
                else: mth -= 1
            start = now.replace(year=y, month=mth)
        elif "a" in unit and "ño" in unit: start = now.replace(year=now.year - n)
        elif "hora" in unit: start = now - timedelta(hours=n)
        else: start = now - timedelta(days=n)
        s0 = start.replace(minute=0, second=0, microsecond=0) if "hora" in unit else _day_bounds(start)[0]
        return s0, now.replace(microsecond=0)

    # Esta/este … / pasada(o)
    if re.search(r"\best[ae]\s+semana\b", t):
        s, e = _week_bounds(now)
        e = min(e, now.replace(hour=23, minute=59, second=59, microsecond=0))
        return s, e
    if re.search(r"\bsemana\s+pasad[ao]\b", t):
        s, _ = _week_bounds(now - timedelta(days=7))
        return s, (s + timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=0)

    if re.search(r"\best[ea]\s+mes\b", t):
        s, e = _month_bounds(now)
        e = min(e, now.replace(hour=23, minute=59, second=59, microsecond=0))
        return s, e
    if re.search(r"\bmes\s+pasad[oa]\b", t):
        prev = now.replace(day=1) - timedelta(days=1)
        s, e = _month_bounds(prev)
        return s, e

    if re.search(r"\best[ea]\s+trimestre\b", t):
        s, e = _quarter_bounds(now); e = min(e, now.replace(hour=23, minute=59, second=59, microsecond=0)); return s, e
    if re.search(r"\btrimestre\s+pasad[oa]\b", t):
        s, _ = _quarter_bounds(now.replace(month=((now.month - 4) % 12) + 1))
        e = _quarter_bounds(s)[1]; return s, e

    if re.search(r"\best[ea]\s+a[nñ]o\b", t):
        s, e = _year_bounds(now); e = min(e, now.replace(hour=23, minute=59, second=59, microsecond=0)); return s, e
    if re.search(r"\ba[nñ]o\s+pasad[oa]\b", t):
        s, e = _year_bounds(now.replace(year=now.year - 1)); return s, e

    # Fin de semana
    if re.search(r"\bfin\s+de\s+semana\s+pasad[oa]?\b", t):
        # sábado y domingo pasados
        last_sun = now - timedelta(days=(now.weekday() + 1))
        sat = last_sun - timedelta(days=1)
        return _day_bounds(sat)[0], _day_bounds(last_sun)[1]
    if re.search(r"\beste\s+fin\s+de\s+semana\b", t):
        # siguiente fin de semana del período actual
        wstart, _ = _week_bounds(now)
        sat = wstart + timedelta(days=5)
        sun = sat + timedelta(days=1)
        return _day_bounds(sat)[0], _day_bounds(sun)[1]

    # Principio/inicio/comienzo de <mes> [de <año>] (hasta hoy si no hay fin)
    m = re.search(r"(?:principio|inicio|comienzo)\s+de\s+([a-záéíóú]+)(?:\s+de\s+(\d{4}))?", t)
    if m:
        month = m.group(1); year = int(m.group(2)) if m.group(2) else now.year
        s = dateparser.parse(f"1 {month} {year}", languages=["es"])
        if s:
            _, e = _day_bounds(now)
            return _day_bounds(s)[0], e

    # Fallback: hoy
    return _day_bounds(now)

# ----------------- NODOS -----------------

def parse_text(state: State) -> State:
    txt = str(state.get("text",""))
    filters: Dict[str, Any] = {}

    # pri_ne_id: acepta “pri_ne_id DTH”, “pri_ne_id=DTH”, “para/en/sobre el DTH”, “ne id DTH”
    m = re.search(r"\bpri[_\s-]?ne[_\s-]?id\b(?:\s*(?:=|:)\s*|\s+(?:es|de)?\s*)?([a-z0-9_-]{2,})\b", txt, flags=re.I)
    if not m:
        m = re.search(r"\b(?:en|para|sobre)\s+(?:el|la|los|las)?\s*([a-z0-9_-]{2,})\b", txt, flags=re.I)
    if not m:
        m = re.search(r"\bne\s*id\b\s*[:=]?\s*([a-z0-9_-]{2,})\b", txt, flags=re.I)
    if m:
        filters["pri_ne_id"] = m.group(1).upper()

    m = re.search(r"\bpri_id\s*[:=]\s*(\d+)\b", txt, flags=re.I)
    if m: filters["pri_id"] = int(m.group(1))

    m = re.search(r"\bpri_action\s*[:=]\s*([a-z0-9_-]+)\b", txt, flags=re.I)
    if not m:
        m = re.search(r"\b(?:action|acciones?)\s+([a-z0-9_-]+)\b", txt, flags=re.I)
    if m: filters["pri_action"] = m.group(1).upper()

    start, end = _parse_range_free(txt)
    filters["start_date"] = start.strftime("%Y-%m-%d %H:%M:%S")
    filters["end_date"]   = end.strftime("%Y-%m-%d %H:%M:%S")
    filters.setdefault("limit", 200)
    filters.setdefault("offset", 0)

    state["filters"] = filters
    state["errors"] = [] if filters.get("pri_ne_id") else ["Falta pri_ne_id"]
    return state

def validate(state: State) -> State:
    # validación mínima de formato, ya vienen normalizadas
    errs = []
    f = state["filters"]
    if not f.get("pri_ne_id"): errs.append("Falta pri_ne_id")
    state["errors"] = errs
    return state

def prepare_sql(state: State) -> State:
    if state.get("errors"): return state
    f = state["filters"]
    sql, _, _ = build_sql(f, include_pagination=True)
    state["sql"] = sql
    return state

graph = StateGraph(State)
graph.add_node("parse_text", parse_text)
graph.add_node("validate", validate)
graph.add_node("prepare_sql", prepare_sql)
graph.set_entry_point("parse_text")
graph.add_edge("parse_text", "validate")
graph.add_edge("validate", "prepare_sql")
graph.add_edge("prepare_sql", END)

app_graph = graph.compile()

def run_pipeline(text: str) -> dict:
    out = app_graph.invoke({"text": text})
    return {"filters": out.get("filters", {}), "sql": out.get("sql",""), "errors": out.get("errors", [])}
