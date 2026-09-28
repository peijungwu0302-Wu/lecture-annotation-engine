from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = [
    "inspect_pdf.py",
    "build_ir.py",
    "build_source_mask.py",
    "render_overlay.py",
    "verify_pdf.py",
]


class CliSurfaceTests(unittest.TestCase):
    def test_phase_one_scripts_expose_help(self) -> None:
        for script in SCRIPTS:
            with self.subTest(script=script):
                result = subprocess.run(
                    [sys.executable, str(ROOT / "scripts" / script), "--help"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("usage:", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
