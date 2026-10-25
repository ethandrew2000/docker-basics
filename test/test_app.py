import contextlib
import io
import os
import random
import unittest
from unittest.mock import Mock, patch

from src.app import ABILITIES, NAMES, ROLES, generate_party, main, roll_ability


class PartyTests(unittest.TestCase):
    def test_ability_discards_lowest_die(self):
        rng = Mock()
        rng.randint.side_effect = [2, 6, 3, 5]
        self.assertEqual(roll_ability(rng), 14)
        self.assertEqual(rng.randint.call_count, 4)
        rng.randint.assert_called_with(1, 6)

    def test_all_party_sizes_have_unique_valid_characters(self):
        for size in range(1, 7):
            for seed in range(20):
                with self.subTest(size=size, seed=seed):
                    party = generate_party(size, random.Random(seed))
                    self.assertEqual(len(party), size)
                    self.assertEqual(len({hero["name"] for hero in party}), size)
                    for hero in party:
                        self.assertIn(hero["name"], NAMES)
                        self.assertIn(hero["role"], ROLES)
                        self.assertEqual(len(hero["scores"]), len(ABILITIES))
                        self.assertTrue(all(3 <= score <= 18 for score in hero["scores"]))

    def test_same_seed_reproduces_party(self):
        self.assertEqual(generate_party(3, random.Random(42)),
                         generate_party(3, random.Random(42)))

    def test_invalid_party_sizes_are_rejected(self):
        for size in (0, -1, 7):
            with self.subTest(size=size), self.assertRaises(ValueError):
                generate_party(size, random.Random(42))

    def test_cli_prints_environment_and_selected_party_size(self):
        output = io.StringIO()
        with patch.dict(os.environ, {"APP_ENV": "production"}), contextlib.redirect_stdout(output):
            main(["--count", "2", "--seed", "42"])
        text = output.getvalue()
        self.assertIn("Environment: production", text)
        self.assertIn("Your Adventure Party", text)
        self.assertIn("Your party of 2 is ready", text)
        self.assertIn("STR", text)

    def test_cli_defaults_work_without_environment_variable(self):
        output = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), contextlib.redirect_stdout(output):
            main(["--seed", "42"])
        self.assertIn("Environment: development", output.getvalue())
        self.assertIn("Your party of 3 is ready", output.getvalue())

    def test_cli_rejects_invalid_count(self):
        for count in ("0", "7", "abc"):
            with self.subTest(count=count), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    main(["--count", count])
                self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
