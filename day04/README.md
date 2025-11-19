# Recombination Rate Calculator
UI: GUI\
Input: _Drosophila melanogaster gene name/FlyBase IDS_ (FlyBase website)[https://flybase.org/]\
Output: gene location- chromosome, genetic distance and recombination rate.
Data source:(NCBI)[https://www.ncbi.nlm.nih.gov/] website.\
Warnings: 
1. The program warns the user in case of ambigous gene name- a name that can refer to multuple genes. 
2. The program Let's the user know when one of the genes is close to a centromere, according to parameters that I found in an article, as no recombination occurs in these regions in the fly.

---

## Prompts:
**AI tool used:** ChatGPT
1. Please write a program that receives two gene FlyBase IDs and outputs the recombination rate.The program should get the data using an API for NCBI and save the data locally.
The output should refer to the gene location in bp and
calculate the recombination rate in centimorgans. If two genes are on different chromosomes,
let the user know and approximate recombination rate to 50%.
Please generate the user interface as a GUI but seperate the UI from the "buisness logic".
2. Now please add a warning when a gene is located close to a centromere, letting the user know that there is almost no recombination in these regions,
according to these parameters:
"2L": 0.3e6\
"2R": 2.05e6\
"3L": 0.86e6\
"3R": 4.53e6\
"X": 1.53e6\
3.for some reason it accepts gene names as a valid input, but makes mistakes as opposed to when i enter flybase id,
do you know what could be the reason for this?
4. yes, please rewrite the "fetch gene info"

םו

