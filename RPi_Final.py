###############################################################################################################################
#Collaborators: Jordan Edgel, Kaleb Rhody, Thomas Presicci, Alex Reed
#Description: A series of trivia questions asked entirely in Morse Code to be solved by competitors. Players are scored by time.
#Due Date: May 10, 2017
###############################################################################################################################
from time import *
import pygame
import RPi.GPIO as GPIO
from Tkinter import *
import threading

# Dot = one unit / Dash = three units
# Space between digits = one unit
# Space between characters = three units
# Space between words = seven units

# Delete last word = eight dots

class Help(Canvas):
        def __init__(self, master):
                self.master = master
                Canvas.__init__(self, master)
                master.columnconfigure(0, weight = 1)
                master.rowconfigure(0, weight = 1)
                
                self.helpText = ""
                
        def gui(self):
                self.grid()
                self.helpLabel = Label(self.master, textvariable = self.helpText)
                self.helpLabel.grid (row = 0, column = 0)
                
class ScoreScreen(Canvas):
        def __init__(self, master, a):
                self.master = master
                Canvas.__init__(self, master)
                master.columnconfigure(0, weight = 1)
                master.rowconfigure(0, weight = 1)
                
                self.scoreText = "You scored: {}".format(a)
        
        def gui(self):
                self.grid()
                
                self.scoreLabel = Label(self.master, text = self.scoreText)
                self.scoreLabel.grid(row = 0, column = 0)
                

class Game(Canvas):
        def __init__(self, master):
                self.master = master
                Canvas.__init__(self,master)
                master.columnconfigure(0, weight = 1)
                master.rowconfigure(0, weight = 1)
                
                # List of questions in form of dots and dashes
                self.questions = ['.--/..../../-.-./.... .-./---/...-/./.-. .--/.-/... -/..../. ..-./../.-./.../- -/--- ./-..-/.--./.-../---/.-./. --/.-/.-./...', # Question 1, [Which rover was the first to explore Mars? - Sojourner]
                             '..../---/.-- --/..-/-.-./.... -/../--/. -../---/./... .- .../..-/-. .-./.-/-.-- -/.-/-.-/. -/--- -/.-./.-/...-/./.-.. -/--- ./.-/.-./-/....', # Question 2, [How much time does a sun ray take to travel to Earth? - 8 minutes]
                             '--/../.-../-.-/-.-- .--/.-/-.-- -.../.-../.-/-.-./-.- ..../---/.-../. -../../.../-/.-/-./-.-./. ../-. .-../../--./..../- -.--/./.-/.-./...', # Question 3, [Milky Way black hole distance in light years? - 27,000 light years]
                             '.--/..../.-/- ../... -/..../. .../..-/-. --/---/.../-/.-../-.-- --/.-/-../. ---/..-.'] # Question 4, [What is the sun mostly made of? - Hydrogen]

                #self.questions = ['.','-','.','-']
                
                # Dict for the times of each dot and dash
                self.morse = {'-':UNIT*3, '.':UNIT}

                # Used to switch the LED the word is displayed on
                self.leds = {RED:GREEN, GREEN:RED}
                
                # Initialized variables
                self.time = StringVar()
                self.current_question = 0
                self.current_word = -1
                self.current_led = RED
                self.answering = False
                self.atext = StringVar()
                self.btext = StringVar()
                self.ctext = StringVar()
                self.dtext = StringVar()
                self.setText()
                self.score = 0
                self.penalty = 0

        def gui(self):
                self.grid()
                
                img = PhotoImage( file = "Neil.gif" )
                pic = Label(self.master, image = img)
                pic.image = img
                pic.grid(row = 0, column = 0, sticky = E+W)

                self.ansA = Radiobutton(self.master, textvariable = self.atext, value = 1, variable = ansvar, width = 10)
                self.ansA.grid(row = 1, column = 0)
                self.ansB = Radiobutton(self.master, textvariable = self.btext, value = 2, variable = ansvar, width = 10)
                self.ansB.grid(row = 2, column = 0)
                self.ansC = Radiobutton(self.master, textvariable = self.ctext, value = 3, variable = ansvar, width = 10)
                self.ansC.grid(row = 1, column = 1)
                self.ansD = Radiobutton(self.master, textvariable = self.dtext, value = 4, variable = ansvar, width = 10)
                self.ansD.grid(row = 2, column = 1)
                
                self.helpButton = Button(self.master, text = "help", command = self.helpWindow, width = 25)
                self.helpButton.grid(row = 0, column = 2, rowspan = 2, sticky = E+W)

                self.timer = Label(self.master, textvariable = self.time, state = DISABLED)
                self.timer.grid(row = 2, column = 2, columnspan = 2, sticky = W)

                self.qNumber = Label(self.master, text = "Question # {}".format(self.current_question + 1), state = DISABLED)
                self.qNumber.grid(row = 3, column = 2, columnspan = 2, sticky = N+W)

                self.submit = Button(self.master, text = "Submit Answer", command = self.buttonThree)
                self.submit.grid(row = 4, column = 2, columnspan = 2)

        def play(self):
                self.setText()
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
                self.checkAns(ansvar.get())
                
        def helpWindow(self):
                helpW = Tk()
                helpW.title("Space with Tyson HELP")
                helpW.geometry("300x400")
                a = Help(helpW)
                helpW.mainloop()
                
        
        def runQuestion(self):
                GPIO.output(RGB_BLUE, False)
                words = self.questions[self.current_question].split(' ')
                if (len(words)-1) < self.current_word:
                        GPIO.output(RGB_BLUE, True)
                        print 'This is the end of the question its time to answer.'
                        return
                GPIO.output(RGB_RED, False)
                GPIO.output(RGB_GREEN, True)
                for n in words[self.current_word]:
                        if n != '/':
                                self.blink(n, self.current_led)
                        else:
                                sleep(UNIT*3)
                                print 'end of character'
                GPIO.output(RGB_GREEN, False)
                GPIO.output(RGB_RED, True)
                if (len(words)-1) == self.current_word:
                        self.answering = True
                        

        # Handles the blinking duration and led
        def blink(self, length, current_led):
                if length in self.morse:
                        print 'light {}, {}'.format(length, current_led)
                        GPIO.output(current_led, True)
                        sleep(self.morse[length])
                        GPIO.output(current_led, False)
                        sleep(UNIT)
                else:
                        print 'blink.error({}, {})'.format(length, current_led)

        def setText(self):
                if (self.current_question == 0):
                        self.atext.set("Sojourner")
                        self.btext.set("Curiosity")
                        self.ctext.set("MER")
                        self.dtext.set("Prop-M")
                elif (self.current_question == 1):
                        self.atext.set("20 minutes")
                        self.btext.set("1 minute")
                        self.ctext.set("8 minutes")
                        self.dtext.set("40 minutes")
                elif (self.current_question == 2):
                        self.atext.set("10,000 light years")
                        self.btext.set("27,000 light years")
                        self.ctext.set("15,000 light years")
                        self.dtext.set("45,000 light years")
                elif (self.current_question == 3):
                        self.atext.set("Carbon")
                        self.btext.set("Water")
                        self.ctext.set("Iron")
                        self.dtext.set("Hydrogen")

        def checkAns(self, var):
                if (self.current_question == 0):
                        if (var == 1):
                                print "Correct Answer!"
                                self.current_question += 1
                                self.current_word = -1
                                self.answering = False
                                self.setText()
                                self.gui()
                        else:
                                print "Wrong Answer!"
                                self.penalty += 30

                elif (self.current_question == 1):
                        if (var == 3):
                                print "Correct Answer!"
                                self.current_question += 1
                                self.current_word = -1
                                self.answering = False
                                self.setText()
                                self.gui()
                        else:
                                print "Wrong Answer!"
                                self.penalty += 30

                elif (self.current_question == 2):
                        if (var == 2):
                                print "Correct Answer!"
                                self.current_question += 1
                                self.current_word = -1
                                self.answering = False
                                self.setText()
                                self.gui()
                        else:
                                print "Wrong Answer!"
                                self.penalty += 30

                elif (self.current_question == 3):
                        if (var == 4):
                                print "Correct Answer!"
                                self.current_question += 1
                                self.current_word = -1
                                self.answering = False
                                self.setText()
                                self.gui()
                                s = score(self.score, self.penalty)
                                print s
                                showScore(s)
                        else:
                                print "Wrong Answer!"
                                self.penalty += 30

        def updateTime(self, a):
                self.time.set("Time: " + str(a) + " sec")
                self.score += 1

