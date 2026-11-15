"""Scope: Verify offline report approval, privacy and prefilled-form boundaries."""

import importlib.util
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "prepare_report", ROOT / "aikea-report-issue/scripts/prepare_report.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
ID = "12345678-1234-4234-8234-123456789abc"
CONFIG = {"status": "ready", "prefill_url_template":
          "https://docs.google.com/forms/d/e/example/viewform?usp=pp_url&entry.123=AIKEA_REPORT"}


class TestIssueReport:
    def draft(self):
        return {"title": "Viewer stopped", "summary": "A shelf update was not shown.",
                "expected": "The shelf appears.", "actual": "The previous view remains.",
                "steps": "Add a synthetic shelf and rebuild.", "version": "0.1.0",
                "environment": "ChatGPT on macOS; browser version unknown"}

    def test_approval_controls_any_transmitting_link(self):
        report = MODULE.IssueReport(self.draft(), ID)
        result = report.prepare(CONFIG)
        assert result["status"] == "review_required"
        assert "prefilled_url" not in result and "form_url" not in result
        approved = report.prepare(CONFIG, approved=True)
        assert parse_qs(urlsplit(approved["prefilled_url"]).query)["entry.123"] == [result["report"]]
        assert approved["report_id"] == ID

    def test_disabled_configuration_retains_local_report(self):
        result = MODULE.IssueReport(self.draft(), ID).prepare({"status": "not_configured"}, True)
        assert result["status"] == "not_configured"
        assert "prefilled_url" not in result
        assert "Viewer stopped" in result["report"]

    @pytest.mark.parametrize("url", [
        "https://evil.example/forms/d/e/example/viewform?usp=pp_url&entry.123=AIKEA_REPORT",
        "http://docs.google.com/forms/d/e/example/viewform?usp=pp_url&entry.123=AIKEA_REPORT",
        "https://docs.google.com@evil.example/forms/d/e/example/viewform?usp=pp_url&entry.123=AIKEA_REPORT",
        "https://docs.google.com/forms/d/e/example/viewform?usp=pp_url&entry.123=AIKEA_REPORT&entry.456=yes",
        "https://docs.google.com/forms/d/e/example/formResponse?usp=pp_url&entry.123=AIKEA_REPORT",
        "https://docs.google.com/forms/d/e/example/viewform?usp=pp_url&entry.123=AIKEA_REPORT#fragment",
    ])
    def test_rejects_changed_destinations_and_extra_prefill_fields(self, url):
        with pytest.raises(ValueError, match="verified Google"):
            MODULE.IssueReport(self.draft(), ID).prepare(dict(CONFIG, prefill_url_template=url), True)

    @pytest.mark.parametrize("private", ["person@example.test", "/Users/private/project",
        "C:\\Users\\private\\project", "api_key=" + "pretend-value", "https://example.test/private?q=abc"])
    def test_private_patterns_are_rejected_without_echoing_values(self, private):
        draft = dict(self.draft(), actual=private)
        with pytest.raises(ValueError) as error:
            MODULE.IssueReport(draft, ID)
        assert private not in str(error.value)

    def test_unapproved_extra_fields_and_long_fields_rejected(self):
        for draft in (dict(self.draft(), attachment="raw.log"), dict(self.draft(), title="x" * 121)):
            with pytest.raises(ValueError):
                MODULE.IssueReport(draft, ID)

    def test_unicode_and_query_characters_round_trip(self):
        report = MODULE.IssueReport(dict(self.draft(), summary="Skuffe & hylde? 你好 #1"), ID)
        url = report.prepare(CONFIG, True)["prefilled_url"]
        assert parse_qs(urlsplit(url).query)["entry.123"] == [report.text]

    def test_multiline_title_cannot_change_the_receiver_header(self):
        with pytest.raises(ValueError, match="single line"):
            MODULE.IssueReport(dict(self.draft(), title="Viewer\nSummary:"), ID)

    def test_large_encoded_report_falls_back_to_manual_paste(self):
        draft = {key: "界" * length for key, length in MODULE.IssueReport.fields.items()}
        result = MODULE.IssueReport(draft, ID).prepare(CONFIG, True)
        assert result["status"] == "manual_paste"
        assert "prefilled_url" not in result
        assert result["form_url"].endswith("/viewform")
