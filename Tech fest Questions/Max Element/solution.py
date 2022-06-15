## Solution for max element


def MaxElement(scores):
  rv = -1

  for i in range(len(scores)):
    rv = max(rv, scores[i])

  return rv