from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, ValidationError


ROOT = Path(__file__).resolve().parents[2]


class PublicSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.course_schema = json.loads(
            (ROOT / "schemas/course-profile.schema.json").read_text(encoding="utf-8")
        )
        cls.ir_schema = json.loads(
            (ROOT / "schemas/lecture-ir.schema.json").read_text(encoding="utf-8")
        )
        cls.profile = yaml.safe_load(
            (ROOT / "profiles/example-course.yaml").read_text(encoding="utf-8")
        )
        cls.ir = json.loads(
            (ROOT / "examples/synthetic-input/lecture-ir.json").read_text(
                encoding="utf-8"
            )
        )

    def test_schemas_are_valid_draft_2020_12(self) -> None:
        Draft202012Validator.check_schema(self.course_schema)
        Draft202012Validator.check_schema(self.ir_schema)

    def test_example_instances_validate(self) -> None:
        Draft202012Validator(self.course_schema).validate(self.profile)
        Draft202012Validator(self.ir_schema).validate(self.ir)

    def test_out_of_page_normalized_geometry_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.ir)
        invalid["sourceRegions"][0]["geometry"]["bbox"]["x"] = 1.01
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.ir_schema).validate(invalid)

    def test_source_ink_must_be_explicitly_immutable(self) -> None:
        invalid = copy.deepcopy(self.ir)
        invalid["sourceRegions"][0]["sourceInk"]["immutable"] = False
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.ir_schema).validate(invalid)

    def test_translation_requires_logical_attachment_and_math_state(self) -> None:
        invalid = copy.deepcopy(self.ir)
        del invalid["translations"][0]["attachedSourceBlock"]
        del invalid["translations"][0]["mathNormalized"]
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.ir_schema).validate(invalid)

    def test_font_minimum_cannot_drop_below_5_5_points(self) -> None:
        invalid = copy.deepcopy(self.profile)
        invalid["translation"]["minimumFontPt"] = 5.4
        with self.assertRaises(ValidationError):
            Draft202012Validator(self.course_schema).validate(invalid)

    def test_margin_roles_are_profile_data(self) -> None:
        roles = {lane["semanticRole"] for lane in self.profile["lanes"]}
        self.assertEqual({"revision", "explanation"}, roles)
        self.assertTrue(all("reliability" in lane for lane in self.profile["lanes"]))


if __name__ == "__main__":
    unittest.main()
