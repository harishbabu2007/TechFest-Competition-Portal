def longestChain(numbers):
  band_len = 0

  for i in range(0,len(numbers)-1):
    band_curr = 1
    for j in range(i,len(numbers)-1):
      if numbers[j]+1 == numbers[j+1]:
        band_curr += 1
      else:
        break

    band_len = max(band_len, band_curr)

  return band_len

numbers = [10203, 10204, 172763, 172764, 172765, 172766]
print(longestChain(numbers=numbers))