I used my code for calculating the efficiency of a transfection, using CLI interface. I copied the buisness logic into a new file named "TransfectionEfficiency_BuisnessLogic".

## Testing the code
I tested the code in a new file named "test_TransfectionCalculator" under the folder "tests". I used pytest to test the code, and made sure it passed all the tests.

## Third party library
chatGPT suggested a few third party libraries, such as:
1. typer for "shorter, more readable, and add automatic help, colors, and type hints".
2. numpy: to "make numeric operations vectorized (useful if you ever process many samples at once)."
3. rich: "colored text, tables, and progress bars."
   I felt that all of these suggestions could be nice add-ons but weren't very necessary in the case of my specific function and needs.
   However, to try adding a third party library, I tried typer, for this I installed it (pip install typer). This is a nice add on because it lets the
   user know what is missing (especiallty useful in CLI configuration) and has a nice "help" option (in the terminal: python TransfectionEfficiency_typer.py --help).


## Prompts
**AI tool-** I used ChatGTP and gave him the following prompts:
1. I have this code file: (enter code file), how can I run pytest on this?
2. I have this code file: (enter code file), can I replace any part of it with a third party library?

## Dependencies:
1. For test file- pytest
2. For typer file- typer
3. TransfectionEfficiency_BuisnessLogic- must exist in repo
