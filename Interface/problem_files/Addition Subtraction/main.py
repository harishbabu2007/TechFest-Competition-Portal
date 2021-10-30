## This file will run the testcases and will determine the results

from _pytest.config import ExitCode
from pytest import main

from AdditionSubtraction import AdditionSubtraction
# from solution import AdditionSubtraction

## Just for testrun
print(AdditionSubtraction(["32 + 698", "3801 - 2", "45 + 43", "123 + 49"]))


## Run unit tests autmatically
result = main()

if result  == ExitCode.TESTS_FAILED:
  print("Failed")
elif result  == ExitCode.OK:
  print("solved")
