import logging
from unittest.mock import patch

from main import calculate_age_statistics, parse_person_data, display_people_data, get_people_data

import unittest
import io
import sys


class TestPeopleData(unittest.TestCase):
    def test_parse_person_data_valid(self):
        self.assertEqual(parse_person_data('Иван Иванов 25'), ('Иванов', 'Иван', 25))

    def test_parse_person_data_valid2(self):
        self.assertEqual(parse_person_data('Иван    Иванов    25'), ('Иванов', 'Иван', 25))

    def test_parse_person_data_valid3(self):
        self.assertEqual(parse_person_data('Иван    \nИванов    \n25'), ('Иванов', 'Иван', 25))

    def test_parse_person_data_invalid(self):
        with self.assertRaises(ValueError):
            parse_person_data('Иван Иванов')

    def test_calculate_age_statistics(self):
        people = [('Иванов', 'Иван', 25), ('Петров', 'Петр', 30), ('Сидоров', 'Сидор', 20)]
        min_age, max_age, avg_age = calculate_age_statistics(people)
        self.assertEqual(min_age, 20)
        self.assertEqual(max_age, 30)
        self.assertAlmostEqual(avg_age, 25.00, places=2)

    def test_zero_person(self):
        people = []
        min_age, max_age, avg_age = calculate_age_statistics(people)
        self.assertEqual(min_age, None)
        self.assertEqual(max_age, None)
        self.assertAlmostEqual(avg_age, None)

    def test_single_person(self):
        people = [('Смирнов', 'Алексей', 40)]
        min_age, max_age, avg_age = calculate_age_statistics(people)
        self.assertEqual(min_age, 40)
        self.assertEqual(max_age, 40)
        self.assertAlmostEqual(avg_age, 40.00, places=2)

    def test_same_ages(self):
        people = [('Иванов', 'Иван', 30), ('Петров', 'Петр', 30), ('Сидоров', 'Сидор', 30)]
        min_age, max_age, avg_age = calculate_age_statistics(people)
        self.assertEqual(min_age, 30)
        self.assertEqual(max_age, 30)
        self.assertAlmostEqual(avg_age, 30.00, places=2)

    def test_display_people_data(self):
        people = [('Иванов', 'Иван', 25), ('Петров', 'Петр', 30)]
        expected_output = "Иванов Иван 25\nПетров Петр 30\n"

        captured_output = io.StringIO()
        sys.stdout = captured_output
        display_people_data(people)
        sys.stdout = sys.__stdout__

        self.assertEqual(captured_output.getvalue(), expected_output)

    @patch('builtins.input', side_effect=['Иван Иванов 12', 'stop'])
    def test_input(self, mock):
        people = get_people_data()
        person = [('Иванов', 'Иван', 12)]
        self.assertEqual(person, people)

    @patch('builtins.input', side_effect=['Иван    Иванов     10',
                                          'Иван    Иванов     42',
                                          'stop'])
    def test_input2(self, mock):
        people = get_people_data()
        person = [('Иванов', 'Иван', 10), ('Иванов', 'Иван', 42)]
        self.assertEqual(person, people)


if __name__ == "__main__":
    unittest.main()
