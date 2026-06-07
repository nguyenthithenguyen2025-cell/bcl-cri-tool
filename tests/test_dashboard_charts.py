# -*- coding: utf-8 -*-
"""Kiểm thử các biểu đồ dashboard so sánh."""

import unittest

from utils.charts import (
    priority_top_chart,
    province_distribution_chart,
    risk_distribution_chart,
)


class DashboardChartTest(unittest.TestCase):
    def _summary(self) -> list[dict]:
        return [
            {
                "ten_bcl": "BCL A",
                "tinh": "Hà Nội",
                "dien_tich_ha": 2.0,
                "CRI": 0.70,
                "risk_level": 4,
            },
            {
                "ten_bcl": "BCL B",
                "tinh": "Hà Nội",
                "dien_tich_ha": 1.5,
                "CRI": 0.60,
                "risk_level": 3,
            },
            {
                "ten_bcl": "BCL C",
                "tinh": "Bắc Ninh",
                "dien_tich_ha": 0.8,
                "CRI": 0.40,
                "risk_level": 2,
            },
        ]

    def test_risk_distribution_chart(self):
        fig = risk_distribution_chart(self._summary())
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.data), 1)

    def test_province_distribution_chart(self):
        fig = province_distribution_chart(self._summary())
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.data), 1)

    def test_priority_top_chart(self):
        fig = priority_top_chart(self._summary(), n=2)
        self.assertIsNotNone(fig)
        self.assertEqual(len(fig.data), 1)


if __name__ == "__main__":
    unittest.main()
