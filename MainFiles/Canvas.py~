# -----------COPYRIGHT NOTICE STARTS WITH THIS LINE------------
# Copyright (c) 2019, Applied Research Laboratories, The University of Texas
# at Austin. All rights reserved.  By using this software, you, the USER,
# indicate you have read, understood, and will comply with the following:
#
# Nonexclusive permission to use, copy and/or modify this software for
# internal, noncommercial, research purposes is granted. Any distribution,
# including commercial sale, of this software, copies, associated documentation
# and/or modifications is strictly prohibited without the prior written
# consent of the Applied Research Laboratories, The University of Texas at
# Austin (ARL:UT).  Appropriate copyright notice shall be placed on software
# copies, and a full copy of this license in associated documentation.  No
# right is granted to use in advertising, publicity or otherwise any
# trademark of ARL:UT.  This software is provided "as is," and ARL:UT makes
# no representations or warranties, express or implied, including those of
# merchantability or fitness for a particular purpose, or that use of the
# software, modifications, or associated documentation will not infringe on
# any patents, copyrights, trademarks or other rights.  ARL:UT shall not be
# held liable for any liability nor for any direct, indirect or consequential
# damages with respect to any claim by USER or any third party on account of
# or arising from this Agreement.  Submit software questions to:
#
# Brian R. La Cour
# Applied Research Laboratories, The University of Texas at Austin
# P.O. Box 8029
# Austin, Texas 78713-8029
# blacour@arlut.utexas.edu
# -----------COPYRIGHT NOTICE ENDS WITH THIS LINE------------


# import tkinter as tk
from tkinter import *
from tkinter import PhotoImage
# import PySimpleGUI as sg
from PIL import Image
from re import split
import os
from csv import writer
import Components

root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = screen_width + 400
height = screen_height - 100
w = screen_width / 2 - width / 2 + 300
h = 0
#root.resizable(0,0)
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# w = screen_width/2 - width/2
# h = 0
# step = 1e-6
imgPath = os.path.join(os.getcwd(), 'MainFiles')
imgPath = os.path.join(imgPath, 'Images')
# these are variables used throughout the program
def set():
    global scFac, delay, pause, on, stop, stepMode, kill, slowMo, wentBack, detectors, conCounters,\
        deletedWaves, numSeconds, totSeconds, FileName, experiment, timeStamps, step, ran
    scFac = 50
    delay = 1
    pause = False
    on = False
    stop = False
    stepMode = False
    kill = False
    slowMo = False
    wentBack = False
    detectors = []
    conCounters = []
    deletedWaves = []
    numSeconds = 0
    totSeconds = 0
    experiment = 1
    timeStamps = []
    FileName = None
    ran = False
    step = 1e-6


