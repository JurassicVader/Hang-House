from tkinter import *
import random
import tkinter as tk
import string
'''
Spencer and Adel
'''

# Function that will read our words from the text file
def readWords():
    with open("25words.txt", 'r') as wordsFile:
        words = wordsFile.readlines()

    # Skipping all empty spaces and new lines
    # Also making everything lowercase for simplicity
    return list(x.lower().replace("\n", '') for x in list(words))

def keyPressed(event):
    # Initializing variables
    global tries, maskedWord, missedLetters, solved, wordLetters
    
    if(len(wordLetters) > 0 and tries < 7):
        
        # Updating our wordList's * with correct letters
        wordList = [letter if letter in guessedLetters else '*' for letter in word.lower()]

        # print *** in console
        # Testing phase in console
        print(' '.join(wordList).lower().capitalize())

        # Message to display in canvas and also calling the function to update it
        msg1 = "Guess a word: " + ' '.join(wordList).lower().capitalize()
        updateMsg1(msg1)

        # New variable for user typed letters
        # An event where if a letter is pressed, it's assigned to used letters
        userLetters = event.char

        # If statement that will return nothing if the user entered something that's not in the alphabet
        if not userLetters.isalpha():
            return
        
        # Duplicate letters check (if user entered a letter they have already guessed)
        if userLetters in guessedLetters:
            return

        # If a letter is in the alphabet AND not a prior guessed letter
        if userLetters in alphabet - guessedLetters:
            guessedLetters.add(userLetters) # ... add that new letter to already guessed letters

            # Now checking if that new letter is in hidden word
            if userLetters in wordLetters:
                wordLetters.remove(userLetters) # Removing from the word's letter set
                # updating our wordList's * with correct letters
                wordList = [letter if letter in guessedLetters else '*' for letter in word.lower()]

                # Updating how the message looks.
                msg1 = "Guess a word: " + ' '.join(wordList).lower().capitalize()
                # Passing message to function in order to update message on canvas
                updateMsg1(msg1)

                # This block of code will only run if there are no letters to be solved
                if(len(wordLetters) == 0):
                    wordList = [letter if letter in guessedLetters else '*' for letter in word.lower()]
                    msg1 = "Guess a word: " + ' '.join(wordList).lower().capitalize() # Updating how the message looks
                    msg3 = f"Congratulations, you win. \n \n Press ENTER to play again." # You lil winner you
                    solved = True

                    # Passing messages to message functions
                    updateMsg1(msg1)
                    updateMsg3(msg3)
                    
                    
            else:
                tries += 1 # Incrementing the number of tries 
                
                #Checking if we have incremented past 6 tries (end of game)
                if(tries > 6): # You snooze you lose
                    missedLetters += userLetters + ',' # adding the users guessed letters to new empty variable 

                    #I think unneeded(?)
                    #msg2 = 'Missed : ' + missedLetters.rstrip(',').lower()
                    #updateMsg2(msg2)

                    # This message 3 will only be displayed if user is out of tries
                    msg3 = f"Awe better luck next time :( \n The word was: {word} \n Press ENTER to play again."
                    updateMsg3(msg3)
                    # Passing the number of tries to the draw function 
                    draw(tries)

                # Only other possibility - haven't won nor lost, but still have guesses to make
                else:  
                    # Increment user letter choice into our variable
                    missedLetters += userLetters + ','
                    # Assigning our message that states the missed letters into our variable
                    # ... all in individualized and lower-cased
                    msg2 = 'Missed : ' + missedLetters.rstrip(',').lower()
                    
                    # Passing new values to functions 
                    updateMsg2(msg2)
                    draw(tries)

    #returning nothing
    return


# The following 3 functions, we pass the messages (msg#) to the canvas
def updateMsg1(msg1):
    window.maskedWordLabel.configure(text=msg1)

def updateMsg2(msg2):
    window.missedLettersLabel.configure(text=msg2)

