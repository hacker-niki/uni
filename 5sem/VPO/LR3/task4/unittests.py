import unittest
import os

from main import generate_html_table


class TestHtmlTableGeneration(unittest.TestCase):
    def test_html_file_creation(self):
        generate_html_table()
        self.assertTrue(os.path.exists("gradient_table.html"))

    def test_html_content(self):
        generate_html_table(rows=3, columns=2)
        with open("gradient_table.html", "r", encoding="utf-8") as file:
            content = file.read()
            expected_start = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">"""
            self.assertTrue(content.startswith(expected_start))
            self.assertIn('<tr style="background-color: rgb(255, 255, 255);">', content)
            self.assertIn('<tr style="background-color: rgb(128, 128, 128);">', content)
            self.assertIn('<tr style="background-color: rgb(1, 1, 1);">', content)
            self.assertIn('<td></td><td></td>', content)
            self.assertNotIn('<td></td><td></td><td></td>', content)

    def test_html_content2(self):
        generate_html_table(rows=255, columns=255)
        with open("gradient_table.html", "r", encoding="utf-8") as file:
            content = file.read()
            expected_start = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">"""
            self.assertTrue(content.startswith(expected_start))
            self.assertIn('<tr style="background-color: rgb(255, 255, 255);">', content)
            self.assertIn('<tr style="background-color: rgb(128, 128, 128);">', content)
            self.assertIn('<tr style="background-color: rgb(1, 1, 1);">', content)
            self.assertIn('<td></td><td></td>', content)
            self.assertIn('<td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>', content)

        def test_html_content2(self):
            generate_html_table(rows=255, columns=255)
            with open("gradient_table.html", "r", encoding="utf-8") as file:
                content = file.read()
                expected_start = """<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">"""
                self.assertTrue(content.startswith(expected_start))
                self.assertIn('<tr style="background-color: rgb(255, 255, 255);">', content)
                self.assertIn('<tr style="background-color: rgb(128, 128, 128);">', content)
                self.assertIn('<tr style="background-color: rgb(1, 1, 1);">', content)
                self.assertIn('<td></td><td></td>', content)
                self.assertIn(
                    '<td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>',
                    content)

        def test_html_content3(self):
            with self.assertRaises(ValueError):
                generate_html_table(rows=-10, columns=-10)
            

    def tearDown(self):
        if os.path.exists("gradient_table.html"):
            os.remove("gradient_table.html")


if __name__ == "__main__":
    unittest.main()
