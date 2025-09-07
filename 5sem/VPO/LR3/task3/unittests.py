import unittest
from unittest.mock import patch

from main import calculate_rectangle_area

class TestRectangleArea(unittest.TestCase):
   def test_positive_values(self):
      self.assertEqual(calculate_rectangle_area(4, 5), 20)

   def test_zero_length(self):
      self.assertEqual(calculate_rectangle_area(0, 5), 0)

   def test_zero_width(self):
      self.assertEqual(calculate_rectangle_area(4, 0), 0)

   def test_negative_length(self):
      with self.assertRaises(ValueError):
       calculate_rectangle_area(-4, 5)

   def test_negative_width(self):
      with self.assertRaises(ValueError):
       calculate_rectangle_area(4, -5)

   def test_non_numeric_length(self):
      with self.assertRaises(TypeError):
       calculate_rectangle_area("abc", 5)

   def test_non_numeric_width(self):
      with self.assertRaises(TypeError):
       calculate_rectangle_area(4, "def")

   @patch('builtins.input', side_effect=['10', '20'])
   def test_input_value(self, mock):
      length = int(input("Введите длину: "))
      width = int(input("Введите ширину: "))
      area = calculate_rectangle_area(length, width)
      self.assertEqual(area, 200)


if __name__ == "__main__":
    unittest.main()