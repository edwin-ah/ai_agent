import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        required=["directory"],
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the file in the specified directory, truncating at 10000 charactes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Reads the file in the specified directory, truncating at 10000 charactes, constrained to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the .py file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Runs the .py file.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to the .py file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Writes to the .py file.",
            ),
            "content": types.Schema(
              type=types.Type.STRING,
              description="The content to be written"
            )
        },
    ),
)

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