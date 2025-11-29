#check user input is one english letter, else print error
def is_one_english_letter (guessed_letter): 
    if len(guessed_letter) != 1 and not guessed_letter.isalpha():
        print("Error. Please make sure you enter a single English letter.")
        return False
    elif len(guessed_letter) !=1:  
        print("Error. Please make sure you enter a single letter.")
        return False
    elif not guessed_letter.isalpha():    
        print("Error. Please make sure you enter an English letter.")
        return False
    else:
        return True

#check if letter has already been guessed, if not add to list of guessed letters
def check_valid_input(guessed_letter, old_letters_guessed):
    guessed_letter= guessed_letter.lower()
    
    if guessed_letter not in old_letters_guessed:
        old_letters_guessed.append(guessed_letter)
        return True
    else :   
        print("You have already guessed this letter. Please try again.")
        return False   

#show the hidden word with guessed letters revealed    
def show_hidden_word(chosen_word, old_letters_guessed):
    blank_word = ""
    
    for letter in chosen_word:
        if letter.lower() in old_letters_guessed:
            blank_word += letter + ""
        else:
            blank_word += "_ "
        
    print(blank_word)
    return blank_word
       

def check_win(secret_word, old_letters_guessed):
    for letter in secret_word:
        if letter.lower() not in old_letters_guessed:
            return False
    return True

def print_hangman(num_of_tries):        
    hangman_photos = { 0 : """
    x-------x""", 1: """
    x-------x
    |
    |
    |
    |
    |""", 2 : """
    x-------x
    |       |
    |       0
    |
    |
    |""", 3 : """
    x-------x
    |       |
    |       0
    |       |
    |
    |
    """, 4 : """
    x-------x
    |       |
    |       0
    |      /|\\
    |
    |""", 5 : """
    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |
    """, 6 :"""
    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |
    """}

    print (hangman_photos.get(num_of_tries))

