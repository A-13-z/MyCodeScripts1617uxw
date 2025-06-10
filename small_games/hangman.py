from nltk.corpus import words                 #download this by running import nltk and nltk.download() in the powershell
import random
from PyDictionary import PyDictionary         #this is optional and is not related to hangman 
word = random.choice(words.words())
turns = 12                                    #no of times a person can fail before losing
guesses = ''
while turns > 0:
    failed = 0

    for char in word:
        if char in guesses:
            print(char, end= ' ')
        else:
            print('_' ,end =' ')
            failed += 1

    if failed == 0:
        print('\nYou win')
        print('The word is ' + word + '\n' + 'Meaning: ' + str(PyDictionary.meaning(word)))
        break
    
    guess = input('\nGuess a character: ')
    if len(guess) != 1:
        guess = input('\nGuess one character at a time: ')
    guesses += guess

    if guess not in word:
        turns -= 1
        print('Wrong!! You have ' + str(turns) + ' turns left')

        if turns == 0:
            print('You Lose. THE WORD IS ' + str(word) + '\n' + 'Meaning: ' + str(PyDictionary.meaning(word)))
            break
