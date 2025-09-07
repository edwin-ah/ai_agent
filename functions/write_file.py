import os

def write_file(working_directory, file_path, content):
  abs_working = os.path.abspath(working_directory)
  abs_target = os.path.abspath(os.path.join(abs_working, file_path)) 

  inside = get_if_target_inside_working(abs_target, abs_working)

  if not inside:
    f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

  try:
    if not os.path.exists(file_path):
      with open(abs_target, "w") as fp:
        pass

    with open(abs_target, "w") as f:
      f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f'Error: {e}'


def get_if_target_inside_working(abs_target, abs_working):
  base = abs_working
  prefix = base if base.endswith(os.sep) else base + os.sep
  inside = (abs_target == base) or abs_target.startswith(prefix)
  return inside