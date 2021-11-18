## Please read the problem statement before coding
## Complete the function below and the return the answer


def MaxElement(scores):
  max_value = 0
  # Write your code in this funtion
  
  for i in range(len(scores)):
    max_value = max(scores[i], max_value)

  return max_value
