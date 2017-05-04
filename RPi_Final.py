###############################################################################################################################
#Collaborators: Jordan Edgel, Kaleb Rhody, Thomas Presicci, Alex Reed
#Description: A series of trivia questions asked entirely in Morse Code to be solved by competitors. Players are scored by time.
#Due Date: May 10, 2017
###############################################################################################################################
from time import *
#import pygame
#import RPi.GPIO as GPIO
from Tkinter import *

# Dot = one unit / Dash = three units
# Space between digits = one unit
# Space between characters = three units
# Space between words = seven units

# Delete last word = eight dots

class Game(Canvas):
        def __init__(self, master):
                self.master = master
                Canvas.__init__(self,master)
                master.columnconfigure(0, weight = 1)
                master.rowconfigure(0, weight = 1)
                
                # List of questions in form of 1s and 0s
                # 0 = dash, 1 = dot
                self.questions = ['.--/..../../-.-./.... .-./---/...-/./.-. .--/.-/... -/..../. ..-./../.-./.../- -/--- ./-..-/.--./.-../---/.-./. --/.-/.-./...', # Question 1, [Which rover was the first to explore Mars? - Sojourner]
                             '..../---/.-- --/..-/-.-./.... -/../--/. -../---/./... .- .../..-/-. .-./.-/-.-- -/.-/-.-/. -/--- -/.-./.-/...-/./.-.. -/--- ./.-/.-./-/....', # Question 2, [How much time does a sun ray take to travel to Earth? - 8 minutes]
                             '--/../.-../-.-/-.-- .--/.-/-.-- -.../.-../.-/-.-./-.- ..../---/.-../. -../../.../-/.-/-./-.-./. ../-. .-../../--./..../- -.--/./.-/.-./...', # Question 3, [Milky Way black hole distance in light years? - 27,000 light years]
                             '.--/..../.-/- ../... -/..../. .../..-/-. --/---/.../-/.-../-.-- --/.-/-../. ---/..-.'] # Question 4, [What is the sun mostly made of? - Hydrogen]
                
                # Dict for the times of each dot and dash
                self.morse = {'-':UNIT*3, '.':UNIT}

                # Used to switch the LED the word is displayed on
                self.leds = {RED:GREEN, GREEN:RED}
                
                # Initialized variables
                self.current_question = 0
                self.current_word = -1
                self.current_led = RED
                self.answering = False

        def gui(self):
                self.grid()
                
                img = PhotoImage( file = "Neil.gif" )
                pic = Label(self.master, image = img)
                pic.image = img
                pic.grid(row = 0, column = 0, sticky = N+S+E+W)

                self.entry = Entry(self.master)
                self.entry.width = 200
                self.entry.grid(row = 3, column = 0, columnspan = 2)

                self.timer = Label(self.master, text = "Time: ", state = DISABLED)
                self.timer.grid(row = 0, column = 2, columnspan = 2, sticky = W)

                self.qNumber = Label(self.master, text = "Question # {}".format(self.current_question + 1), state = DISABLED)
                self.qNumber.grid(row = 1, column = 2, columnspan = 2, sticky = N+W)

                self.nextWord = Button(self.master, text = "Next Word", command = self.buttonOne)
                self.nextWord.grid(row = 2, column = 2)

                self.replayWord = Button(self.master, text = "Replay Word", command = self.buttonTwo)
                self.replayWord.grid(row = 2, column = 3)

                self.submit = Button(self.master, text = "Submit Answer", command = self.buttonThree)
                self.submit.grid(row = 3, column = 2, columnspan = 2)

        def play(self):
                self.gui()

        def buttonOne(self):
                self.current_word += 1
                self.current_led = self.leds[self.current_led]
                print 'Current word: {}'.format(self.current_word)
                print 'Current question: {}'.format(self.current_question)
                self.runQuestion()

        def buttonTwo(self):
                print 'Current word: {}'.format(self.current_word)
                print 'Current question: {}'.format(self.current_question)
                self.runQuestion()

        def buttonThree(self):
                if not self.answering:
                        print "The question hasen't been fully asked yet."
                        return
                # todo check if answer is correct
                self.current_question += 1
                self.current_word = -1
                print 'Ayy you got it wrong dumbass, next question.'
                self.answering = False

        
        def runQuestion(self):
                words = self.questions[self.current_question].split(' ')
                if (len(words)-1) < self.current_word:
                        print 'This is the end of the question its time to answer.'
                        return
                #GPIO.output(current_led, True)
                for n in words[self.current_word]:
                        if n != '/':
                                self.blink(n, self.current_led)
                        else:
                                sleep(UNIT*3)
                                print 'end of character'
                #GPIO.output(current_led, False)
                if (len(words)-1) == self.current_word:
                        self.answering = True
                        

        # Handles the blinking duration and led
        def blink(self, length, current_led):
                if length in self.morse:
                        print 'light {}, {}'.format(length, current_led)
                        #GPIO.output(current_led, True)
                        sleep(self.morse[length])
                        #GPIO.output(current_led, False)
                        #sleep(UNIT)
                else:
                        print 'blink.error({}, {})'.format(length, current_led)

        def timerstuff(self):
                pass

# Constants // assuming the green led is for every other word
RED = 12
GREEN = 17
RGB_RED = 22
RGB_GREEN = 21
RGB_BLUE = 4
REPEAT = 6
NEXT_WORD = 26
UNIT = .2

# GPIO stuffs
#GPIO.setmode(GPIO.BCM)

#GPIO.setup(red, GPIO.OUT)
#GPIO.setup(green, GPIO.OUT)

#GPIO.setup(repeat, GPIO.IN, GPIO.PUD_DOWN)
#GPIO.setup(next_word, GPIO.IN, GPIO.PUD_DOWN) 

window = Tk()
window.title("Space with Tyson")
window.geometry("400x300")
f = Game(window)
f.play()
window.mainloop()
