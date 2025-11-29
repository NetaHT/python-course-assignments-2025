# random selection of a word from a word bank
import random
from hangman_BL import (
    is_one_english_letter,
    check_valid_input,
    show_hidden_word,
    print_hangman,
    check_win)

def main():
    word_bank= ["balancer", "recombination", "genotype", "phenotype", "thomas morgan", "chromosomes", "pruning", "remodeling", "tubby", "curlyo", "kenyon cells", "mushroom body", "drosophila", "neurons", "synapses"]
    chosen_word= random.choice(word_bank).lower()

#Hello message to the user- prints welcome to the game hangman and the number of trials they have
    print("Welcome to the game Hangman! The number of possible errors you have is: 6")
#creates an empty list to store the letters of the chosen word
    print("The word you need to guess is: " + "_ " * len(chosen_word))

#make sure no more that 6 mistakes are made:
    old_letters_guessed= []
    mistakes= 0

    while mistakes < 6:

#asks the user to guess a letter:
        guessed_letter = input("Please guess a letter ").lower()

        if not is_one_english_letter(guessed_letter):
            continue

        if not check_valid_input(guessed_letter, old_letters_guessed):
            continue

        if guessed_letter in chosen_word:
            show_hidden_word(chosen_word, old_letters_guessed)
        else:
            mistakes += 1
            print("Incorrect guess. You have made {} mistakes.".format(mistakes))
            print_hangman(mistakes)
            show_hidden_word(chosen_word, old_letters_guessed)

        if check_win(chosen_word, old_letters_guessed):
            print("Congratulations! You've won!")
            return

    print_hangman(6)
    print("You Lose! The word was:", chosen_word)

if __name__ == '__main__':
    main()
