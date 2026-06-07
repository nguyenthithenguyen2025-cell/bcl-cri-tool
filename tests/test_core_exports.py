# -*- coding: utf-8 -*-
"""Kiểm thử hồi quy cho logic CRI và các bộ xuất báo cáo."""

import json
import unittest
from pathlib import Path

from core.calculator import calculate_cri
from core.classifier import classify_and_recommend, generate_technical_analysis
from export.excel_export import export_to_excel
from export.html_export import export_to_html
from export.word_export import export_to_word


ROOT = Path(__file__).resolve().parents[1]


def _sample_entry() -> dict:
    data = json.loads((ROOT / "data" / "sample_data.json").read_text(encoding="utf-8"))
    result = calculate_cri(data["scores"])
    result.update(classify_and_recommend(result["CRI"], data["info"]["loai_bcl"]))
    return {
        "info": data["info"],
        "scores": data["scores"],
        "missing_notes": data.get("missing_notes", {}),
        "result": result,
    }


class CoreCriTest(unittest.TestCase):
    def test_sample_pl24_classification(self):
        entry = _sample_entry()
        result = entry["result"]

        self.assertAlmostEqual(result["H"], 0.6250, places=4)
        self.assertAlmostEqual(result["P"], 0.6658, places=4)
        self.assertAlmostEqual(result["R"], 0.7000, places=4)
        self.assertAlmostEqual(result["CRI"], 0.6647, places=4)
        self.assertEqual(result["risk"]["level"], 3)
        self.assertEqual(result["solution"]["short_name"], "GP 2.2")

    def test_missing_scores_are_assumed_max(self):
        result = calculate_cri({"H1": 0.25})

        self.assertEqual(len(result["missing_params"]), 13)
        self.assertEqual(len(result["assumed_max"]), 13)
        self.assertIn("H2", result["assumed_max"])
        self.assertTrue(0.25 <= result["CRI"] <= 1.00)

    def test_hvs_classification_has_no_cri(self):
        result = classify_and_recommend(None, bcl_type="HVS", hvs_status="DAT_CHUAN")

        self.assertIsNone(result["risk"]["cri"])
        self.assertEqual(result["classification_key"], "HVS_DAT_CHUAN")
        self.assertEqual(result["solution"]["short_name"], "GP 2.1")

    def test_technical_analysis_for_sample(self):
        entry = _sample_entry()

        analysis = generate_technical_analysis(entry)

        self.assertIn("CRI = 0.6647", analysis["summary"])
        self.assertEqual(len(analysis["group_comments"]), 3)
        self.assertGreaterEqual(len(analysis["top_risks"]), 3)
        self.assertTrue(analysis["dominant_group"])
        self.assertTrue(analysis["recommended_actions"])


class ExportTest(unittest.TestCase):
    def test_exports_return_non_empty_files(self):
        entry = _sample_entry()

        xlsx = export_to_excel([entry]).getvalue()
        html = export_to_html(entry)
        docx = export_to_word(entry).getvalue()

        self.assertGreater(len(xlsx), 5000)
        self.assertGreater(len(html), 5000)
        self.assertGreater(len(docx), 10000)
        self.assertTrue(xlsx.startswith(b"PK"))
        self.assertTrue(html.startswith(b"<!DOCTYPE html>"))
        self.assertIn("BÁO CÁO".encode("utf-8"), html)
        self.assertTrue(docx.startswith(b"PK"))


if __name__ == "__main__":
    unittest.main()
