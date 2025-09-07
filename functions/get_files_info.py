import os

def get_files_info(working_directory, directory="."):
  abs_working = os.path.abspath(working_directory)
  abs_target = os.path.abspath(os.path.join(abs_working, directory)) 

  inside = get_if_target_inside_working(abs_target, abs_working)

  if not inside:
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

  if os.path.isdir(abs_target) == False:
    return f'Error: "{directory}" is not a directory'

  dir_content = os.listdir(abs_target)
  files_info_list = []
  for file in dir_content:
    try:
      file_info = f"- {file}: file_size={os.path.getsize(os.path.join(abs_target, file))} bytes, is_dir={os.path.isdir(os.path.join(abs_target, file))}"
      files_info_list.append(file_info)
    except Exception as e:
      return f"Error: {e}"

  return "\n".join(files_info_list)

def get_if_target_inside_working(abs_target, abs_working):
  base = abs_working
  prefix = base if base.endswith(os.sep) else base + os.sep
  inside = (abs_target == base) or abs_target.startswith(prefix)
  return inside