def updateMsg3(msg3):
    window.finalMessageLabel.configure(text=msg3)


# Our drawing function for the outline of the house
def draw(tries):

    # Initializing our window (i.e. the window / 7th line)
    radius = 30

    color = 'brown' # Color of wood for ultra realism graphics (WARNING: Must have GTX 3090 or computer will throttle)
    lineWidth = 6

    # The number of tries is initialized first at 0, so this won't do anything until user guesses at least once
    # With each guess, these 'if functions' will go through and draw appropriate lines

    # 1 - 4 tries is the walls
    if tries >= 1:
        canvas.create_line(100, 320, 400, 320, tags="hang", fill=color, width=lineWidth)
    if tries >= 2:
        canvas.create_line(100, 320, 100, 160, tags="hang", fill=color, width=lineWidth)
    if tries >= 3:
        canvas.create_line(400, 320, 400, 160, tags="hang", fill=color, width=lineWidth)
    if tries >= 4:
        canvas.create_line(100, 160, 400, 160, tags="hang", fill=color, width=lineWidth)
        # Tries 5 and 6 is the roof
    if tries >= 5:
        canvas.create_line(100, 160, 250, 80, tags="hang", fill=color, width=lineWidth)
    if tries >= 6:
        canvas.create_line(250, 80, 400, 160, tags="hang", fill=color, width=lineWidth)
        # The window
    if tries >= 7:
        canvas.create_oval(250 - radius, 130 - radius, 250 + radius, 110 + radius, tags="hang", outline='blue', width=3)



# Function that will start a new game
def newGame():
    # More global variables
    global tries, maskedWord, word, missedLetters, guessedLetters, alphabet, wordLetters

    # Clear any previous game that may be on the canvas
    canvas.delete("hang")

    # Choosing a random word from list and assigning it to word variable
    word = random.choice(words)

    # Print the word in the console (for the devs)
    print(word)

    # Creating a set of the letters in a word / making them lowercase
    wordLetters = set(word.lower())

    # Masking the letters of the word with *** (stars)
    maskedWord = "*" * len(word)

    # Creating a set to hold any guessed letters
    guessedLetters = set()

    # Creating a set of all alphabetical letters
    # We use this for subtracting with another set - helps determine choices are letters
    alphabet = set(string.ascii_lowercase)

    # initializing
    tries = 0
    missedLetters = ''

    # Display first message and the masked word
    msg1 = "Guess a word: " + maskedWord
    msg2 = ""
    msg3 = ""

    # passing values while function calling
    updateMsg1(msg1)
    updateMsg2(msg2)
    updateMsg3(msg3)

    draw(tries)


def play(event):
    global tries, solved

    # Don't execute a new game unless the game is finished
    if (tries < 7 and solved == True) or (tries == 7 and solved == False):
        newGame()
        solved = False
        tries = 0




#Main starts here

#initializing the window
window = Tk()
window.title("HangHouse")

# Initializing
word = maskedWord = missedLetters = ''
tries = 7
solved = False

# Setting size of canvas and text font
size = 500
font = 'calibri 13 bold'

canvas = Canvas(window, width = size, height = size)
canvas.pack()

#initializing the 3 label messages (i.e., position, font, color, etc)
window.maskedWordLabel = tk.Label(window, text='maskedWord', font=(font), fg='blue', justify=CENTER)
window.maskedWordLabel.place(x=180, y=360)

window.missedLettersLabel = tk.Label(window, text='missedLetters', font=(font), fg='red', justify=CENTER)
window.missedLettersLabel.place(x=180, y=390)

window.finalMessageLabel = tk.Label(window, text='final message', font=(font), fg='green', justify=CENTER)
window.finalMessageLabel.place(x=180, y=420)

# readWords will read the file and assigning it to words
words = readWords()

# Function call that will start the game
newGame()

canvas.focus_set()

# Letting the user presses ENTER to play again
canvas.bind('<Return>', play)
canvas.bind('<Key>', keyPressed)

window.mainloop()
