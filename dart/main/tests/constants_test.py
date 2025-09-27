from django.test import TestCase
from main.constants import checkout_map
import re


class ConstantsTests(TestCase):

    def test_checkout_map_values(self):
        """Test that checkout suggestions are valid"""
        # Regex to match S/D/T followed by a number
        regex = r"([SDT])(\d+)"

        for key, value in checkout_map.items():
            values = value.split(" ")
            round_value = 0
            for dart_value in values:
                match = re.match(regex, dart_value)
                if match:
                    multiplier_type = match.group(1)
                    multiplier_value = int(match.group(2))

                    match multiplier_type:
                        case "S":
                            multiplier_value = multiplier_value * 1
                        case "D":
                            multiplier_value = multiplier_value * 2
                        case "T":
                            multiplier_value = multiplier_value * 3
                    round_value += multiplier_value
            self.assertEqual(
                round_value, int(key), f"Failed for key {key} with value {value}"
            )
