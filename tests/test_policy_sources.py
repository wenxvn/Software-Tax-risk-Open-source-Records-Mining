from taxrisk.policy_sources import POLICY_CANDIDATES, html_to_text


def test_html_to_text_preserves_policy_content():
    assert html_to_text("<h1>政策</h1><p>正文 &amp; 附件</p>") == "政策\n正文 & 附件\n"


def test_policy_candidates_are_official_and_not_tax_conclusions():
    assert len(POLICY_CANDIDATES) >= 3
    for policy in POLICY_CANDIDATES:
        assert policy["source_url"].startswith("https://")
        assert policy["status"] in {"VERIFIED", "NEEDS_REVIEW"}
        assert "TODO_MISSING_DATA" in policy["notes"] or policy["status"] == "NEEDS_REVIEW"
