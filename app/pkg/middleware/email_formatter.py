from html import escape
from typing import Any

from app.pkg.domain import Type

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
    Type.RESERVE.value: "Prenotazione confermata per il libro {book_id}",
    Type.RETURN.value: "Restituzione registrata per il libro {book_id}",
}

_DEFAULT_TITLE = "Dettagli notifica"
_DEFAULT_SUBJECT = "Notifica dalla biblioteca"
_FOOTER = "— Servizio email biblioteca"


def _humanize_key(key: str) -> str:
    return _FIELD_LABELS.get(key, key.replace("_", " ").strip().capitalize())


def _format_value(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "Sì" if value else "No"
    if isinstance(value, (list, tuple)):
        return ", ".join(_format_value(item) for item in value)
    if isinstance(value, dict):
        return "; ".join(f"{_humanize_key(k)}: {_format_value(v)}" for k, v in value.items())
    return str(value)


def _format_plain(email_type: str, body: dict) -> str:
    title = _TYPE_TITLES.get(email_type, _DEFAULT_TITLE)
    lines = [title, "=" * len(title), ""]

    for key, value in body.items():
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
        for key, value in body.items()
    )

    wrapper_open = '<' + 'div' + ' style="max-width: 560px; margin: 0 auto; padding: 24px;">'
    wrapper_close = '</' + 'div' + '>'

    return f"""<!DOCTYPE html>
<html lang="it">
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, Helvetica, sans-serif; color: #1a1a1a; line-height: 1.5;">
  {wrapper_open}
    <h2 style="margin: 0 0 16px; color: #0f4c81;">{title}</h2>
    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
      <tbody>{rows}</tbody>
    </table>
    <p style="margin: 24px 0 0; font-size: 12px; color: #666;">Servizio email biblioteca</p>
  {wrapper_close}
</body>
</html>"""


def format_email_subject(email_type: str, body: dict | None) -> str:
    data = body or {}
    template = _TYPE_SUBJECTS.get(email_type, _DEFAULT_SUBJECT)
    try:
        return template.format(**data)
    except KeyError:
        return _DEFAULT_SUBJECT


def format_email_body(email_type: str, body: dict | None) -> tuple[str, str]:
    data = body or {}
    plain = _format_plain(email_type, data)
    html = _format_html(email_type, data)
    return plain, html
