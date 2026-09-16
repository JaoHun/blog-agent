import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import config


class ConfigTests(unittest.TestCase):
    def test_load_environment_reads_dotenv_without_manual_env(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_file = Path(temp_dir) / ".env"
            env_file.write_text(
                "\n".join(
                    [
                        "DEEPSEEK_API_KEY=dotenv-key",
                        "BLOG_ROOT=C:\\Blog",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.dict(os.environ, {}, clear=True):
                config.load_environment(env_file)

                self.assertEqual(config.get_deepseek_api_key(), "dotenv-key")
                self.assertEqual(config.get_blog_root(), Path("C:\\Blog"))

    def test_required_environment_values_raise_explicit_errors(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "DEEPSEEK_API_KEY environment variable is not set"):
                config.get_deepseek_api_key()

            with self.assertRaisesRegex(RuntimeError, "BLOG_ROOT environment variable is not set"):
                config.get_blog_root()


if __name__ == "__main__":
    unittest.main()
