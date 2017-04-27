###############################################################################################################################
#Collaborators: Jordan Edgel, Kaleb Rhody, Thomas Presicci, Alex Reed
#Description: A series of trivia questions asked entirely in Morse Code to be solved by competitors. Players are scored by time.
#Due Date: May 10, 2017
###############################################################################################################################
from time import *
#import pygame
#import RPi.GPIO as GPIO
from Tkinter import *

class Game(Canvas):
        def __init__(self, master):
                self.master = master
                Canvas.__init__(self,master)
                master.columnconfigure(0, weight = 1)
                master.rowconfigure(0, weight = 1)

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

                self.qNumber = Label(self.master, text = "Question #", state = DISABLED)
                self.qNumber.grid(row = 1, column = 2, columnspan = 2, sticky = N+W)

                self.nextWord = Button(self.master, text = "Next Word")
                self.nextWord.grid(row = 2, column = 2)

                self.replayWord = Button(self.master, text = "Replay Word")
                self.replayWord.grid(row = 2, column = 3)

                self.submit = Button(self.master, text = "Submit Answer")
                self.submit.grid(row = 3, column = 2, columnspan = 2)

        def play(self):
                self.gui()
        
        def morsestuff(self):
                pass

        def ledstuff(self):
                pass

        def timerstuff(self):
                pass
        
        

window = Tk()
window.title("Space with Tyson")
window.geometry("400x300")
f = Game(window)
f.play()
window.mainloop()
