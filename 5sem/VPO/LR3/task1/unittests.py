import unittest
from main import print_hello_world

class TestHellowWorld(unittest.TestCase):
    def test_print_hello_world_hello_word_in_out(self):
      # Перехватываем вывод в stdout
      import io
      from unittest.mock import patch
      with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
          print_hello_world()
          output = mock_stdout.getvalue()
          # Проверяем, что в выводе есть текст "Hello, world!"
          assert "Hello, world!" in output

    def test_print_hello_world_and_hi_again_in_out(self):
      """
      Тестирует функцию print_hello_world()
      Проверяет, что функция печатает текст с правильным количеством восклицательных знаков
      """
      # Перехватываем вывод в stdout
      import io
      from unittest.mock import patch
      with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
          print_hello_world()
          output = mock_stdout.getvalue()

          # Проверяем, что в выводе есть текст "And hi again!"
          assert "And hi again!" in output


    def test_print_hello_count_znak(self):

      # Перехватываем вывод в stdout
      import io
      from unittest.mock import patch
      with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
          print_hello_world()
          output = mock_stdout.getvalue()

          # Проверяем, что количество восклицательных знаков в третьей строке находится в диапазоне 5-50
          lines = output.splitlines()
          assert 5 <= len(lines[2]) <= 50
          assert lines[2].strip() == "!" * len(lines[2])


if __name__ == "__main__":
    unittest.main()
