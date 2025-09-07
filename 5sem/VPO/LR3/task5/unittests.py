import io
import os
import shutil
import unittest
from unittest.mock import patch

from main import search_files

class TestSearchFiles(unittest.TestCase):

  def setUp(self):
      self.base_dir = f'{os.path.dirname(os.path.abspath(__file__))}/test_data_5_task'
      os.makedirs(os.path.join(self.base_dir, "empty_directory"), exist_ok=True)
      os.makedirs(os.path.join(self.base_dir, "test_dir"), exist_ok=True)
      os.makedirs(os.path.join(self.base_dir, "test_dir", "subdir1"), exist_ok=True)

      with open(os.path.join(self.base_dir, "test_dir", "file1.txt"), "w") as f:
          f.write("Content of file1.txt")

      with open(os.path.join(self.base_dir, "test_dir", "file2.txt"), "w") as f:
          f.write("Content of file2.txt")

      with open(os.path.join(self.base_dir, "test_dir", "file.py"), "w") as f:
          f.write("Content of file.py")

      with open(os.path.join(self.base_dir, "test_dir", "subdir1", "file3.txt"), "w") as f:
          f.write("Content of file3.txt")

  def tearDown(self):
      shutil.rmtree(self.base_dir)

  def test_empty_directory(self):
      with (patch('sys.stdout', new_callable=io.StringIO) as mock_stdout):
            search_files(f"{self.base_dir}/empty_directory", "txt")
            output = mock_stdout.getvalue()
            lines = output.splitlines()
            self.assertEqual(len(lines), 0)



  def test_subdirectories(self):
      with (patch('sys.stdout', new_callable=io.StringIO) as mock_stdout):
          search_files(f"{self.base_dir}/test_dir", "txt")
          output = mock_stdout.getvalue()
          lines = output.splitlines()
          result =[
              f"{self.base_dir}/test_dir/file2.txt",
              f"{self.base_dir}/test_dir/file1.txt",
              f"{self.base_dir}/test_dir/subdir1/file3.txt"
          ]
          print(lines)
          self.assertEqual(len(lines), 3)
          for i in range(3):
            self.assertEqual(lines[0], result[0])

  def test_another_extension(self):
      with (patch('sys.stdout', new_callable=io.StringIO) as mock_stdout):
          search_files(f"{self.base_dir}/test_dir", "py")
          output = mock_stdout.getvalue()
          lines = output.splitlines()
          result =[
              f"{self.base_dir}/test_dir/file.py",
          ]
          self.assertEqual(len(lines), 1)
          for i in range(1):
            self.assertEqual(lines[0], result[0])


if __name__ == "__main__":
    unittest.main()