def score(t, penalty):
        playing = False
        return t+penalty

def timer():
        t = 0
        while(playing == True):
                t += 1
                f.updateTime(t)
                sleep(1)
                
def buttonReader():
        while (True):
                input_state = GPIO.input(REPEAT)
                if (input_state == 1):
                        f.buttonTwo()
                input_state = GPIO.input(NEXT_WORD)
                if (input_state == 1):
                        f.buttonOne()
                sleep(.1)
        
def showScore(c):
        scoreWindow = Tk()
        scoreWindow.title("Space with Tyson SCORE")
        scoreWindow.geometry("300x500")
        
        s = ScoreScreen(scoreWindow, c)
        scoreWindow.mainloop()

# Constants // assuming the green led is for every other word
RED = 12
GREEN = 17
RGB_RED = 22
RGB_GREEN = 21
RGB_BLUE = 4
REPEAT = 6
NEXT_WORD = 26
UNIT = .2

playing = True
penalty = 0
time = threading.Thread(target = timer)
time.deamon = True
buttonRead = threading.Thread(target = buttonReader)
buttonRead.deamon = True

# GPIO stuffs
GPIO.setmode(GPIO.BCM)

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(RGB_RED, GPIO.OUT)
GPIO.setup(RGB_GREEN, GPIO.OUT)
GPIO.setup(RGB_BLUE, GPIO.OUT)

GPIO.setup(REPEAT, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(NEXT_WORD, GPIO.IN, GPIO.PUD_DOWN) 

window = Tk()
ansvar = IntVar()
window.title("Space with Tyson")
window.geometry("600x500")
f = Game(window)
f.play()
time.start()
buttonRead.start()
window.mainloop()
