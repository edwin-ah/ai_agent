import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):
  abs_working = os.path.abspath(working_directory)
  abs_target = os.path.abspath(os.path.join(abs_working, file_path)) 

  inside = get_if_target_inside_working(abs_target, abs_working)

  if not inside:
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

  if not os.path.isfile(abs_target):
    return f'Error: File "{file_path}" not found.'

  if not file_path.endswith(".py"):
    return f'Error: "{file_path}" is not a Python file.'

  try:
    script_dir = os.path.dirname(abs_target)
    args = [sys.executable, os.path.basename(abs_target), *args]
    
    cp = subprocess.run(args, timeout=30, capture_output=True, cwd=working_directory, text=True)

    parts = []
    if cp.stdout:
        parts.append(f"STDOUT:\n{cp.stdout}".rstrip())
    if cp.stderr:
        parts.append(f"STDERR: {cp.stderr}".rstrip())
    if cp.returncode != 0:
        parts.append(f"Process exited with code {cp.returncode}")
    if not parts:
      return "No output produced."
    return "\n".join(parts)

  except Exception as e:
    return f"Error: executing Python file: {e}"




def get_if_target_inside_working(abs_target, abs_working):
  base = abs_working
  prefix = base if base.endswith(os.sep) else base + os.sep
  inside = (abs_target == base) or abs_target.startswith(prefix)
  return inside