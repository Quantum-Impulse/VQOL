import os
import sys
import time
from tkinter import *

sys.path.insert(1, os.path.join(os.getcwd(), 'MainFiles'))
path = os.getcwd()
exampPath = os.path.join(path, 'Experiments')
first = True
# get what file the user wants to run in VQOL
while True:
    try:
        if len(sys.argv) > 1 and first:
            fileName = sys.argv[1]
            first = False
        else:
            fileName = input('Enter the experiment you want to run: ')
        fileName = fileName.partition('.')[0] + '.txt'
        fileName = os.path.join(exampPath, fileName)
        print(fileName)
        file = open(fileName, 'r')
    except:
        print("That is not a valid file, please try again.")
        print()
        continue
    else:
        break
print()
print('Starting VQOL....')
print()

# moved down here for the exe
import Canvas
if __name__== '__main__':
    Canvas.root.geometry("+%d+%d" % (Canvas.w, Canvas.h))
    c = Canvas.MyCanvas(Canvas.root, fileName, debugMode = False, noNoise=False)
    if c.noVisMode:
        #for i in range(3):
        #c.refresh()
        #c.quit()
        c.on()
    else:
        Canvas.root.lift()
        Canvas.root.mainloop()
    # Canvas.root.lift()
    # Canvas.root.mainloop()

