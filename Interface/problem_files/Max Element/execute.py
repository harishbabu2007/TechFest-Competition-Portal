def executeProg():
  try:
    # from solution import MaxElement
    from user import MaxElement

    file = open("testcases.txt", "r")
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


      output.append(MaxElement(arr_input))

    for i in range(len(output)):
      output[i] = str(output[i]) + "\n"

    output_file = open("output.txt", "w")
    output_file.writelines(output)
    output_file.close()


    return "success"
  except Exception as e:
    return f"Error\n {e}"

  

out = executeProg()
print(out)
