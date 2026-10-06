"""Scope: Prepare an approved public report and Google Form link without networking."""

import argparse
import json
from pathlib import Path
import re
from urllib.parse import quote, parse_qs, urlsplit
import uuid


class IssueReport:
    fields = {"title": 120, "summary": 700, "expected": 500, "actual": 500,
              "steps": 900, "version": 100, "environment": 200}
    private_patterns = (
        r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
        r"(?:/Users/|/home/|[A-Za-z]:\\Users\\)",
        r"(?:gh[pousr]_|github_pat_|sk-|AKIA)[A-Za-z0-9_/-]{8,}",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"(?i)(?:authorization|password|api[_ -]?key|token|secret)\s*[:=]\s*\S+",
        r"https?://\S+",
    )

    def __init__(self, draft, report_id):
        self.report_id = str(uuid.UUID(report_id))
        if set(draft) != set(self.fields):
            raise ValueError("Use only the seven documented report fields")
        for field, limit in self.fields.items():
            value = draft[field]
            if not isinstance(value, str) or not 1 <= len(value.strip()) <= limit:
                raise ValueError(f"Invalid length or type in {field}")
            if field == "title" and len(value.splitlines()) != 1:
                raise ValueError("Use a single line for title")
            if any(re.search(pattern, value) for pattern in self.private_patterns):
                raise ValueError(f"Remove potentially private information from {field}")
        self.text = "\n\n".join([f"Report ID: {self.report_id}"] + [
            f"{field.title()}:\n{draft[field].strip()}" for field in self.fields])

    def prepare(self, config, approved=False):
        result = {"report_id": self.report_id, "report": self.text,
                  "status": "review_required"}
        if not approved:
            return result
        if config.get("status") == "not_configured":
            return dict(result, status="not_configured")
        template = config.get("prefill_url_template", "")
        if config.get("status") != "ready" or not isinstance(template, str):
            raise ValueError("Invalid publisher reporting configuration")
        url = urlsplit(template)
        fields = parse_qs(url.query)
        entries = [key for key, values in fields.items()
                   if re.fullmatch(r"entry\.\d+", key) and values == ["AIKEA_REPORT"]]
        valid = (url.scheme == "https" and url.netloc == "docs.google.com"
                 and re.fullmatch(r"/forms/d/e/[A-Za-z0-9_-]+/viewform", url.path)
                 and not url.fragment and len(entries) == 1
                 and template.count("AIKEA_REPORT") == 1
                 and set(fields) == {"usp", entries[0]}
                 and fields["usp"] == ["pp_url"])
        if not valid:
            raise ValueError("Use the verified Google Forms prefill template")
        prefilled = template.replace("AIKEA_REPORT", quote(self.text, safe=""))
        result.update(status="ready", form_url=f"https://docs.google.com{url.path}")
        if len(prefilled) <= 8000:
            result["prefilled_url"] = prefilled
        else:
            result["status"] = "manual_paste"
        return result


class ReportCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("draft", type=Path)
        parser.add_argument("--report-id")
        parser.add_argument("--approved", action="store_true")
        args = parser.parse_args()
        if args.approved and not args.report_id:
            parser.error("Approved reports must reuse the reviewed report ID")
        report = IssueReport(json.loads(args.draft.read_text()), args.report_id or str(uuid.uuid4()))
        config = Path(__file__).resolve().parents[1] / "assets/reporting.json"
        print(json.dumps(report.prepare(json.loads(config.read_text()), args.approved), indent=2))


if __name__ == "__main__":
    ReportCommand().run()
