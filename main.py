import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info 
from functions.get_files_info import schema_get_files_info
from functions.get_files_info import schema_get_file_content
from functions.get_files_info import schema_run_python_file
from functions.get_files_info import schema_write_file
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt")
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        print("verbosity turned on")
    else:
        print("verbosity turned off")

    user_prompt = args.user_prompt
    is_verbose = args.verbose

    model_name = os.environ.get("GEMINI_MODEL")
    
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

    Assume relevant code is within the current project.
    Start by exploring the file structure if it's asked about code you doesn't already know.
    Use get_files_info to begin this exploration.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info, 
            schema_get_file_content, 
            schema_run_python_file, 
            schema_write_file
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    should_continue = True

    i = 1
    while i <= 20 and should_continue:
        did_call_tools = False
        try:
            response = client.models.generate_content(
                model=model_name, 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
            )
        except Exception as e:
            print(f"Something went wrong trying to generate content: {e}")
            break

        try:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
                    for part in candidate.content.parts:
                        if part.function_call:
                            did_call_tools = True
                            fc = part.function_call
                            tool_content = call_function(fc, verbose=is_verbose)
                            # validate
                            parts = getattr(tool_content, "parts", []) # try to get the attribute parts from tool_content, [] if did not succeed
                            if not parts or not getattr(parts[0], "function_response", None):
                                raise RuntimeError("Function call returned invalid tool content")
                            resp = parts[0].function_response.response
                            func_resp = types.FunctionResponse(name=fc.name, response=resp)
                            messages.append(types.Content(role="user", parts=[types.Part(function_response=func_resp)]))

                            if is_verbose:
                                print(f"-> {resp}")
            if did_call_tools:
                continue
            elif response.text:
                print(response.text)
                should_continue = False
                break
            else:
                break

        except RuntimeError as re:
            print(f"There was a runtime error: {re}")
            break
        except Exception as e:
            print(f"Something want wrong trying to call python file: {e}")
            break
                
        if is_verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        i += 1

if __name__ == "__main__":
    main()