class MyCanvas(Canvas):

    def __init__(self, master, textFile, debugMode = False, noNoise = False, onlyNoise = False, test = False):
        set()
        global FileName, timeStamps
        self.noVisMode = False
        FileName = textFile
        self.debug = debugMode
        self.timeStamps = timeStamps
        self.noNoise = noNoise
        self.onlyNoise = onlyNoise
        self.test = test # used to run testing script
        self.root = root
        root.protocol("WM_DELETE_WINDOW", self.quit)
        super().__init__(master, width=width, height=height, bg="whitesmoke", highlightthickness=0, relief="ridge")
        self.master = master
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        l = Label(self,
                  text="Welcome to the Virtual Quantum Optics Laboratory                                Copyright (c) 2019 ARL:UT.  All rights reserved.",
                  font=("Helvetica", 10))
        l.grid(column=0, row=0, columnspan=2, sticky=E + W)

        self.legend = ScrollableFrame(self)
        # laser
        self.laser_frame = Frame(self.legend.scrollable_frame, width=135, height=170)
        exp = Label(self.laser_frame, text='Experiment Controls', bg='#ced1d6', fg='black', height=1,
                    font=("Helvetica", 10), relief='groove')
        exp.grid(column=0, row=0, columnspan=2, sticky=W + E)
        # on off pause bottons for laser
        self.playB = PhotoImage(file=os.path.join(imgPath,'PlayButton.png'))
        self.onBut = Button(self.laser_frame, text='Start', image=self.playB, compound=LEFT, command=self.on,
                            bg='#ced1d6',
                            pady=0, font=("Helvetica", 9))
        self.onBut.grid(column=0, row=1, columnspan=2, sticky=W + E)
        self.pauseB = PhotoImage(file=os.path.join(imgPath,'PauseButton.png'))
        self.pauseBut = Button(self.laser_frame, text="Pause", compound=LEFT, image=self.pauseB, command=self.pause,
                               bg='#ced1d6',
                               pady=0, font=("Helvetica", 9))
        self.pauseBut.grid(column=0, row=2, columnspan=2, sticky=W + E)
        self.stopB = PhotoImage(file=os.path.join(imgPath,'Stop.png'))
        self.stopBut = Button(self.laser_frame, text="Stop", compound=LEFT, image=self.stopB, command=self.stop,
                              bg='#ced1d6', pady=0, font=("Helvetica", 9))
        self.stopBut.grid(column=0, row=3, columnspan=2, sticky=W + E)
        # self.noVisBut = Button(self.laser_frame, text = "No Visual", compound = LEFT, command = self.noVis, bg='#ced1d6',
        #                        pady=0, font=("Helvetica", 9))
        # self.noVisBut.grid(column = 0, row = 4, columnspan = 2, sticky = W + E)

        # step mode and step forward
        self.stepModeBut = Button(self.laser_frame, text="Step by step mode", fg="black", bg='#ced1d6',
                        font=("Helvetica", 9),  pady=0, command=self.stepMode)
        self.stepModeBut.grid(column=0, row=5, columnspan=2,  sticky=W+E)
        self.stepFB = PhotoImage(file=os.path.join(imgPath,'SkipForward.png'))
        self.stepFBut = Button(self.laser_frame, text="Forward", compound=LEFT, image=self.stepFB, command=self.stepForward, bg='#ced1d6', pady=0)
        self.stepFBut.grid(column=0, row=6,  sticky=W+E)
        self.slowB = PhotoImage(file=os.path.join(imgPath,'SlowMotion.png'))
        self.slow = Button(self.laser_frame, text="Slow Motion", compound=LEFT, image=self.slowB, command=self.slowMotion,
                               bg='#ced1d6',  pady=0, font=("Helvetica", 9))
        self.slow.grid(column=0, row=7, columnspan=2,  sticky=W+E)
        self.refreshB = PhotoImage(file=os.path.join(imgPath,'Refresh.png'))
        self.refreshBut = Button(self.laser_frame, text="Refresh", compound=LEFT, image=self.refreshB, command=self.refresh,
                           bg='#ced1d6', pady=0, font=("Helvetica", 9))
        self.refreshBut.grid(column=0, row=8, columnspan=2,  sticky=W+E)
        # back in time step buttons
        self.stepBB = PhotoImage(file=os.path.join(imgPath,'SkipBack.png'))
        self.stepBBut = Button(self.laser_frame, text="Backward", compound=LEFT, image=self.stepBB, command=self.stepBack,
                               bg='#ced1d6', pady=0)
        self.stepBBut.grid(column=1, row=6, sticky=W+E)
        self.laser_frame.grid(column=1,row=1, sticky=N+S+E+W)

        # Code for key image
        self.key = PhotoImage(file=os.path.join(imgPath, 'KeyFinal.png'))
        self.img = Label(self.legend.scrollable_frame, image=self.key)
        self.img.grid(column = 1, row = 3, sticky = W + E)

        # polarization key
        self.polar_key = Frame(self.legend.scrollable_frame, width=135)
        keyLabel = Label(self.polar_key, text="Key for Polarizations", bg="#242426", fg='white',  height=1,
                         font=("Helvetica", 10), width = 17, padx = 2)
        keyLabel.grid(column=0, row=0, sticky=W + E)
        b1Horz = Label(self.polar_key, text="Horizontal Mode", fg="red", bg="#242426",  height=1,
                       font=("Helvetica", 10))
        b1Horz.grid(column=0, row=1, sticky=W + E)
        b2Vert = Label(self.polar_key, text="Vertical Mode", fg="#3336ff", bg="#242426", height=1,
                       font=("Helvetica", 10))
        b2Vert.grid(column=0, row=2, sticky=W + E)
        b3Diag = Label(self.polar_key, text="Diagonal Mode", fg="gold", bg="#242426", height=1,
                       font=("Helvetica", 10))
        b3Diag.grid(column=0, row=3, sticky=W + E)
        b4Anti = Label(self.polar_key, text="Anti-Diagonal Mode", fg="limegreen", bg="#242426", height=1,
                       font=("Helvetica", 10))
        b4Anti.grid(column=0, row=4, sticky=W + E)
        b5Right = Label(self.polar_key, text="Right Circular Mode", fg="darkorange2", bg="#242426", height=1,
                        font=("Helvetica", 10))
        b5Right.grid(column=0, row=5, sticky=W + E)
        b6Left = Label(self.polar_key, text="Left Circular Mode", fg="purple2", bg="#242426", height=1,
                       font=("Helvetica", 10), padx = 4)
        b6Left.grid(column=0, row=6, sticky=W + E)
        self.polar_key.grid(column=1,row=2, sticky=N + S + E + W)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=0)

        self.legend.grid(column = 1, row = 1)

        # grid
        grid_width = Components.WIDTHB
        grid_height = Components.HEIGHTB
        self.grid_frame = Frame(self, width=height, height=height, bd=0, bg="blue", highlightthickness=0)
        self.grid_frame.grid(column=0, row=1, rowspan=3, sticky=N + S + E + W)
        self.grid = Canvas(self.grid_frame, width=height, height=height - 200, bg="whitesmoke", bd=0, relief="ridge",
                           scrollregion=(0, 0, 50 * grid_width, 50 * grid_height), highlightthickness=0)
        hbar = Scrollbar(self.grid_frame, orient=HORIZONTAL)
        hbar.pack(side=BOTTOM, fill=X)
        hbar.config(command=self.grid.xview)
        vbar = Scrollbar(self.grid_frame, orient=VERTICAL)
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=self.grid.yview)
        self.grid.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        for j in range(grid_height):
            for i in range(grid_width):
                self.grid.create_rectangle(i * 50, 0 + 50 * j, i * 50 + 50, 50 + 50 * j, fill="#b9bdc4")
        self.grid.pack(fill=BOTH, expand=YES)

        # arrays used to keep track of the components and waves
        global detectors
        self.waveSegs = []  # keeps track of laser objects
        self.waveVis = []  # keeps track of laser objects representation on the Canvas
        self.comps = []
        self.lasers = []
        self.splitCheckWaves = []
        self.splitCheckVis = []
        self.detectors = detectors
        self.powerMeters = []
        self.beamblockers = []
        self.conCounters = conCounters
        self.beamSplitters = []
        self.deleteRoundEdge = []
        self.deleteRoundBlocked = []
        self.deleteOverallEdge = []
        self.deleteOverallBlocked = []
        self.blocking = []
        self.addtag_all("all")
        root.lift()
        self.parseFile(textFile)
        # countdown
        if (totSeconds != None):
            time, unit = self.unit(totSeconds)
            self.countLabel = Label(self.laser_frame, text='Time Left: ' + ('%2.1f ' % time) + unit, bg='#ced1d6',
                                    fg='black',
                                    height=1, font=("Helvetica", 10), relief='groove')
        else:
            self.countLabel = Label(self.laser_frame, text='No time limit set', bg='#ced1d6', fg='black',
                                    height=1, font=("Helvetica", 10), relief='groove')
        self.countLabel.grid(column=0, row=9, columnspan=2, sticky=W + E)
        self.pack(fill=BOTH, expand=YES)
        # if self.test or self.noVisMode:
        #     self.on()

    def noVis(self):
        global on, stop
        if self.noVisMode == False and stop == False and on == False:
            self.noVisMode = True
            self.noVisBut.configure(relief='sunken')
        elif on == False and self.noVisMode == True and stop == False:
            self.noVisMode = False
            self.noVisBut.configure(relief = 'raised')

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.legend.canvas.config(height = self.height - 50)
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)

    def parseFile(self, fileName):
        global totSeconds
        totSeconds = None
        path = os.getcwd()
        resultFile = 'result.csv'
        keyWords = ['mode', 'x', 'y', 'orientation', 'reflectivity', 'strength', 'phase', 'indexDetOne', 'indexDetTwo',
                    'dark_count_rate', 'angle', 'phase', 'angle', 'strength', 'entanglement_type', 'power', 'emitAngle', 'basis',
                    'probability_dark_count', 'delay']
        components = ['laser', 'led', 'entanglementsource', 'mirror', 'neutraldensityfilter', 'polarizer', 'phasedelay', 'quarterwaveplate',
                      'halfwaveplate', 'beamsplitter', 'polarizingbeamsplitter', 'singlemodefiber', 'powermeter', 'detector', 'coincidencecounter',
                      'beamblocker', 'rotator', 'phaseretarder', 'depolarizer', 'dephaser', 'timedelay']
        file = open(fileName, 'r')
        line_list = [l for l in (line.strip() for line in file) if l]
        for line in line_list:
            keyWord = False
            line = "".join(line.split())
            if len(line) != 1 and line[0] != '#':
                comp = []
                line = line.partition('#')[0]
                line = line.rstrip()
                for word in split('=|,', line):
                    word = word.lower().strip()
                    comp.append(word)
                    if word in keyWords and (comp[0] != 'laser' or word != 'optical_density'):
                        keyWord = True
                if not (comp[0] in components or comp[0] == 'num_seconds' or comp[0] == 'file_name' or comp[0] == 'offline_mode'):
                    print("error at line: " + line)
                    raise ValueError('There is no component of type', comp[0],
                                     'nor is this a special command. Please check your'
                                     ' spelling and try again')
                # print(comp)
                if comp[0] in components:
                    compType = components.index(comp[0])
                    if not keyWord:
                        self.nonKeywordDef(comp, compType)
                    else:
                        self.keywordDef(comp, compType)
                if comp[0] == 'file_name':
                    resultFile = comp[1]
                if comp[0] == 'num_seconds':
                    totSeconds = float(comp[1])
                if comp[0] == 'offline_mode':
                    if comp[1] == 'true':
                        self.noVisMode = True
                    else:
                        self.noVisMode = False
        path = os.path.join(path, 'Results')
        if self.noVisMode and totSeconds == None:
            raise ValueError("You need to give a time limit if you are going to run in offline mode")

        self.csvFilename = os.path.join(path, resultFile)

    def unit(self, time):
        unit = 's'
        # print(self._power)
        if time < 0.01e-9:
            time = 0
            unit = 'ns'
        elif time < 1e-6:
            time /= 1e-9
            unit = 'ns'
        elif time < 1e-3:
            time /= 1e-6
            unit = 'μs'
        elif time < 1:
            time /= 1e-3
            unit = 'ms'
        return time, unit

    def keywordDef(self, comp, compType):
        if compType == 0:
            words = ['laser', 'x', 'y', 'orientation', 'mode', 'power']
            res = ['laser', 0, 0, 0, 'h', 4e-3]
        elif compType == 1:
            words = ['led', 'x', 'y', 'orientation', 'power']
            res = ['led', 0, 0, 0, 4e-3]
        elif compType == 2:
            words = ['entanglementsource', 'x', 'y', 'orientation', 'strength', 'phase', 'entanglement_type', 'directions']
            res = ['entanglementsource', 0, 0, 90, 1, None, 1, "LR"]
        elif compType == 3:
            words = ['mirror', 'x', 'y', 'orientation']
            res = ['mirror', 0, 0, 0]
        elif compType == 4:
            words = ['neutraldensityfilter', 'x', 'y', 'orientation', 'optical_density']
            res = ['neutraldensityfilter', 0, 0, 0, 10]
        elif compType == 5:
            words = ['polarizer', 'x', 'y', 'orientation', 'angle', 'phase']
            res = ['polarizer', 0, 0, 0, 0, 0]
        elif compType == 6:
            words = ['phasedelay', 'x', 'y', 'orientation', 'phase']
            res = ['phasedelay', 0, 0, 0, 0]
        elif compType == 7:
            words = ['quarterwaveplate', 'x', 'y', 'orientation', 'angle']
            res = ['quarterwaveplate', 0, 0, 0, 0]
        elif compType == 8:
            words = ['halfwaveplate', 'x', 'y', 'orientation', 'angle']
            res = ['halfwaveplate', 0, 0, 0, 0]
        elif compType == 9:
            words = ['beamsplitter', 'x', 'y', 'orientation', 'reflectivity']
            res = ['beamsplitter', 0, 0, 0, 0.5]
        elif compType == 10:
            words = ['polarizingbeamsplitter', 'x', 'y', 'orientation', 'basis']
            res = ['polarizingbeamsplitter', 0, 0, 0, "HV"]
        # elif compType == 11:
        #     words = ['singlemodefiber', 'x_start', 'y_start', 'x_stop', 'y_stop', 'orientation_start', 'orientation_stop']
        #     res = ['singlemodefiber', 0, 0, 1, 1, 0, 0]
        elif compType == 12:
            words = ['powermeter', 'x', 'y']
            res = ['powermeter', 0, 0]
        elif compType == 13:
            words = ['detector', 'x', 'y', 'orientation', 'dark_count_rate', 'probability_dark_count']
            res = ['detector', 0, 0, 0, 1, -1]
        elif compType == 14:
            words = ['coincidencecounter', 'detector_one', 'detector_two']
            res = ['coincidencecounter', 1, 2]
        elif compType == 15:
            words =  ['beamblocker', 'x', 'y']
            res = ['beamblocker', 0, 0]
        elif compType == 16:
            words = ['rotator', 'x', 'y', 'orientation', 'angle']
            res = ['rotator', 0, 0, 0, 0]
        elif compType == 17:
            words = ['phaseretarder', 'x', 'y', 'orientation', 'phase']
            res = ['phaseretarder', 0, 0, 0, 0]
        elif compType == 18:
            words = ['depolarizer', 'x', 'y', 'orientation']
            res = ['depolzarizer', 0, 0, 0]
        elif compType == 19:
            words = ['dephaser', 'x', 'y', 'orientation']
            res = ['dephaser', 0, 0, 0]
        elif compType == 20:
            words = ['timedelay', 'x', 'y','orientation', 'delay']
            res = ['timedelay', 0, 0, 0, 0]
        self.keywrdHelp(words, comp, res)
        self.nonKeywordDef(res, compType)

    def keywrdHelp(self, words, comp, res):
        ind = 1
        while ind < len(comp):
            word = comp[ind]
            ind += 1
            try:
                spot = words.index(word)
            except:
                raise ValueError("There was an error when reading keywords. There is not a param " + word + " for a "
                                                                             + comp[0] + ". Your options are " + str(words))
            try:
                res[spot] = comp[ind]
                ind += 1
            except:
                raise ValueError("Please be sure that when you use keyword initialization that there is a keyword"
                                 " followed by its value. There was an error at " + comp[0])

    def nonKeywordDef(self, comp, compType):
        if len(comp) < 2:
            raise ValueError("You do not have enough parameters for the components: " + str(comp[0]))
        try:
            x = int(comp[1])
            y = int(comp[2])
        except ValueError:
            raise ValueError("Your first two parameters must be ints for a " + comp[0])
        if compType != 12 and compType != 14 and compType != 11:
            if len(comp) > 3:
                try:
                    orientation = int(comp[3])
                except ValueError:
                    raise ValueError("Orientation must be a int for a " + comp[0])
            # laser
        if compType == 0:
            if len(comp) < 3 or len(comp) > 6:
                raise ValueError("You do not have the correct number of parameters for a laser. You must"
                                 "at least have 2 parameters and at most 4, you have: " + str((len(comp) - 1)))
            # user is using two defauls
            if len(comp) == 3:
                Components.Laser(self, x, y)
            # user is using one default
            elif len(comp) == 4:
                Components.Laser(self, x, y, orientation)
            # user is not using any default paramas
            mode = comp[4]
            if len(comp) == 5:
                Components.Laser(self, x, y, orientation, mode)
            elif len(comp) == 6:
                try:
                    power = float(comp[5])
                except ValueError:
                    raise ValueError("The power for an laser source must be a double")
                Components.Laser(self, x, y, orientation, mode, power)

            # LED
        elif compType == 1:
            if len(comp) < 3 or len(comp) > 5:
                raise ValueError("You do not have the correct number of parameters for an LED. You must"
                                 " have at least 2 parameters and at most 4, you have: " + str((len(comp) - 1)))
            # two defaults
            if len(comp) == 3:
                Components.LED(self, x, y)
            # one default
            elif len(comp) == 4:
                Components.LED(self, x, y, orientation)
            # no defaults
            else:
                try:
                    power = float(comp[4])
                except ValueError:
                    raise ValueError("The power for an LED source must be a double")
                Components.LED(self, x, y, orientation, power)
            # SPDC
        elif compType == 2:
            if len(comp) < 3 or len(comp) > 8:
                raise ValueError("You do not have the correct number of parameters for a SPDC. You must"
                                 " have at least 2 parameters and at most 6, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.EntanglementSource(self, x, y)
                return
            elif len(comp) == 4:
                Components.EntanglementSource(self, x, y, orientation)
                return
            strength = float(comp[4])
            if len(comp) == 5:
                Components.EntanglementSource(self, x, y, orientation, strength)
                return
            phase = float(comp[5])
            if len(comp) == 6:
                Components.EntanglementSource(self, x, y, orientation, strength, phase)
            if len(comp) == 7:
                entanglement_type = int(comp[6])
                Components.EntanglementSource(self, x, y, orientation, strength, phase, entanglement_type)
            if len(comp) == 8:
                entanglement_type = int(comp[6])
                directions = str(comp[7]).upper()
                Components.EntanglementSource(self, x, y, orientation, strength, phase, entanglement_type, directions)
            # Mirror
        elif compType == 3:
            if len(comp) == 3:
                Components.Mirror(self, x, y)
            else:
                Components.Mirror(self, x, y, orientation)
            # NeutralDensityFilter
        elif compType == 4:
            if len(comp) < 3 or len(comp) > 5:
                raise ValueError("You do not have the correct number of parameters for a NeutralDensityFilter. You must"
                                 " have between 2 and 4 parameters, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.NeutralDensityFilter(self, x, y)
            elif len(comp) == 4:
                Components.NeutralDensityFilter(self, x, y, orientation)
            else:
                try:
                    optical_density = float(comp[4])
                except:
                    raise ValueError("Your optical_density for a NeutralDensityFilter must be a double")
                if(optical_density < 0):
                    raise ValueError("You cannot have a negative value for optical density ")
                Components.NeutralDensityFilter(self, x, y, orientation, optical_density)
            # Polarizer
        elif compType == 5:
            if len(comp) < 3 or len(comp) > 6:
                raise ValueError("You do not have the correct number of parameters for a polarizer. You must"
                                 " have between 2 and 5 parameters, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.Polarizer(self, x, y)
            elif len(comp) == 4:
                Components.Polarizer(self, x, y, orientation)
            else:
                angle = int(comp[4])
                if len(comp) == 5:
                    Components.Polarizer(self, x, y, orientation, angle)
                if len(comp) == 6:
                    phase = int(comp[5])
                    Components.Polarizer(self, x, y, orientation, angle, phase)
            # PhaseDelay
        elif compType == 6:
            if len(comp) < 3 or len(comp) > 5:
                raise ValueError("You do not have the correct number of parameters for a Phase Delay."
                                 " You must have bewteen 2 and 4 parameters, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.PhaseDelay(self, x, y)
            elif len(comp) == 4:
                Components.PhaseDelay(self, x, y, orientation)
            else:
                try:
                    phase = int(comp[4])
                except:
                    raise ValueError("The phase for you phase delay must be an int")
                Components.PhaseDelay(self, x, y, orientation, phase)
            # QuarterWavePlate
        elif compType == 7:
            if len(comp) < 3 or len(comp) > 5:
                raise ValueError("You do not have the correct number of parameters for a Quarter Plate. You must"
                                 " have between 2 and 4 parameters, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.QuarterWavePlate(self, x, y)
            elif len(comp) == 4:
                Components.QuarterWavePlate(self, x, y, orientation)
            else:
                try:
                    angle = float(comp[4])
                except:
                    raise ValueError("You fast axis angle for a wave plate should be given in degrees as a double")
                Components.QuarterWavePlate(self, x, y, orientation, angle)
            # HalfWavePlate
        elif compType == 8:
            if len(comp) < 3 or len(comp) > 5:
                raise ValueError("You do not have the correct number of parameters for a HalfWavePlate. You must"
                                 " have between 2 and 4 parameters, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.HalfWavePlate(self, x, y)
            elif len(comp) == 4:
                Components.HalfWavePlate(self, x, y, orientation)
            else:
                try:
                    angle = float(comp[4])
                except:
                    raise ValueError(
                        "You fast axis angle for a wave plate should be given in degrees as a double")
                Components.HalfWavePlate(self, x, y, orientation, angle)
            # beamsplitter
        elif compType == 9:
            if len(comp) < 3 or len(comp) > 5:
                raise ValueError("You do not have the correct number of parameters for a BeamSplitter. You must"
                                 "have between 2 and 4 parameters, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.BeamSplitter(self, x, y)
            elif len(comp) == 4:
                if orientation % 90 != 0:
                    raise ValueError("You must pick an orientation that is a multiple of 90 for a BeamSplitter")
                Components.BeamSplitter(self, x, y, orientation)
            else:
                try:
                    reflectivity = float(comp[4])
                except:
                    raise ValueError("The value of your r^2 for a beam splitter should be given as a double")
                if orientation % 90 != 0:
                    raise ValueError("You must pick an orientation that is a multiple of 90 for a BeamSplitter")
                Components.BeamSplitter(self, x, y, orientation, reflectivity)
            # PolarizingBeamSplitter
        elif compType == 10:
            if len(comp) == 3:
                Components.PolarizingBeamSplitter(self, x, y)
            elif len(comp) == 4:
                if orientation % 90 != 0:
                    raise ValueError("You must pick an orientation that is a multiple of 90 for a PolarBeamSplitter")
                Components.PolarizingBeamSplitter(self, x, y, orientation)
            elif len(comp) == 5:
                basis = comp[4]
                Components.PolarizingBeamSplitter(self, x, y , orientation, basis)
            # SMF
        # elif compType == 11:
        #     if len(comp) != 7:
        #         raise ValueError("You do not have the correct number of parameters for a SMF. You must"
        #                          "have 6 parameters, you have: " + str((len(comp) - 1)))
        #     try:
        #         x_stop = int(comp[3])
        #         y_stop = int(comp[4])
        #         orientation_start = int(comp[5])
        #         orientation_stop = int(comp[6])
        #     except:
        #         print("Please check the type of the parameters for your SMF", sys.exc_info()[0])
        #         raise
        #     Components.SingleModeFiber(self, x, y, x_stop, y_stop, orientation_start, orientation_stop)
            # PowerMeter
        elif compType == 12:
            Components.PowerMeter(self, x, y)
            # Detector
        elif compType == 13:
            if len(comp) < 3 or len(comp) > 6:
                raise ValueError("You do not have the correct number of parameters for a detector. You must"
                                 " have between 2 and 5 parameters, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.Detector(self, x, y)
                return
            elif len(comp) == 4:
                Components.Detector(self, x, y, orientation)
                return
            try:
                dcr = float(comp[4])
            except:
                print(comp[4])
                raise ValueError("Your dark count rate for detectors must be given as a double")
            if len(comp) == 5:
                Components.Detector(self, x, y, orientation, dcr)
            elif len(comp) == 6:
                try:
                    pdc = float(comp[5])
                except:
                    raise ValueError("Your probability of a dark count for detectors must be given as a double")
                Components.Detector(self, x, y, orientation, dcr, pdc)
            # CoincidenceCounter
        elif compType == 14:
            Components.CoincidenceCounter(self, x, y)
        elif compType == 15:
            Components.BeamBlocker(self, x, y)
        elif compType == 16:
            if len(comp) < 3 or len(comp) > 5:
                raise ValueError("You do not have the correct number of parameters for a Rotator."
                                 " You must have bewteen 2 and 4 parameters, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.Rotator(self, x, y)
            elif len(comp) == 4:
                Components.Rotator(self, x, y, orientation)
            else:
                try:
                    angle = float(comp[4])
                except:
                    raise ValueError("Your angle for a Rotator must be a double")
                Components.Rotator(self, x, y, orientation, angle)
        elif compType == 17:
            if len(comp) < 3 or len(comp) > 5:
                raise ValueError("You do not have the correct number of parameters for a Phase Retarder."
                                 " You must have bewteen 2 and 4 parameters, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.PhaseRetarder(self, x, y)
            elif len(comp) == 4:
                Components.PhaseRetarder(self, x, y, orientation)
            else:
                try:
                    phase = int(comp[4])
                except:
                    raise ValueError("The phase for you phase retarder must be an int")
                Components.PhaseRetarder(self, x, y, orientation, phase)
        elif compType == 18:
            if len(comp) == 3:
                Components.Depolarizer(self, x, y)
            else:
                Components.Depolarizer(self, x, y, orientation)
        elif compType == 19:
            if len(comp) < 3 or len(comp) > 4:
                raise ValueError("You do not have the correct number of parameters for a Dephaser."
                                 " You must have bewteen 2 and 4 parameters, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.Dephaser(self, x, y)
            elif len(comp) == 4:
                Components.Dephaser(self, x, y, orientation)
        elif compType == 20:
            if len(comp) < 3 or len(comp) > 5:
                raise ValueError("You do not have the correct number of parameters for a time delay."
                                 " You must have bewteen 2 and 4 parameters, you have: " + str((len(comp) - 1)))
            if len(comp) == 3:
                Components.TimeDelay(self, x, y)
            elif len(comp) == 4:
                Components.TimeDelay(self, x, y, orientation)
            elif len(comp) == 5:
                try:
                    delay = int(comp[4])
                except:
                    raise ValueError("The delay must be a integer number you tried, " + str(comp[4]))
                Components.TimeDelay(self,x,y,orientation,delay)

    # re run the user file to see if they changed the components specified without closing the program
    def refresh(self):
        global FileName, w, h, root
        self.quit()
        Components.components = [[Components.Cmpnts(x, y) for x in range(Components.WIDTHB)] for y in range(Components.HEIGHTB)]
        root = Tk()
        root.geometry("+%d+%d" % (w, h))
        c = MyCanvas(root, FileName)
        # if c.noVisMode:
        #     c.on()
        # else:
        root.mainloop()

    def runOffline(self):
        global on, kill, stop, stepMode, numSeconds, totSeconds, pause, timeStamps
        while (totSeconds != None and numSeconds < totSeconds) or totSeconds == None:
            if kill:
                self.root.destroy()
            elif not (pause or stepMode or stop):
                numSeconds += step
                timeStamps.append(self.round())
                if totSeconds != None:
                    time, unit = self.unit(totSeconds - numSeconds)
                    self.countLabel.config(text='Time Left: ' + ('%2.1f ' % time) + unit)
                for laser in self.lasers:
                    laser.shoot(self)
                self.moveNoVis()
        while len(self.waveSegs) > 0:
            numSeconds += step
            timeStamps.append(self.round())
            self.moveNoVis()
        self.quit()
         # if (totSeconds != None and numSeconds < totSeconds) or totSeconds == None:
        #     if kill:
        #         self.root.destroy()
        #     elif not (pause or stepMode or stop):
        #         numSeconds += step
        #         timeStamps.append(self.round())
        #         if totSeconds != None:
        #             time, unit = self.unit(totSeconds - numSeconds)
        #             self.countLabel.config(text='Time Left: ' + ('%2.1f ' % time) + unit)
        #         for laser in self.lasers:
        #             laser.shoot(self)
        #         self.moveNoVis()
        #         self.after(delay, self.runOnLaser)

    # runs the wave
    def runOnLaser(self):
        global on, kill, stop, stepMode, numSeconds, totSeconds, pause, timeStamps
        if kill:
            self.root.destroy()
        elif not (pause or stepMode or stop):
            numSeconds += step
            timeStamps.append(self.round())
            if totSeconds != None:
                time, unit = self.unit(totSeconds - numSeconds)
                self.countLabel.config(text='Time Left: ' + ('%2.1f ' % time) + unit)
            for laser in self.lasers:
                laser.shoot(self)
            if not self.noVisMode:
                self.moveWave()
            else:
                self.moveNoVis()
            if (totSeconds != None and numSeconds < totSeconds) or totSeconds == None:
                self.after(delay, self.runOnLaser)
            elif totSeconds != None:
                # we have reached the end of when we need to shoot new waves
                self.stop()

    # runs the remaining wave once the laser is turned off
    def runOffLaser(self):
        global on, pause, stop, kill, stepMode, numSeconds, experiment, timeStamps, detectors, root
        if kill:
            self.root.destroy()
        if not (pause or on or stepMode or kill) and len(self.waveSegs) > 0:
            numSeconds += step
            timeStamps.append(self.round())
            if totSeconds != None:
                time, unit = self.unit(totSeconds - numSeconds)
                self.countLabel.config(text='Time Left: ' + ('%2.1f ' % time) + unit)
            if not self.noVisMode:
                self.moveWave()
            else:
                self.moveNoVis()
            self.after(delay, self.runOffLaser)
        if len(self.waveSegs) <= 0 and stop:
            if self.test:
                self.quit()
                Components.components = [[Components.Cmpnts(x, y) for x in range(Components.WIDTHB)] for y in
                                         range(Components.HEIGHTB)]
            else:
                numSeconds = 0
                if totSeconds != None:
                    time, unit = self.unit(totSeconds - numSeconds)
                    self.countLabel.config(text='Time Left: ' + ('%2.1f ' % time) + unit)
                stop = False
                self.onBut.configure(relief='raised')
                if len(detectors) != 0:
                    self.printDetectionTable()
                if len(self.powerMeters) != 0:
                    self.makePowerMeterLists()
                for counter in self.conCounters:
                    Components.CoincidenceCounter.printResult(counter, self)
                for detector in self.detectors:
                    self.grid.itemconfig(detector._vis2, fill='black')
                    detector._count = 0
                    detector._invldMes = 0
                    detector._detections = []
                    detector._used = False
                for powermeter in self.powerMeters:
                    powermeter._label.config(text = (('%4.1f ' % 0) + 'nW'))
                for counter in self.conCounters:
                    counter._counts = 0
                for i in self.powerMeters:
                    i.readings = []
                    i.rounded = []
                    i.deletedHereWave = []
                    i.used = False
            experiment += 1
            timeStamps = []
            print()

    # used to turn on laser
    def on(self):
        global on, stop, numSeconds, totSeconds, ran
        if not on and (totSeconds == None or numSeconds < totSeconds) and not stop:
            self.onBut.configure(relief='sunken')
            on = True
            ran = True
            for laser in self.lasers:
                if type(laser) == Components.LED:
                    laser._vis = laser.visualPictureFlat(self, Image.open(os.path.join(imgPath,"LEDOn.png")))
                else:
                    self.grid.itemconfig(laser._vis2, fill='red')
            if self.noVisMode:
                self.runOffline()
            else:
                self.runOnLaser()

    # used to pause laser
    def pause(self):
        global pause, on, stop
        if not pause:
            pause = True
            self.pauseBut.configure(relief='sunken')
        else:
            self.pauseBut.configure(relief='raised')
            pause = False
            if stop == True:
                self.runOffLaser()
            elif on:
                self.runOnLaser()

    # used to stop laser
    def stop(self):
        global stop, stepMode, ran
        if not stop and not stepMode:
            global on
            on = False
            stop = True
            for laser in self.lasers:
                if type(laser) == Components.LED:
                    laser._vis = laser.visualPictureFlat(self, Image.open(os.path.join(imgPath,"LEDOff.png")))
                else:
                    self.grid.itemconfig(laser._vis2, fill='grey')
            if ran:
                self.runOffLaser()
            else:
                stop = False
            ran = False

    # end the program
    def quit(self):
        global kill, on, pause, stop, stepMode, detectors, timeStamps
        if pause or stepMode or on or stop:
            if not self.test:
                if len(detectors) != 0:
                    self.printDetectionTable()
                if len(self.powerMeters) != 0:
                    self.makePowerMeterLists()
                for i in self.conCounters:
                    Components.CoincidenceCounter.printResult(i, self)
            for i in detectors:
                i._count = 0
                i._invldMes = 0
                i._detections = []
            for i in self.conCounters:
                i._counts = 0
            print()
            for i in self.powerMeters:
                i.readings = []
                i.rounded = []
                i.deletedHereWave = []
                i.used = False
        root.destroy()
        timeStamps = []
        kill = True

    # slows down the wave but it continues to move
    def slowMotion(self):
        global slowMo, delay, on
        if not on and (totSeconds == None or numSeconds < totSeconds):
            self.slow.configure(relief='sunken')
            delay = 1000
            slowMo = True
            self.on()
        elif not slowMo:
            self.slow.configure(relief='sunken')
            delay = 1000
            slowMo = True
        else:
            delay = 1
            self.slow.configure(relief='raised')
            slowMo = False

    # stop the wave from moving to go into step mode
    def stepMode(self):
        global stepMode, pause, stop, on
        if not stepMode and not self.noVisMode:
            self.stepModeBut.configure(relief='sunken')
            stepMode = True
        else:
            stepMode = False
            self.stepModeBut.configure(relief='raised')
            if stop:
                self.runOffLaser()
            elif on:
                on = True
                stop = False
                self.runOnLaser()

    #move the program forward one step
    def stepForward(self):
        global stepMode, on, numSeconds, timeStamps, totSeconds, stop
        if stepMode:
            if (on or stop) and not pause:
                if on:
                    numSeconds += step
                    if totSeconds != None:
                        time, unit = self.unit(totSeconds - numSeconds)
                        self.countLabel.config(text='Time Left: ' + ('%2.1f ' % time) + unit)
                    if numSeconds >= totSeconds:
                        on = False
                        stop = True
                    timeStamps.append(self.round())
                    for laser in self.lasers:
                        laser.shoot(self)
                        if numSeconds >= totSeconds:
                            if type(laser) == Components.LED:
                                laser._vis = laser.visualPictureFlat(self, Image.open(os.path.join(imgPath,"LEDOff.png")))
                            else:
                                self.grid.itemconfig(laser._vis2, fill='grey')
                self.moveWave()

    def stepBack(self):
        global wentBack, stepMode, pause, stop, on, numSeconds, timeStamps
        if stepMode and not pause:
            if not stop and len(timeStamps) != 0:
                numSeconds -= step
                if totSeconds != None:
                    time, unit = self.unit(totSeconds - numSeconds)
                    self.countLabel.config(text='Time Left: ' + ('%2.1f ' % time) + unit)
                timeStamps.pop()
            if not self.noVisMode:
                for l, wave in zip(reversed(self.waveVis), reversed(self.waveSegs)):
                    pos = self.grid.coords(l)
                    centerX = ((pos[0] + pos[2]) / 2)
                    if pos[2] > (50 * Components.WIDTHB) or pos[3] > (50 * Components.HEIGHTB) or pos[2] < 0 or pos[3] < 0 and pos != []:
                        self.waveSegs.remove(wave)
                        self.waveVis.remove(l)
                        pos = self.grid.coords(l)
                    for comp in self.comps:
                        x = int(pos[2] / scFac)
                        y = int(pos[3] / scFac)
                        comp.bringForward(self)
                        # if type(comp) == Components.SingleModeFiber:
                        #     if centerX == comp._xStrtCheck  and pos[1] == comp._yStrtCheck:
                        #         if comp._orientStrt == 270 or comp._orientStrt == 180:
                        #             comp.useCompBack(wave, self, 14, 15, comp._orientStrt, comp._orientStp, l)
                        #         elif comp._orientStrt == 0 or comp._orientStrt == 90:
                        #             comp.useCompBack(wave, self, 0, 1, comp._orientStp, comp._orientStrt, l)
                        #     elif centerX == comp._xStpCheck and pos[1] == comp._yStpCheck:
                        #         if comp._orientStrt == 270 or comp._orientStrt == 180:
                        #             comp.useCompBack(wave, self, 14, 15, comp._orientStrt, comp._orientStp, l)
                        #         elif comp._orientStrt == 0 or comp._orientStrt == 90:
                        #             comp.useCompBack(wave, self, 0, 1, comp._orientStp, comp._orientStrt, l)
                        if centerX == comp._centerX and pos[1] == comp._centerY:
                            if type(comp) == Components.Laser or type(comp) == Components.EntanglementSource or type(comp) == Components.LED:
                                stop = False
                                on = True
                            notContinue = comp.useCompBack(wave, self, x, y, l)
                            if notContinue:
                                self.waveSegs.remove(wave)
                                self.waveVis.remove(l)
                                self.grid.delete(l)
                    self.grid.move(l, -1 * wave._xSpeed, -1 * wave._ySpeed)
                i = 0
                for i in detectors:
                    i.useCompBack(self)
                for i in self.powerMeters:
                    i.useCompBack(self)
                for i in self.conCounters:
                    i.checkBack(self)
                for i in self.beamblockers:
                    i.useCompBack(self)
                for i in self.beamSplitters:
                    i._skip = False
                if (len(self.deleteOverallEdge) > 0):
                    self.addBackDeadWave(self.deleteOverallEdge.pop(), deletedVisual)
                    if not stop and not on:
                        stop = True
                if (len(self.deleteOverallBlocked) > 0):
                    self.addBackDeadWave(self.deleteOverallBlocked.pop(), Components.Laser.centeredLaser)
                for i in self.blocking:
                    i.bringForward(self)
            else:
                l = None
                for wave in reversed(self.waveSegs):
                    thickness = wave._thick
                    diff = thickness / 2
                    wave._scalX += wave._xSpeed
                    wave._scalY += wave._ySpeed
                    pos = [wave._scalX + 25 - diff, wave._scalY + 25, wave._scalX + 25 + diff, wave._scalY + 25]
                    centerX = ((pos[0] + pos[2]) / 2)
                    if pos[2] > (50 * Components.WIDTHB) or pos[3] > (50 * Components.HEIGHTB) or pos[2] < 0 or pos[3] < 0 and pos != []:
                        self.waveSegs.remove(wave)
                    for comp in self.comps:
                        x = int(pos[2] / scFac)
                        y = int(pos[3] / scFac)
                        comp.bringForward(self)
                        # if type(comp) == Components.SingleModeFiber:
                        #     if centerX == comp._xStrtCheck  and pos[1] == comp._yStrtCheck:
                        #         if comp._orientStrt == 270 or comp._orientStrt == 180:
                        #             comp.useCompBack(wave, self, 14, 15, comp._orientStrt, comp._orientStp, l)
                        #         elif comp._orientStrt == 0 or comp._orientStrt == 90:
                        #             comp.useCompBack(wave, self, 0, 1, comp._orientStp, comp._orientStrt, l)
                        #     elif centerX == comp._xStpCheck and pos[1] == comp._yStpCheck:
                        #         if comp._orientStrt == 270 or comp._orientStrt == 180:
                        #             comp.useCompBack(wave, self, 14, 15, comp._orientStrt, comp._orientStp, l)
                        #         elif comp._orientStrt == 0 or comp._orientStrt == 90:
                        #             comp.useCompBack(wave, self, 0, 1, comp._orientStp, comp._orientStrt, l)
                        if centerX == comp._centerX and pos[1] == comp._centerY:
                            if type(comp) == Components.Laser or type(comp) == Components.EntanglementSource or type(comp) == Components.LED:
                                stop = False
                                on = True
                            notContinue = comp.useCompBack(wave, self, x, y, l)
                            if notContinue:
                                self.waveSegs.remove(wave)
                    wave._scalX += wave._xSpeed
                    wave._scalY += wave._ySpeed
                i = 0
                for i in detectors:
                    i.useCompBack(self)
                for i in self.powerMeters:
                    i.useCompBack(self)
                for i in self.conCounters:
                    i.checkBack(self)
                for i in self.beamSplitters:
                    i._skip = False
                if (len(self.deleteOverallEdge) > 0):
                    self.addBackDeadWave(self.deleteOverallEdge.pop(), deletedVisual)
                    if not stop and not on:
                        stop = True
                if (len(self.deleteOverallBlocked) > 0):
                    self.addBackDeadWave(self.deleteOverallBlocked.pop(), Components.Laser.centeredLaser)
                for i in self.blocking:
                    i.bringForward(self)

    # round numSeconds to the correct micro second version in preparation to append it to a list of time stamps
    def round(self):
        global numSeconds
        unit = 'uS'
        seconds = numSeconds
        seconds /= 1e-6
        seconds = round(seconds)
        return str(seconds) + " " + unit

    # move that timeseg forward and see if it will interact with any components
    def moveWave(self):
        for l, wave in zip(reversed(self.waveVis), reversed(self.waveSegs)):
            self.grid.move(l, wave._xSpeed, wave._ySpeed)
            pos = self.grid.coords(l)
            centerX = ((pos[0] + pos[2]) / 2)
            if pos[2] >= (50 * Components.WIDTHB) or pos[3] >= (50 * Components.HEIGHTB) or pos[2] <= 0 or pos[3] <= 0 and pos != []:
                wave.recalVals(int(pos[2] / scFac), Components.WIDTH - int(pos[3] / scFac))
                self.deleteRoundEdge.append(wave)
                self.waveSegs.remove(wave)
                self.waveVis.remove(l)
                self.grid.delete(l)
            else:
                for comp in self.comps:
                    x = int(pos[2] / scFac)
                    y = int(pos[3] / scFac)
                    comp.bringForward(self)
                    # if type(comp) == Components.SingleModeFiber:
                    #     notContinue= False
                    #     if centerX == comp._xStrtCheck and pos[1] == comp._yStrtCheck:
                    #         notContinue = comp.useComp(wave, self, 14, 15, comp._orientStrt, comp._orientStp, l)
                    #     elif centerX == comp._xStpCheck and pos[1] == comp._yStpCheck:
                    #         notContinue = comp.useComp(wave, self, 0, 1, comp._orientStp, comp._orientStrt, l)
                    #     if notContinue:
                    #         if type(comp) != Components.Detector and type(comp) != Components.PowerMeter:
                    #             self.blocking.append(comp)
                    #             wave.recalVals(x, Components.WIDTH - y)
                    #             self.deleteRoundBlocked.append(wave)
                    #         self.waveSegs.remove(wave)
                    #         self.waveVis.remove(l)
                    #         self.grid.delete(l)
                    # print(centerX, comp._centerX, pos[1], comp._centerY)
                    if centerX == comp._centerX and pos[1] == comp._centerY:
                        notContinue = comp.useComp(wave, self, x, y, l)
                        if notContinue:
                            if type(comp) != Components.Detector and type(comp) != Components.PowerMeter:
                                self.blocking.append(comp)
                                wave.recalVals(x, Components.WIDTH - y)
                                self.deleteRoundBlocked.append(wave)
                            self.waveSegs.remove(wave)
                            self.waveVis.remove(l)
                            self.grid.delete(l)
                    if (type(comp) == Components.TimeDelay and (((centerX == (comp._centerX + 25) or centerX == (comp._centerX - 25)) and
                        (pos[1] == comp._centerY) and wave._direction % 180 == comp._orientation % 180) or ((pos[1] == (comp._centerY + 25) or pos[1] == comp._centerY - 25)
                        and centerX == comp._centerX and wave._direction % 180 == comp._orientation % 180))):
                            # hide the wave
                            if not self.noVisMode:
                                if wave._hide == False:
                                    self.grid.tag_lower(l)
                                    wave._hide = True
                                else:
                                    wave._hide = False
                                    self.grid.tag_raise(l)
        self.deleteOverallEdge.append(self.deleteRoundEdge.copy())
        self.deleteRoundEdge = []
        self.deleteOverallBlocked.append(self.deleteRoundBlocked.copy())
        self.deleteRoundBlocked = []
        for i in self.splitCheckWaves:
            l = self.splitCheckVis[self.splitCheckWaves.index(i)]
            Components.TimeSeg.checkTwoInputs(i, self, l, self.splitCheckWaves.index(i) + 1)
        self.splitCheckWaves.clear()
        self.splitCheckVis.clear()
        for i in detectors:
            if i._used == False:
                i.darkCounts(self)
            else:
                i._used == False
        for i in self.powerMeters:
            if not i._used:
                i.useDark()
            else:
                i._used = False
        for i in self.conCounters:
            i.checkCoincidence()

    def moveNoVis(self):
        l = None
        for wave in reversed(self.waveSegs):
            diff = wave._thick / 2
            wave._scalX += wave._xSpeed
            wave._scalY += wave._ySpeed
            pos = [wave._scalX + 25 - diff, wave._scalY + 25, wave._scalX + 25 + diff, wave._scalY + 25]
            centerX = ((pos[0] + pos[2]) / 2)
            if pos[2] >= (50 * Components.WIDTHB) or pos[3] >= (50 * Components.HEIGHTB) or pos[2] <= 0 or \
                    pos[3] <= 0 and pos != []:
                wave.recalVals(int(pos[2] / scFac), Components.WIDTH - int(pos[3] / scFac))
                self.deleteRoundEdge.append(wave)
                self.waveSegs.remove(wave)
            else:
                for comp in self.comps:
                    x = int(pos[2] / scFac)
                    y = int(pos[3] / scFac)
                    # if type(comp) == Components.SingleModeFiber:
                    #     notContinue = False
                    #     if centerX == comp._xStrtCheck and pos[1] == comp._yStrtCheck:
                    #         notContinue = comp.useComp(wave, self, 14, 15, comp._orientStrt, comp._orientStp, l)
                    #     elif centerX == comp._xStpCheck and pos[1] == comp._yStpCheck:
                    #         notContinue = comp.useComp(wave, self, 0, 1, comp._orientStp, comp._orientStrt, l)
                    #     if notContinue:
                    #         if type(comp) != Components.Detector and type(comp) != Components.PowerMeter:
                    #             self.blocking.append(comp)
                    #             wave.recalVals(x, Components.WIDTH - y)
                    #             self.deleteRoundBlocked.append(wave)
                    #         self.waveSegs.remove(wave)
                    if centerX == comp._centerX and pos[1] == comp._centerY:
                        notContinue = comp.useComp(wave, self, x, y, l)
                        if notContinue:
                            if type(comp) != Components.Detector and type(comp) != Components.PowerMeter:
                                self.blocking.append(comp)
                                wave.recalVals(x, Components.WIDTH - y)
                                self.deleteRoundBlocked.append(wave)
                            self.waveSegs.remove(wave)
        self.deleteOverallEdge.append(self.deleteRoundEdge.copy())
        self.deleteRoundEdge = []
        self.deleteOverallBlocked.append(self.deleteRoundBlocked.copy())
        self.deleteRoundBlocked = []
        for i in self.splitCheckWaves:
            l = None
            Components.TimeSeg.checkTwoInputs(i, self, l, self.splitCheckWaves.index(i) + 1)
        self.splitCheckWaves.clear()
        self.splitCheckVis.clear()
        for i in detectors:
            if i._used == False:
                i.darkCounts(self)
            else:
                i._used == False
        for i in self.powerMeters:
            if not i._used:
                i.useDark()
            else:
                i._used = False
        for i in self.conCounters:
            i.checkCoincidence()

    # when moving back in time, bring back waves that were killed either by components, or by moving off the board
    def addBackDeadWave(self, listOfWaves, method):
        for wave in listOfWaves:
            self.waveSegs.append(wave)
            obj = method(self, wave)
            self.grid.itemconfig(obj, fill=Components.TimeSeg.color(wave))
            self.waveVis.append(obj)
            self.grid.move(obj, -1 * wave._xSpeed, -1 * wave._ySpeed)

    # methods below are used to print out results and write out the data to a file

    # print the results at the end of the experiment
    def printDetectionTable(self):
        global timeStamps
        print("RESULTS FROM RUN " + str(experiment))
        listsPerTime = self.makeDetectorResults()
        allCombs = self.fixResultingDict(listsPerTime)
        self.printResultingCounts(allCombs)

    # change the allComb dict to have the appropriate number of counts for each detector probability
    def fixResultingDict(self, listsPerTime):
        allCombs = self.allCombinations(0, len(self.detectors), self.originalPattern(), {})
        for i in listsPerTime:
            count = ''
            for j in i[1:]:
                if j == "C":
                    count += 'C'
                else:
                    count += 'N'
            counts = allCombs.get(count)
            # we didn't find the new pattern so we need to change the counts from none to zero
            if counts is None:
                raise ValueError('Something went wrong! Please email Dr. La Cour with what excitement you'
                                 'run that found this bug in calculating end results!')
            currCount = counts['counts']
            counts['counts'] = currCount + 1
            allCombs[count] = counts
        return allCombs

    # go through the dic of all the possible detector combinations and print out their resulting counts in ascending
    # order
    def printResultingCounts(self, allCombs):
        for k in sorted(allCombs, key=lambda i: (len(allCombs[i]["detectors"]), i)):
            detectors = allCombs[k]['detectors']
            countNum = allCombs[k]['counts']
            if len(detectors) == 1:
                print("Detector " + str(detectors[0]) + " only: " + str(countNum))
            elif len(detectors) != 0:
                detectorList = "Detectors " + str(detectors[0])
                for x in detectors[1:]:
                    detectorList += " & " + str(x)
                # if countNum > 0:
                print(detectorList + ": " + str(countNum))

    # make the dictionary for each possible detector combination outcome
    def makeDict(self, pattern):
        dict = {'detectors' : self.getDetectorsInPattern(pattern), 'counts' : 0}
        return dict

    # change the string of 'C' and 'N' to a list of the detectors that clicked at this point
    def getDetectorsInPattern(self, pattern):
        countSpot = []
        for detNum in range(len(pattern)):
            if pattern[detNum] == 'C':
                countSpot.append(detNum + 1)
        return countSpot

    # returns all the possible cominations of clicks you can get from the detectors
    def allCombinations(self, detIndex, numDet, currPattern, allPatterns):
        if numDet == 0:
            return
        options = ['C', 'N']
        for i in options:
            currPattern[detIndex] = i
            str = ""
            string = str.join(currPattern)
            if not string in allPatterns:
                allPatterns[string] = self.makeDict(string)
            self.allCombinations(detIndex + 1, numDet - 1, currPattern, allPatterns)
            currPattern[detIndex] = 'N'
        return allPatterns

    # get a string of 'N' as the case base for when no detectors clicked
    def originalPattern(self):
        result = []
        for x in detectors:
            result.append('N')
        return result

    # collect detector count data from experiment
    def makeDetectorResults(self):
        header = ['Time(us)']
        max_len = 1e12
        long_ind = 0
        for i in range(len(detectors)):
            header.append("Detector " + (str(i + 1)))
            if len(detectors[i]._detections) < max_len :
                max_len = len(detectors[i]._detections) 
                long_ind = i
        listsPerTimeForFile = [header]
        listsPerTime = []
        if len(detectors) != 0:
            for i in range(len(detectors[long_ind]._detections)):
                found = False
                detIndex = 0
                while not found and detIndex < len(detectors):
                    found = detectors[detIndex]._detections[i] == "C"
                    detIndex += 1
                if found:
                    time = timeStamps[i][:-2]
                    count = [time]
                    timeCount = [time]
                    for det in detectors:
                        timeCount.append(det._detections[i])
                    listsPerTime.append(timeCount)
                    listsPerTimeForFile.append(self.changeCtoOne(timeCount, count))
            self.writeResultToFile(listsPerTimeForFile, self.csvFilename)
        return listsPerTime

    def makePowerMeterLists(self):
        header = ['Time(us)']
        for i in range(len(self.powerMeters)):
            header.append("PM " + str (i + 1) + " (mW)")
        listsPerTimeForFile = [header]
        if len(self.powerMeters) != 0:
            for i in range(len(self.powerMeters[0].readings)):
                # found = False
                # pmIndex = 0
                # while not found and pmIndex < len(self.powerMeters):
                #     found = self.powerMeters[pmIndex].readings[i] != 0
                #     pmIndex += 1
                # if found:
                time = timeStamps[i][:-2]
                timeCount = [time]
                for pm in self.powerMeters:
                    timeCount.append((pm.readings[i]))
                listsPerTimeForFile.append(timeCount)
            path = os.getcwd()
            path = os.path.join(path, 'Results')
            powerFile = 'PM_Readings.csv'
            powerFile = os.path.join(path, powerFile)
            self.writeResultToFile(listsPerTimeForFile, powerFile)


    # used to change the C's that represent when there was a count to a 1 for writing the file
    def changeCtoOne(self, timeCount, count):
        for i in timeCount[1:]:
            if i == 'C':
                count.append('1')
            else:
                count.append('0')
        return count

    # write the results into the file
    def writeResultToFile(self, listsPerDetector, file):
        with open(file, 'w', newline='') as csvFile:
            wri = writer(csvFile)
            # wri.writerow(timesWithCount)
            for listFromDet in listsPerDetector:
                wri.writerow(listFromDet)

# when a visual of a timeseg needs to be brought back after being deleted, call this method
def deletedVisual(canvas, wave):
    thickness = wave._thick
    diff = thickness / 2
    if wave._direction == Components.LEFT or wave._direction == Components.RIGHT:
        obj = canvas.grid.create_line(wave._scalX - diff, wave._scalYB + 25, wave._scalX + diff,
                                      wave._scalYB + 25, fill=wave._color, width=thickness)
    elif wave._direction == Components.DOWN or wave._direction == Components.UP:
        obj = canvas.grid.create_line(wave._scalX + 25 - diff, wave._scalYB, wave._scalX + 25 + diff,
                                      wave._scalYB, fill=wave._color, width=thickness)
    return obj

class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self, width = 135, height=height - 200)
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
