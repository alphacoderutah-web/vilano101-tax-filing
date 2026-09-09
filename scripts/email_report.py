"""Email a generated report to the configured recipient.

Reads SMTP settings from the revenue project's .env via its lib.creds. No credentials
are stored in this repository, and none may be added -- this repo is public.

    SMTP_HOST · SMTP_PORT · SMTP_USERNAME · SMTP_PASSWORD · REPORT_RECIPIENT

Sends the markdown as both plain text and rendered HTML, and attaches the .md file.

Usage:
  python scripts/email_report.py worksheets/stessa/2026-08-stessa-entry.md
  python scripts/email_report.py <path> --subject "..." --to someone@example.com
"""
import argparse
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

# The revenue project holds the credential loader and the markdown renderer.
REVENUE_PROJECT = Path(os.environ.get("VILANO_REVENUE_PROJECT",
                                      r"D:\Vilano 101\FreeWyld\freewyld"))
if not REVENUE_PROJECT.exists():
    sys.exit(f"Revenue project not found at {REVENUE_PROJECT}. Set VILANO_REVENUE_PROJECT.")
sys.path.insert(0, str(REVENUE_PROJECT))

from lib import creds                       # noqa: E402
from scripts.send_report import md_to_html  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report", help="path to the .md report")
    ap.add_argument("--subject")
    ap.add_argument("--to", help="override REPORT_RECIPIENT")
    a = ap.parse_args()

    path = Path(a.report)
    if not path.exists():
        sys.exit(f"no report at {path}")
    body = path.read_text(encoding="utf-8")

    cfg = creds.smtp()
    host, port = cfg["host"], cfg["port"]
    user, pwd = cfg["username"], cfg["password"]
    to = a.to or cfg["recipient"]

    if not to:
        sys.exit("No recipient. Set REPORT_RECIPIENT in .env or pass --to.")
    if not (host and user and pwd):
        sys.exit("SMTP not configured in .env (SMTP_HOST / SMTP_USERNAME / SMTP_PASSWORD).")

    subject = a.subject or f"VILANO101 — {path.stem.replace('-', ' ')}"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to
    msg.set_content(body)
    msg.add_alternative(md_to_html(body), subtype="html")
    msg.add_attachment(body.encode("utf-8"), maintype="text", subtype="markdown",
                       filename=path.name)

    with smtplib.SMTP(host, int(port or 587), timeout=45) as s:
        s.starttls()
        s.login(user, pwd)
        s.send_message(msg)

    masked = to[:2] + "***@" + to.split("@")[-1] if "@" in to else "***"
    print(f"sent '{subject}' to {masked} ({len(body):,} chars, 1 attachment)")


if __name__ == "__main__":
    main()
