# Longest Chain - Problem Statement

## Overview

Mohan Likes consecutive numbers. he is given a list of numbers. write a programe to find the longest chain. A chain is a subsequence of consecutive integers.

example (1) - "1,2,3,-5,3,6,7,8,9". should return

```
4
```

in the example (1) the answer is 4
because "6,7,8,9" is the longest subsequence of consecutive integers (chain).

#

## Constraints

- `0 < len(numbers) < 10`
- `0 < numbers[i] < 10^5`
- `Expected time complexity 0(n)`

#

## Examples

Input:

```
10 11 13 14 15 -4 -2
```

Output:

```
3
```

Input:

```
10203 10204 172763 172764 172765 172766
```

Output:

```
4
```

#

## Development

Complete the function `LongestChain` in the editor below. which takes an argument `numbers` which is the list of numbers . The function should finally return the `longest` chain.

#

## Submitting

Click the `Submit` button below to submit the code and get and instant judgement. If you have any problem in the code click the `Reset` button to reset the code.
