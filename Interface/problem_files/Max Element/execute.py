from importlib.machinery import SourceFileLoader
import os
from pathlib import Path

this_file_path = Path(__file__).resolve().parent

def executeProg(func, out_name):
  try:
    global this_file_path
    file_path = os.path.join(this_file_path, "testcases.txt")
    file = open(file_path, "r")
    lines = file.readlines()

    line_txt = []

    for line in lines:
      line_txt.append(line)

    for i in range(len(line_txt)):
      line_txt[i] = line_txt[i].replace("\n", "")

    output = []

    for i in range(1, len(line_txt)):
      arr_input = []
      raw_txt = line_txt[i].split(" ")

      for j in raw_txt:
        arr_input.append(int(j))


      output.append(func.MaxElement(arr_input))

    for i in range(len(output)):
      output[i] = str(output[i]) + "\n"

    output_path = os.path.join(this_file_path, f"./outputs/{out_name}.txt")
    output_file = open(output_path, "w")
    output_file.writelines(output)
    output_file.close()


    return True, "success"
  except Exception as e:
    return False, f"Error\n {e}"


# file_path_user = os.path.join(this_file_path, "user.py")
# file = SourceFileLoader("user", file_path_user).load_module()
# out = executeProg(file, "harish_output")
# print(out)
