from tkinter import *
from game import *
import time
import pickle


def destroy():
    root.destroy()


def play():

    global score
    score = game()

    if score > pickle.load(open("score.pickle", "rb")):
        pickle.dump(score, open("score.pickle", "wb"))
    else:
        pass

    entry.configure(state="normal")
    entry.delete(0, END)
    entry.insert(1, pickle.load(open("score.pickle", "rb")))
    entry.configure(state="disabled")

    currentScore.configure(state="normal")
    currentScore.delete(0, END)
    currentScore.insert(1, score)
    currentScore.configure(state="disabled")

    time.sleep(3)

    destroy()


root = Tk()

text = Text(root, height=1, width=12)
text.pack()
text.insert(END, "High Score:")
text.configure(state="disabled")

entry = Entry(root)
entry.pack()
entry.delete(0, END)
entry.insert(1, pickle.load(open("score.pickle", "rb")))
entry.configure(state="disabled")

text = Text(root, height=1, width=14)
text.pack()
text.insert(END, "Current Score:")
text.configure(state="disabled")

currentScore = Entry(root)
currentScore.pack()
currentScore.delete(0, END)
currentScore.insert(1, 0)
currentScore.configure(state="disabled")

button = Button(root, text="Play",command=play)
button.pack()

root.mainloop()
