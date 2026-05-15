import json
from html import escape
from typing import Any

from app.pkg.domain import Type

_META_KEYS = frozenset({
    "Type", "type", "To", "to", "Subject", "subject",
    "user_email", "userEmail", "From", "from",
})

_WRAPPER_KEYS = frozenset({
    "Body", "body", "Message", "message",
    "reservation", "data", "payload",
})

_MAX_JSON_DEPTH = 4

_FIELD_LABELS: dict[str, str] = {
    "book_id": "Libro",
    "user_id": "Utente",
    "user_email": "Email",
    "reservation_id": "Prenotazione",
    "reserved_at": "Prenotato il",
    "due_date": "Scadenza",
    "returned_at": "Restituito il",
    "status": "Stato",
}

_TYPE_TITLES: dict[str, str] = {
    Type.RESERVE.value: "Prenotazione confermata",
    Type.RETURN.value: "Libro restituito",
}

_TYPE_SUBJECTS: dict[str, str] = {
    Type.RESERVE.value: "Prenotazione confermata con successo!",
    Type.RETURN.value: "Restituzione registrata con successo!",
}

_DEFAULT_TITLE = "Dettagli notifica"
_DEFAULT_SUBJECT = "Notifica dalla biblioteca"
_FOOTER = "— Servizio email biblioteca"


def _humanize_key(key: str) -> str:
    return _FIELD_LABELS.get(key, key.replace("_", " ").strip().capitalize())


def _parse_json_deep(value: str, depth: int = 0) -> Any | None:
    if depth >= _MAX_JSON_DEPTH:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    if isinstance(parsed, str):
        inner = _parse_json_deep(parsed, depth + 1)
        return inner if inner is not None else parsed
    return parsed


def normalize_body(body: Any) -> dict:
    if body is None:
        return {}
    if isinstance(body, str):
        parsed = _parse_json_deep(body)
        if isinstance(parsed, dict):
            return normalize_body(parsed)
        if isinstance(parsed, list):
            return normalize_body(parsed)
        if isinstance(parsed, str):
            return {"Messaggio": parsed}
        return {"Messaggio": body}
    if isinstance(body, list):
        return {"Elementi": body}
    if not isinstance(body, dict):
        return {"Valore": body}

    for key in _WRAPPER_KEYS:
        nested = body.get(key)
        if nested is not None:
            normalized = normalize_body(nested)
            if normalized:
                extras = {
                    k: v for k, v in body.items()
                    if k not in _WRAPPER_KEYS and k not in _META_KEYS
                }
                return {**extras, **normalized}

    return {
        key: _normalize_field_value(value)
        for key, value in body.items()
    }


def _normalize_field_value(value: Any) -> Any:
    if isinstance(value, str):
        parsed = _parse_json_deep(value)
        if isinstance(parsed, (dict, list)):
            return parsed
    return value


def _display_rows(body: dict) -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    for key, value in body.items():
        if key in _META_KEYS or key in _WRAPPER_KEYS:
            continue
        if isinstance(value, dict) and value:
            rows.extend(_display_rows(value))
        else:
            rows.append((key, value))
    return rows


def _format_value(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "Sì" if value else "No"
    if isinstance(value, str):
        parsed = _parse_json_deep(value)
        if isinstance(parsed, (dict, list)):
            return _format_value(parsed)
        return value
    if isinstance(value, (list, tuple)):
        return ", ".join(_format_value(item) for item in value)
    if isinstance(value, dict):
        return "; ".join(
            f"{_humanize_key(k)}: {_format_value(v)}" for k, v in value.items()
        )
    return str(value)


def extract_body_from_message(msg: dict) -> dict:
    for key in _WRAPPER_KEYS:
        if key in msg:
            return normalize_body(msg[key])
    return normalize_body({
        k: v for k, v in msg.items()
        if k not in _META_KEYS
    })


def _format_plain(email_type: str, body: dict) -> str:
    title = _TYPE_TITLES.get(email_type, _DEFAULT_TITLE)
    lines = [title, "=" * len(title), ""]

    for key, value in _display_rows(body):
        lines.append(f"{_humanize_key(key)}: {_format_value(value)}")

    lines.append("")
    lines.append(_FOOTER)
    return "\n".join(lines)


def _format_html(email_type: str, body: dict) -> str:
    title = escape(_TYPE_TITLES.get(email_type, _DEFAULT_TITLE))
    rows = "".join(
        f"<tr><th style='text-align:left;padding:8px;border-bottom:1px solid #e5e5e5;"
        f"color:#555;width:40%;'>{escape(_humanize_key(key))}</th>"
        f"<td style='padding:8px;border-bottom:1px solid #e5e5e5;'>"
        f"{escape(_format_value(value))}</td></tr>"
        for key, value in _display_rows(body)
    )

    return f"""<!DOCTYPE html>
<html lang="it">
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, Helvetica, sans-serif; color: #1a1a1a; line-height: 1.5;">
  <div style="max-width: 560px; margin: 0 auto; padding: 24px;">
    <h2 style="margin: 0 0 16px; color: #0f4c81;">{title}</h2>
    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
      <tbody>{rows}</tbody>
    </table>
    <p style="margin: 24px 0 0; font-size: 12px; color: #666;">Servizio email biblioteca</p>
  </div>
</body>
</html>"""


def format_email_subject(email_type: str, body: Any = None) -> str:
    data = normalize_body(body)
    template = _TYPE_SUBJECTS.get(email_type, _DEFAULT_SUBJECT)
    try:
        return template.format(**data)
    except KeyError:
        return _DEFAULT_SUBJECT


def format_email_body(email_type: str, body: Any = None) -> tuple[str, str]:
    data = normalize_body(body)
    plain = _format_plain(email_type, data)
    html = _format_html(email_type, data)
    return plain, html
