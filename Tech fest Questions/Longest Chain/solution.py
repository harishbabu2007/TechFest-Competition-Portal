## Please read the problem statement before coding
## Complete the function below and the return the answer
## very smooth typing 


def LongestChain(numbers):
  chain_len = 0

  for i in range(0,len(numbers)-1):
    band_curr = 1
    for j in range(i,len(numbers)-1):
      if numbers[j]+1 == numbers[j+1]:
        band_curr += 1
      else:
        break

    chain_len = max(chain_len, band_curr)

  return chain_len


## This is the solution to LongestChain function .... 
## this file should not be found in the server