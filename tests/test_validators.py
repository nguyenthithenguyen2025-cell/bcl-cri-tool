# -*- coding: utf-8 -*-
"""Kiểm thử validator dữ liệu đầu vào."""

import unittest

from utils.validators import (
    get_bcl_info_warnings,
    validate_bcl_info,
    validate_missing_notes,
)


class BclInfoValidatorTest(unittest.TestCase):
    def _valid_info(self) -> dict:
        return {
            "ten_bcl": "BCL kiểm thử",
            "tinh": "Hà Nội",
            "loai_bcl": "KHVS",
            "dien_tich_ha": 2.5,
            "toa_do_lat": 21.0,
            "toa_do_lon": 105.8,
            "nam_bat_dau": 2000,
            "nam_ngung": 2020,
        }

    def test_valid_bcl_info_has_no_errors(self):
        self.assertEqual(validate_bcl_info(self._valid_info()), [])

    def test_stop_year_cannot_be_before_start_year(self):
        info = self._valid_info()
        info["nam_ngung"] = 1999

        errors = validate_bcl_info(info)

        self.assertTrue(any("Năm ngừng tiếp nhận" in err for err in errors))

    def test_coordinate_pair_is_required(self):
        info = self._valid_info()
        info["toa_do_lon"] = None

        errors = validate_bcl_info(info)

        self.assertTrue(any("cả vĩ độ và kinh độ" in err for err in errors))

    def test_unusual_physical_values_generate_warnings(self):
        info = self._valid_info()
        info["dien_tich_ha"] = 150
        info["chieu_cao_m"] = 60
        info["the_tich_m3"] = 11_000_000

        warnings = get_bcl_info_warnings(info)

        self.assertGreaterEqual(len(warnings), 3)

    def test_missing_notes_are_required(self):
        errors = validate_missing_notes(["H1", "P3"], {"H1": "Chưa có hồ sơ quan trắc"})

        self.assertEqual(len(errors), 1)
        self.assertIn("P3", errors[0])


if __name__ == "__main__":
    unittest.main()
