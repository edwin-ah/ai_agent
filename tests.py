from functions.get_files_info import get_files_info 
from functions.get_files_info import get_file_content

def check_current_dir():
  res = "Result for current directory:\n"
  res += get_files_info("calculator", ".")
  print(res)

def check_pkg_dir():
  dir = "pkg"
  res = f"Result for '{dir}' directory:\n"
  res += get_files_info("calculator", dir)
  print(res)

def check_bin_dir():
  dir = "/bin"
  res = f"Result for '{dir}' directory:\n"
  res += get_files_info("calculator", dir)
  print(res)

def check_back_dir():
  dir = "../"
  res = f"Result for '{dir}' directory:\n"
  res += get_files_info("calculator", dir)
  print(res)

def test_read_file_content(working_dir, file_path):
  print(get_file_content(working_dir, file_path))


test_read_file_content("calculator", "main.py")
test_read_file_content("calculator", "pkg/calculator.py")
test_read_file_content("calculator", "/bin/cat")
test_read_file_content("calculator", "pkg/does_not_exist.py")