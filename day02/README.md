**AI tools used:** co-pilot, claude sonnet 3.5

# LastDateFor Collection

## Function use:
In our lab, we work with Drosophila Melanogaster, that have a relatively short life cycle. Therefore, when we collect offspring from a cross, we need to make sure
that this cross was set up less than 18 days ago, otherwise we could already have F2 progeny, which we cannot always cotrol for in terms of
desired genotypes. This calculation happens on a daily basis in our lab.

## Prompts that I used:
1. can you open a new file under the name "LastDateForCollection.py" under the folder "day02"
2. Can you generate in this file a function that asks the user to input a date and outputs the date that is 18 days before the input date, according to the christian calendar?
3. can you generate a new GUI file for this function?
4. so can you generate the same function with only a command line? no input?

---

# TransfectionEfficiency

## Function use:
This function can be used to calculate the tansfection efficiency of two cell lines we use in our lab, called "S2" and "BG3" given the total number of cells and the number of GFP+ cells on the day of experiment. The function accounts for average doubling time of each cell line, as found on the internet (24h for S2 and 30h for BG3), it outputs an alert if transfection efficiency is low (<20%) or too high (>100%).

## Prompts that I used:
1. please write a function so that the input that the user gives is the cell type, total number of cells on the day of the experiment, the number of GFP positive cells on the day of the experiment, and the number of days since transfection. the function should output the transfection percentage taking into account the doubling rate of the cell type, according to acerage doubling time reported on the internet.
2. please modify this so that the function takes into account duplication rate of the cells, assuming that only one of two daughter cells of a duplication event would contain the transfected plasmid. use the average duplication of S2 and BG3 from the internet.
3. can you add an alert if transfection efficiency is below 20%?
4. please add an alert if effieciency if over 100%, telling the user to check if their input is correct
5. can you generate two more file, one that has an input interface, and one with a GUI interface, name "TransfectionEfficiency_in.py" and TransfectionEfficiency_GUI.py" respectively?
   
