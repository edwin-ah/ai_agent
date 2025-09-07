import os

def get_file_content(working_directory, file_path):
  MAX_CHARS = 10000

  abs_working = os.path.abspath(working_directory)
  abs_target = os.path.abspath(os.path.join(abs_working, file_path)) 

  inside = get_if_target_inside_working(abs_target, abs_working)
  
  if not inside:
    return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

  if file_path.endswith(os.sep) or not os.path.isfile(abs_target):
    return f'Error: File not found or is not a regular file: "{file_path}"'

  try:
    with open(abs_target, "r") as f:
      file_content_string = f.read(MAX_CHARS)

    if len(file_content_string) >= MAX_CHARS:
      file_content_string += f'\n[...File "{file_path}" truncated at 10000 characters]'
    return file_content_string
  except Exception as e:
    return f"Error: {e}"



def get_if_target_inside_working(abs_target, abs_working):
  base = abs_working
  prefix = base if base.endswith(os.sep) else base + os.sep
  inside = (abs_target == base) or abs_target.startswith(prefix)
  return inside