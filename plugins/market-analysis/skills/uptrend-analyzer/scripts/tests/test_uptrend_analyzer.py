"""E2E orchestration tests for uptrend_analyzer.main()"""

import json
import os
import tempfile
from unittest import mock

from helpers import make_all_timeseries, make_full_sector_summary

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

WORKSHEET_MAP = {
    "Technology": "sec_technology",
    "Consumer Cyclical": "sec_consumercyclical",
    "Communication Services": "sec_communicationservices",
    "Financial": "sec_financial",
    "Industrials": "sec_industrials",
    "Utilities": "sec_utilities",
    "Consumer Defensive": "sec_consumerdefensive",
    "Healthcare": "sec_healthcare",
    "Real Estate": "sec_realestate",
    "Energy": "sec_energy",
    "Basic Materials": "sec_basicmaterials",
}


def _build_full_timeseries(all_rows, sector_summary):
    """Combine 'all' rows with per-sector rows for the fetcher mock."""
    rows = list(all_rows)
    for sec_row in sector_summary:
        ws = WORKSHEET_MAP.get(sec_row["Sector"], sec_row["Sector"].lower())
        rows.append(
            {
                "worksheet": ws,
                "date": "2026-01-25",
                "count": 100,
                "total": 300,
                "ratio": sec_row["Ratio"],
                "ma_10": sec_row.get("10MA"),
                "slope": sec_row.get("Slope"),
                "trend": (sec_row.get("Trend") or "up").lower(),
            }
        )
    return rows


def _derive_all_timeseries(full_ts):
    """Replicate UptrendDataFetcher.get_all_timeseries()."""
    filtered = [r for r in full_ts if r["worksheet"] == "all"]
    filtered.sort(key=lambda r: r["date"])
    return filtered


def _derive_latest_all(full_ts):
    """Replicate UptrendDataFetcher.get_latest_all()."""
    ts = _derive_all_timeseries(full_ts)
    return ts[-1] if ts else None


def _derive_all_sector_latest(full_ts):
    """Replicate UptrendDataFetcher.get_all_sector_latest()."""
    sectors = {}
    for row in full_ts:
        ws = row["worksheet"]
        if ws == "all":
            continue
        if ws not in sectors or row["date"] > sectors[ws]["date"]:
            sectors[ws] = row
    return sectors


def _make_mock_fetcher(full_ts, sector_summary):
    """Configure a mock UptrendDataFetcher with derived helper methods."""
    instance = mock.MagicMock()
    instance.fetch_timeseries.return_value = full_ts
    instance.fetch_sector_summary.return_value = sector_summary
    instance.get_all_timeseries.return_value = _derive_all_timeseries(full_ts)
    instance.get_latest_all.return_value = _derive_latest_all(full_ts)
    instance.get_all_sector_latest.return_value = _derive_all_sector_latest(full_ts)
    return instance


def _run_main(output_dir, sector_summary=None):
    """Run main() with mocked fetcher, returning output_dir contents."""
    all_rows = make_all_timeseries(n=25, base_ratio=0.28, slope=0.001)
    if sector_summary is None:
        sector_summary = make_full_sector_summary()
    full_ts = _build_full_timeseries(all_rows, sector_summary)
    mock_instance = _make_mock_fetcher(full_ts, sector_summary)

    with mock.patch("data_fetcher.UptrendDataFetcher", return_value=mock_instance):
        with mock.patch("sys.argv", ["uptrend_analyzer.py", "--output-dir", output_dir]):
            import uptrend_analyzer

            uptrend_analyzer.main()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestMainGeneratesReports:
    """Test that main() produces both JSON and Markdown report files."""

    def test_main_generates_reports(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            _run_main(tmpdir)

            files = os.listdir(tmpdir)
            json_files = [f for f in files if f.endswith(".json")]
            md_files = [f for f in files if f.endswith(".md")]

            assert len(json_files) == 1, f"Expected 1 JSON file, got {json_files}"
            assert len(md_files) == 1, f"Expected 1 MD file, got {md_files}"

            # Verify JSON is parseable
            with open(os.path.join(tmpdir, json_files[0])) as f:
                data = json.load(f)
            assert "composite" in data
            assert "components" in data
            assert "metadata" in data

            # Verify MD is non-empty
            with open(os.path.join(tmpdir, md_files[0])) as f:
                content = f.read()
            assert "Uptrend Analyzer Report" in content


class TestMainCompositeScoreInRange:
    """Test that composite_score in JSON output is within 0-100."""

    def test_main_composite_score_in_range(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            _run_main(tmpdir)

            files = os.listdir(tmpdir)
            json_file = [f for f in files if f.endswith(".json")][0]
            with open(os.path.join(tmpdir, json_file)) as f:
                data = json.load(f)

            score = data["composite"]["composite_score"]
            assert 0 <= score <= 100, f"composite_score {score} out of range"


class TestMainWithNoSectorSummary:
    """Test that main() completes gracefully when sector_summary is empty."""

    def test_main_with_no_sector_summary(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            all_rows = make_all_timeseries(n=25, base_ratio=0.28, slope=0.001)
            mock_instance = _make_mock_fetcher(all_rows, [])

            with mock.patch("data_fetcher.UptrendDataFetcher", return_value=mock_instance):
                with mock.patch("sys.argv", ["uptrend_analyzer.py", "--output-dir", tmpdir]):
                    import uptrend_analyzer

                    uptrend_analyzer.main()

            files = os.listdir(tmpdir)
            json_files = [f for f in files if f.endswith(".json")]
            assert len(json_files) == 1

            with open(os.path.join(tmpdir, json_files[0])) as f:
                data = json.load(f)

            score = data["composite"]["composite_score"]
            assert 0 <= score <= 100
