from functions.get_files_info import get_files_info 
from functions.get_file_content import get_file_content
from functions.write_file import write_file

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

def test_write_file(working_dir, file_path, content):
  print(write_file(working_dir, file_path, content))

test_write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
test_write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
test_write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

#test_read_file_content("calculator", "main.py")
#test_read_file_content("calculator", "pkg/calculator.py")
#test_read_file_content("calculator", "/bin/cat")
#test_read_file_content("calculator", "pkg/does_not_exist.py")
#check_current_dir()