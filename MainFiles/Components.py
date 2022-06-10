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


from random import gauss
from random import randrange
from random import uniform
import math
import math
import os
from tkinter import *
from copy import deepcopy
from PIL import Image
from PIL import ImageTk

# these are constants used throughout the program
HORZ = 0
DIAG = 45
VERT = 90
ANTI = 135
RIGHT = 0
UP = 90
LEFT = 180
DOWN = 270
QUARTER = 90
HALF = 180
FULL = 360
PHTN_PER_BIN = 1e5
WIDTH = 33
WIDTHB = WIDTH + 1
HEIGHT = 18
HEIGHTB = HEIGHT + 1
scFac = 50
pixPerDegree = 50 / 180
deletedWave = []
imgPath = os.path.join(os.getcwd(), 'MainFiles')
imgPath = os.path.join(imgPath, 'Images')

# This is the parent class for the various component types
class Cmpnts:
    # default values are none (empty component)
    # default for orientationaion is 20 so I know if its the first initialization
    def __init__(self, x, y, orientation = None): # For each individual component
        if type(x) != int or type(y) != int or x > WIDTHB or y > HEIGHTB or x < 0 or y < 0:
            raise ValueError('x and y coordinates must be integers in the domain [0, 17]. '
                             'You tried: x = ' + str(x) + ', y = ' + str(y))
        self._x = x
        self._scalX = x * 50
        self._y = y
        self._scalY = y * 50
        # if this statement is not true then the component is just a filler component
        if orientation != None:
            if type(components[self._y][self._x]) != Cmpnts and type(self) != TimeSeg:
                raise ValueError('You cannot place two components in the same spot. Position of two components: ('
                                + str(x) + ", " + str(y) + ")")
            self._orientation = int(orientation % 360)
            self._centerX = self._x * scFac + 25
            self._centerY = self._y * scFac + 25
            self._vis = None
            self._vis2 = None
            self._vis3 = None

    # recalculate the x and y position of a wave before it is deleted so that if it needs to be brought back it'll be
    # in the right place
    def recalVals(self, x, y): # Rewind method
        # x and y is the position of the component that is blocking the wave
        self._x = x
        self._y = y
        self._scalX = x * 50
        self._scalY = y * 50

    # brings the components infront of the wave
    def bringForward(self, canvas):
        if not canvas.noVisMode:
            canvas.grid.tag_raise(self._vis)

    # blocks the wave if it comes into contact with this component
    def useComp(self, wave, canvas, x, y, l):
        # blocks any wave that comes back
        return True

    # creates a vacuum mode
    @staticmethod
    def createVacMode(energyPerMode = 0.5): # energyPerMode is in self._units of hbar*omega = h*c/lamb
        # standard complex Gaussian is gauss(0, 1) / sqrt(2)
        x = math.sqrt(energyPerMode) * gauss(0, 1) / math.sqrt(2)
        y = math.sqrt(energyPerMode) * gauss(0, 1) / math.sqrt(2)
        return complex(x, y)

    # def lineOrRec(self, canvas, color, width, change): # Draws polarizers, plates, filters, lasers, detectors
    #     dir = self._orientation
    #     if dir == LEFT:
    #         dir = RIGHT
    #     elif dir == DOWN:
    #         dir = UP
    #     if dir == HORZ:
    #         obj = canvas.grid.create_line(self._scalX + change, self._scalYB + 25, self._scalX + 50 - change, self._scalYB + 25,
    #                                fill=color, width=width)
    #     elif dir == VERT:
    #         obj = canvas.grid.create_line(self._scalX + 25, self._scalYB + change, self._scalX + 25, self._scalYB + 50 - change,
    #                                fill=color, width=width)
    #     elif dir == DIAG:
    #         obj = canvas.grid.create_line(self._scalX + 50 - change, self._scalYB + change, self._scalX + change, self._scalYB + 50 - change,
    #                                fill=color, width=width)
    #     elif dir == ANTI:
    #         obj = canvas.grid.create_line(self._scalX + change, self._scalYB + change, self._scalX + 50 - change, self._scalYB + 50 - change,
    #                                fill=color, width=width)
    #     else:
    #         exitString = 'incorrect orientation for type' + str(type(self))
    #         sys.exit(exitString)
    #     return obj

    # light for detectors and lasers to indicate on / count and off / no count
    def light(self, canvas, color):
        dir = self._orientation
        # place a light on the component based on that components orientationation
        if dir == RIGHT:
            obj = canvas.grid.create_rectangle(self._scalX + 35, self._scalY + 22.5, self._scalX + 40,
                                        self._scalY + 27.5, fill=color)
        elif dir == LEFT:
            obj = canvas.grid.create_rectangle(self._scalX + 10, self._scalY + 22.5, self._scalX + 15,
                                        self._scalY + 27.5, fill=color)
        elif dir == UP:
            obj = canvas.grid.create_rectangle(self._scalX + 22.5, self._scalY + 10, self._scalX + 27.5,
                                        self._scalY + 15, fill=color)
        elif dir == DOWN:
            obj = canvas.grid.create_rectangle(self._scalX + 22.5, self._scalY + 35, self._scalX + 27.5,
                                        self._scalY + 40, fill=color)
        else:
            # wrong orientationation was sent in!
            exitString = 'incorrect orientation for type' + str(type(self))
            sys.exit(exitString)
        return obj

    # used rotate bs picture and pbs picture as needed
    def visualPictureBS(self, canvas, fileName1, fileName2):
        # place the picture for the component based on the components orientationation
        if self._orientation == HORZ or self._orientation == VERT:
            self.image = Image.open(fileName1)
            self.rotated = ImageTk.PhotoImage(self.image.rotate(self._orientation))
        else:
            self.image = Image.open(fileName2)
            self.rotated = ImageTk.PhotoImage(self.image.rotate(self._orientation - ANTI))
        return canvas.grid.create_image(self._centerX, self._centerY, image = self.rotated)

    # used to rotate component pictures to their needed orientationation
    def visualPictureFlat(self, canvas, image):
        # place the image of a component based on the orientationation when
        # the image is flat instead of square or rectangular
        self.rotated = ImageTk.PhotoImage(image.rotate(self._orientation, expand=True))
        return canvas.grid.create_image(self._centerX, self._centerY, image=self.rotated)


components = [[Cmpnts(x, y) for x in range(WIDTHB)] for y in range(HEIGHTB)] # Keep track of components


# class only used by the program itself, should not be used by user
class TimeSeg(Cmpnts):
    # alpha is the H component of the photon while beta is the V component
    def __init__(self, x, y, orientation, hComp, vComp, canvas):
        # the x, y, and orientation make in super are only the beginning x, y and orientation
        super().__init__(x, y, orientation)
        self._xVis = 0
        self._yVis = 0
        self._hComp = hComp
        self._vComp = vComp
        self._direction = orientation
        self._xSpeed = 0
        self._ySpeed = 0
        self._thick = 5
        self._pause = False
        self._count = 0
        self._color = self.color()
        TimeSeg.speed(self, canvas)
        self.hBefore = []
        self.vBefore = []
        self.hAfter = []
        self.vAfter = []
        self._hide = False

    # do not change or else it will mess up interactions between wave and components
    def speed(self, canvas):
        # because of the size of the components, if the speed is changed, then
        # the wave will never reach the center of the components
        if self._direction == RIGHT:
            self._xSpeed = 5
            self._ySpeed = 0
        elif self._direction == UP:
            self._xSpeed = 0
            self._ySpeed = -5
        elif self._direction == LEFT:
            self._xSpeed = -5
            self._ySpeed = 0
        elif self._direction == DOWN:
            self._xSpeed = 0
            self._ySpeed = 5
        # if canvas.noVisMode:
        #     self._xSpeed *= 10
        #     self._ySpeed *= 10

    # applies a self._unitary gate to the wave with the angle, phase, and lambda passed in
    def applyUnitary(wave, angle, lamb, phase):
        # calculate the unitary matrix based on the given angle, phase, and lambda
        U = [[0, 0], [0, 0]]
        z1 = imag_exp(phase)
        z2 = -imag_exp(lamb)
        z3 = imag_exp(lamb + phase)
        U[0][0] = math.cos(angle / 2)
        U[1][0] = math.sin(angle / 2) * z1
        U[0][1] = math.sin(angle / 2) * z2
        U[1][1] = math.cos(angle / 2) * z3
        wave.martixMult(U)

    # multiplying a matrix with our vector state
    def martixMult(self, U):
        # multiply a time segment (vector) by a matrix
        a = self._hComp
        b = self._vComp
        self._hComp = U[0][0] * a + U[0][1] * b
        self._vComp = U[1][0] * a + U[1][1] * b

    # prepares a vacuum state for a wave
    # Two vacuum components are created
    def prepareVacuum(self, energyPerMode=0.5):
        # get two vac modes that will the noise added to a timeseg
        self._alpha = Cmpnts.createVacMode(energyPerMode)
        self._beta  = Cmpnts.createVacMode(energyPerMode)

    # pick the color based off of which mode is most probable
    def color(self):
        h = self._hComp
        v = self._vComp

        if self._hComp != 0 or self._vComp != 0:
            H = [1, 0]
            D = [1 / math.sqrt(2), 1 / math.sqrt(2)]
            R = [1 / math.sqrt(2), 1j * 1 / math.sqrt(2)]
            opH = (abs(H[0] * h + H[1] * v) ** 2) / (abs(h) ** 2 + abs(v) ** 2)
            opD = (abs(D[0] * h + D[1] * v) ** 2) / (abs(h) ** 2 + abs(v) ** 2)
            opR = (abs(conj(R[0]) * h + conj(R[1]) * v) ** 2) / (abs(h) ** 2 + abs(v) ** 2)
            c1 = opH * opD * (1 - opD) * opR * (1 - opR) + opD * opH * (1 - opH) * opR * (1 - opR) + (
                    opR + 0.5 * (1 - opR)) * opH * (1 - opH) * opD * (1 - opD);
            c2 = opH * (1 - opH) * opR * (1 - opR) + 0.5 * opR * opH * (1 - opH) * opD * (1 - opD)
            c3 = (1 - opH) * opD * (1 - opD) * opR * (1 - opR) + (1 - opR) * opH * (1 - opH) * opD * (1 - opD)
            c = [c1, c2, c3]
            maxAmount = max(c)
            colorRGB = [i / maxAmount * 255 for i in c]
            tk_rgb = "#%02x%02x%02x" % (int(colorRGB[0]), int(colorRGB[1]), int(colorRGB[2]))
            return tk_rgb

        else:
            # if the h and v comp are zero, something may have been wrong
            # so instead of deleting, will return white so that we know to check
            # if something is wrong
            return 'white'

        """"# old color scheme: pick max probability
        V = [0, 1]
        A = [1 / math.sqrt(2), -1 / math.sqrt(2)]
        L = [1 / math.sqrt(2), -1j * 1 / math.sqrt(2)]
        opH = abs(H[0] * a + H[1] * b) ** 2
        opV = abs(V[0] * a + V[1] * b) ** 2
        opD = abs(D[0] * a + D[1] * b) ** 2
        opA = abs(A[0] * a + A[1] * b) ** 2
        opR = abs(R[0] * a + R[1] * b) ** 2
        opL = abs(L[0] * a + L[1] * b) ** 2
        ops = [opH, opV, opD, opA, opR, opL]
        # print(opH, opV, opD, opA, opR, opL)
        choice = ops.index(max(ops))
        color = ['red', 'blue', 'yellow', 'green', 'purple', 'tomato']"""

        """old color scheme: pastel colors
        opH = (abs(H[0] * h + H[1] * v) ** 2)/(abs(h)**2 + abs(v)**2) * 256
        opD = (abs(D[0] * h + D[1] * v) ** 2)/(abs(h)**2 + abs(v)**2) * 256
        opR = (abs(conj(R[0]) * h + conj(R[1]) * v) ** 2)/(abs(h)**2 + abs(v)**2) * 256
        intOpH = min(int(abs(opH)), 255)
        intOpD = min(int(abs(opD)), 255)
        intOpR = min(int(abs(opR)), 255)
        tk_rgb = "#%02x%02x%02x" % (intOpH, intOpD, intOpR)
        print(intOpH, intOpD, intOpR)"""

    # checks if there was or was not two inputs on BS and PBS and adds noise accordingly
    def checkTwoInputs(self, canvas, l, start): # If there was two inputs, add vacuum if two inputs are not present
        found = False
        j = start
        if not canvas.noVisMode:
            pos = canvas.grid.coords(l)
        else:
            thickness = self._thick
            diff = thickness / 2
            pos = [self._scalX + 25 - diff, self._scalY + 25, self._scalX + 25 + diff, self._scalY + 25]
        # get the current position of the wave
        x = pos[2]
        y = pos[3]
        # get the component at this poistion
        xComp = int(pos[2] / 50)
        yComp = int(pos[3] / 50)
        comp = components[yComp][xComp]
        # look for another wave at this spot that is traveling in the same direction
        while not found and j < len(canvas.splitCheckWaves):
            found = self.twoInput(canvas, comp, x, y, l, j, found)
            j += 1
        j = 0
        # if there wasn't another wave found then we need to add in the vacuum component to the wave
        if found == False and comp._checked == False:
            a = Cmpnts.createVacMode()
            b = Cmpnts.createVacMode()
            # if(canvas.noNoise == True):
            #     a = 0
            #     b = 0
            while not comp._checked and j < len(canvas.splitCheckWaves):
                self.oneInput(canvas, comp, x, y, a, b, j)
                j += 1
            if not canvas.noVisMode:
                canvas.grid.itemconfig(l, fill=TimeSeg.color(self))
        return found

    # looking to see if their were two inputs and return if the second input
    # was found or not
    def twoInput(self, canvas, comp, x, y, l, j, found):
        if not canvas.noVisMode:
            posCheck = canvas.grid.coords(canvas.splitCheckVis[j])
        else:
            checkWave = canvas.splitCheckWaves[j]
            posCheck = [checkWave._scalX + 25 - checkWave._thick / 2, checkWave._scalY + 25, checkWave._scalX + 25 + checkWave._thick / 2, checkWave._scalY + 25]
        # get the position of this new current wave
        xCheck = posCheck[2]
        yCheck = posCheck[3]
        # check to see if the current wave is at the same spot as the wave we
        # are checking for, if so, we will check if they are going the same way
        if x == xCheck and y == yCheck and canvas.splitCheckWaves[j] != self:
            if self._direction == canvas.splitCheckWaves[j]._direction:
                comp.oneOrTwo.append(2)
                found = True
                # we need to add the two waves together
                self._hComp += canvas.splitCheckWaves[j]._hComp
                self._vComp += canvas.splitCheckWaves[j]._vComp
                # get rid of the old wave
                deleteWave = canvas.splitCheckWaves[j]
                canvas.waveSegs.remove(deleteWave)
                canvas.splitCheckWaves.remove(deleteWave)
                if not canvas.noVisMode:
                    deleteVis = canvas.splitCheckVis[j]
                    canvas.waveVis.remove(deleteVis)
                    canvas.grid.delete(deleteVis)
                    canvas.splitCheckVis.remove(deleteVis)
                    canvas.grid.itemconfig(l, fill=TimeSeg.color(self))
                if(canvas.debug == True):
                    # let the user know that there was two inputs that we
                    # added together
                    print("Two in!", self._hComp, self._vComp)
                    print()
        return found

    # if there is only one input, add a vacuum component to both parts of that wave
    def oneInput(self, canvas, comp, x, y, a, b, j):
        if not canvas.noVisMode:
            posCheck = canvas.grid.coords(canvas.splitCheckVis[j])
        else:
          checkWave = canvas.splitCheckWaves[j]
          posCheck = [checkWave._scalX + 25 - checkWave._thick / 2, checkWave._scalY + 25,
                checkWave._scalX + 25 + checkWave._thick / 2, checkWave._scalY + 25]
        # get the position of this new current wave
        xCheck = posCheck[2]
        yCheck = posCheck[3]
        # check if they are at the same spot
        if x == xCheck and y == yCheck and canvas.splitCheckWaves[j] != self:
            comp._checked = True
            comp.oneOrTwo.extend([1, 1])
            if type(comp) == PolarizingBeamSplitter:
                # there was one wave that went through a PBS, add noise
                TimeSeg.addVacPolSplitter(a, b, self, canvas.splitCheckWaves[j], canvas)
            elif type(comp) == BeamSplitter:
                # there was one wave that went through a BS, add noise
                TimeSeg.addVacBeamsplitter(a, b, comp, self, canvas.splitCheckWaves[j], canvas)
        if not canvas.noVisMode:
            canvas.grid.itemconfig(canvas.splitCheckVis[j], fill=TimeSeg.color(canvas.splitCheckWaves[j]))

    # takes in a wave and appends that wave to the waveSegs list. Creates the visual representation of that wave segment
    # and appends it to the viual waves list   

    #LOOK AT ME CHECK HOW THIS WORKS LATER
    #### LOOOK AT ME MEEE HELLO GABE CHECK EME OUT

    #                           HERE PLS

    ## 
    def createWave(self, canvas, method):
        # add a new wave to the board, get its visual
        # and append it to the needed lists
        canvas.waveSegs.append(self)
        if canvas.noVisMode != True:
            obj = method(canvas, self)
            # make sure that the wave is the correct color based on its composition
            canvas.grid.itemconfig(obj, fill=TimeSeg.color(self))
            canvas.waveVis.append(obj)


    # method used to add the vac component to a wave that has gone through
    # a pbs
    def addVacPolSplitter(a, b, wave1, wave2, canvas):
        wave1._vComp += b
        wave2._hComp += a
        if (canvas.debug == True):
            # let the user know that there was only one input and let them know
            # that we added noise to the outgoing waves
            print('One in! add: ', a, b)
            print('resulting in', wave1._hComp, wave1._vComp, wave2._hComp, wave2._vComp)
            print()

    # add the vac components a and b to the waves passing
    # though the beamsplitter
    def addVacBeamsplitter(a, b, comp, wave1, wave2, canvas):
        # make a noise wave so that we can send it through the BS
        # noise = TimeSeg(wave1._x, wave1._y, wave1._orientation + 90, a, b, canvas) # BRL
        noise = TimeSeg(wave1._x, wave1._y, wave2._direction, a, b, canvas) # BRL
        factor = Mirror.reflectWave(noise, comp._orientation, canvas)
        # get the two parts of the wave that we are going to
        # add to the resulting wave of the BS
        reflH = noise._hComp * math.sqrt(comp._reflectivity) # BRL * -1
        reflV = noise._vComp * math.sqrt(comp._reflectivity) # BRL * -1
        noise._hComp = factor * math.sqrt(1 - comp._reflectivity) * noise._hComp
        noise._vComp = factor * math.sqrt(1 - comp._reflectivity) * noise._vComp
        # add the noise
        wave2._hComp += noise._hComp
        wave2._vComp += noise._vComp
        wave1._hComp += reflH
        wave1._vComp += reflV
        if (canvas.debug == True):
            # let the user know that there was one input and that we added noise
            # to the wave
            print('One in! add: ',noise._hComp, noise._vComp, reflH, reflV)
            print('resulting in', wave1._hComp, wave1._vComp, wave2._hComp, wave2._vComp)
            print()


class Laser(Cmpnts):
    # user has to enter either 0, 90, 180, or 270 for the orientation
    def __init__(self, canvas, x, y, orientation = 0, mode = 'H', power = 4e-3):
        modes = 'HVDARL'
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        # check to see if we need to use default values
        super().__init__(x, y, orientation)
        if type(self._orientation) != int or not(self._orientation in possibleorientationations):
            raise ValueError('The orientation for a laser must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}.'
                             ' You tried: ' + str(orientation))
        if type(mode) != str or not(mode.upper() in modes):
            raise ValueError('The mode for a laser must be given as a string and be from the set {H, V, D, A, R, L}.'
                             ' You tried: ' + mode)
        components[self._y][self._x] = self
        canvas.lasers.append(self)
        canvas.comps.append(self)
        self._mode = mode
        self._power = power
        self.wavesBackIn = []
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, 'Laser.png')))
        self._vis2 = self.light(canvas, 'grey')

    # Turns the laser on, only shoots one timeSeg of the wave at a time
    def shoot(self, canvas):
        global PHTN_PER_BIN
        if self.wavesBackIn != []:
            # we have gone at reverse so we need to recover the old wave
            last = len(self.wavesBackIn) - 1
            wave = self.wavesBackIn.pop(last)
            if wave != '':
                TimeSeg.createWave(wave, canvas, Laser.centeredLaser)
                self.bringForward(canvas)
        else:
            # pick the color and composition of the wave based of the orientationation of the laser
            lamb = 496.61e-9
            h = 6.62607004e-34
            c = 299792458
            perbin = math.sqrt((self._power * 1e-6) / (h * c / lamb) + 0.5)
            if(canvas.onlyNoise == True):
                perbin = 0
            self.prepareVacuum(canvas)
            # pick where the beam will come from based on the orientationation of the laser
            if self._mode.upper() == 'H':
                wave = TimeSeg(self._x, self._y, self._orientation, perbin + self._alpha, self._beta, canvas)
            elif self._mode.upper() == 'V':
                wave = TimeSeg(self._x, self._y, self._orientation, 0 + self._alpha, perbin + self._beta, canvas)
            elif self._mode.upper() == 'D':
                wave = TimeSeg(self._x, self._y, self._orientation, perbin / math.sqrt(2) + self._alpha,
                               perbin / math.sqrt(2) + self._beta, canvas)
            elif self._mode.upper() == 'A':
                wave = TimeSeg(self._x, self._y, self._orientation, perbin / math.sqrt(2) + self._alpha,
                               - 1 * perbin / math.sqrt(2) + self._beta, canvas)
            elif self._mode.upper() == 'R':
                wave = TimeSeg(self._x, self._y, self._orientation, perbin / math.sqrt(2) + self._alpha,
                               1j * perbin / math.sqrt(2) + self._beta, canvas)
            elif self._mode.upper() == 'L':
                wave = TimeSeg(self._x, self._y, self._orientation, perbin / math.sqrt(2) + self._alpha,
                               -1j * perbin / math.sqrt(2) + self._beta, canvas)
            else:
                # let the user know that they gave us a mode that we don't support
                raise ValueError("You cannot have a laser of the mode " + self._mode)
            TimeSeg.createWave(wave, canvas, Laser.centeredLaser)

    # prepares a vacuum state for a wave
    def prepareVacuum(self, canvas): # Specifically for laser
        self._alpha = Cmpnts.createVacMode()
        self._beta = Cmpnts.createVacMode()
        if(canvas.noNoise == True and canvas.onlyNoise != True):
            # if we want to check the program without noise, set
            # the noise to zero
            self._alpha = 0
            self._beta = 0

    # used when going in reverse
    def useCompBack(self, wave, canvas, x, y, l):
        # get the current position of the wave set
        wave.recalVals(x, y)
        # collect the waves going back into the laser
        self.wavesBackIn.append(wave)
        canvas.grid.itemconfig(self._vis2, fill = 'red')
        return True

    # brings the component infront of the laser
    def bringForward(self, canvas):
        if not canvas.noVisMode:
            canvas.grid.tag_raise(self._vis)
            canvas.grid.tag_raise(self._vis2)

    # shoot the laser beam from the center of the component rather than on the edge
    def centeredLaser(canvas, wave): # Recreating a laser beam, introduces new laser source not from source
        thickness = wave._thick
        diff =  wave._thick / 2
        # find where the laser should come from based on the orientationation of the laser
        if wave._direction == LEFT or wave._direction == RIGHT:
            obj = canvas.grid.create_line(wave._scalX + 25 - diff, wave._scalY + 25, wave._scalX + 25 + diff, wave._scalY + 25,
                                     fill=wave._color, width=thickness)
        elif wave._direction == UP or wave._direction == DOWN:
            obj = canvas.grid.create_line(wave._scalX + 25 - diff, wave._scalY + 25, wave._scalX + 25 + diff, wave._scalY + 25,
                                     fill=wave._color, width=thickness)
        return obj


class LED(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0, power = 4e-3):
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        # check to see if we need to use default values
        super().__init__(x, y, orientation)
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a laser must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}.'
                               ' You tried: ' + str(orientation))
        components[self._y][self._x] = self
        canvas.lasers.append(self)  # Each laser component
        canvas.comps.append(self)
        self.wavesBackIn = []
        self._power = power
        # print(self._power)
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, 'LEDOff.png')))

    def shoot(self, canvas):
        if self.wavesBackIn != []:
            # we have gone in reverse at some point so we need to recover the old wave
            last = len(self.wavesBackIn) - 1
            wave = self.wavesBackIn.pop(last)
            if wave != '':
                TimeSeg.createWave(wave, canvas, Laser.centeredLaser)
                self.bringForward(canvas)
        else:  # Visual representation of laser
            self.prepareVacuum()
            # create the composition of the output wave based on the LED power
            lamb = 496.61e-9
            h = 6.62607004e-34
            c = 299792458
            perBin = math.sqrt( (self._power * 1e-6) / (h*c/lamb) + 0.5 )
            # create the wave coming from the LED source
            wave = TimeSeg(self._x, self._y, self._orientation, self._alpha * perBin, self._beta * perBin, canvas)
            TimeSeg.createWave(wave, canvas, Laser.centeredLaser)

    # prepares a vacuum state for a wave for a laser
    def prepareVacuum(self):
        self._alpha = Cmpnts.createVacMode()
        self._beta = Cmpnts.createVacMode()

    # method used when going in reverse to collect waves going back into the source
    def useCompBack(self, wave, canvas, x, y, l):
        # be sure that the position stored by the wave is correct
        wave.recalVals(x, y)
        # collect the waves
        self.wavesBackIn.append(wave)
        return True


class EntanglementSource(Cmpnts):
    # there is type one and two PDC. The defualt for r will be 1 and the default for phase will be pi for type two
    # and zero for type one
    def __init__(self, canvas, x, y, orientation = 90, strength = 1, phase = None, entanglement_type = 1, directions="LR"):
        if type == 1 and phase == None:
            phase = 0
        elif type == 2 and phase == None:
            phase = 180
        phase = math.radians((phase))
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        super().__init__(x, y, orientation)
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a SPDC must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}.'
                               ' You tired: ' + str(orientation))
        if type(entanglement_type) != int or not(entanglement_type == 1 or entanglement_type == 2):
            raise ValueError('You must pick either a type one or a type two SPDC. You tried: ' + str(entanglement_type))
        if strength < 0:
            raise ValueError('strength must be greater or equal to zero. You tried: ' + str(strength))
        self._r = strength
        self._varphase = phase
        self._typeConv = entanglement_type
        self._emitDirs = directions
        components[self._y][self._x] = self
        self.wavesBackIn = []
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "SPDC.png")))
        canvas.comps.append(self)
        canvas.lasers.append(self)

    # shoots a pair of entangled photons
    def shoot(self, canvas):
        if self.wavesBackIn != []:
            # we went in reverse so we want to bring back the waves that were collected
            last = len(self.wavesBackIn) - 1
            wave1 = self.wavesBackIn.pop(last)
            wave2 = self.wavesBackIn.pop(last - 1)
            if wave1 != '':
                TimeSeg.createWave(wave1, canvas, Laser.centeredLaser)
            if wave2 != '':
                TimeSeg.createWave(wave2, canvas, Laser.centeredLaser)
            self.bringForward(canvas)
        else: # Creates the output
            self._alphaH = Cmpnts.createVacMode()
            self._alphaV = Cmpnts.createVacMode()
            self._betaH = Cmpnts.createVacMode()
            self._betaV = Cmpnts.createVacMode()
            if self._typeConv == 1:
                self.downConvT1(canvas)
            elif self._typeConv == 2:
                self.downConvT2(canvas)
            else:
                exitString = 'SPDC must be type 1 or 2. The attempted type was was: {}'.format(self._typeConv)
                sys.exit(exitString)

    # this type of entangled pair has perpendicular polarizations
    def downConvT2(self, canvas): # Resulting matrices
        self._alphaHP = self._alphaH * math.cosh(self._r) + conj(self._betaV) * math.sinh(self._r)
        self._alphaVP = self._alphaV * math.cosh(self._r) + imag_exp( self._varphase) * conj(
            self._betaH) * math.sinh(self._r)
        self._betaHP = self._betaH * math.cosh(self._r) + imag_exp( self._varphase) * conj(
            self._alphaV) * math.sinh(self._r)
        self._betaVP = self._betaV * math.cosh(self._r) + conj(self._alphaH) * math.sinh(self._r)
        self.entangledPair(canvas)

    # this type of entangled pair has the same polarization
    def downConvT1(self, canvas): # resulting matrices
        self._alphaHP = self._alphaH * math.cosh(self._r) + conj(self._betaH) * math.sinh(self._r)
        self._alphaVP = self._alphaV * math.cosh(self._r) + imag_exp( self._varphase) * conj(
            self._betaV) * math.sinh(self._r)
        self._betaHP = self._betaH * math.cosh(self._r) + conj(self._alphaH) * math.sinh(self._r)
        self._betaVP = self._betaV * math.cosh(self._r) + imag_exp( self._varphase) * conj(
            self._alphaV) * math.sinh(self._r)
        self.entangledPair(canvas)

    # creates an entangles pair of photons and shoots the visual components of that wave
    def entangledPair(self, canvas): # Creates two visual and properties (TimeSeg)
        # first photon
        directions=["LR", "LF", "LB", "FR", "BR", "BF"]
        emitAngs=[(UP,DOWN), (UP,RIGHT), (UP,LEFT), (RIGHT,DOWN), (LEFT,DOWN), (LEFT, RIGHT)]
        dir_index = directions.index(self._emitDirs)
        for i in range(6):
            if i == dir_index:
                self._aDirec = (emitAngs[i][0] + self._orientation) % 360
                self._bDirec = (emitAngs[i][1] + self._orientation) % 360
        #self._aDirec = (self._orientation - QUARTER)%360
        # if self._aDirec == FULL:
        #     self._aDirec = RIGHT
        a = TimeSeg(self._x, self._y, self._aDirec, self._alphaHP, self._alphaVP, canvas)
        TimeSeg.createWave(a, canvas, Laser.centeredLaser)
        # second photon
        # if self._emitAngle%180 == 90:
        #     self._bDirec = (self._orientation - HALF)%360
        # else:
        #     self._bDirec = (self._orientation + QUARTER)%360
        # if self._bDirec == -QUARTER:
        #     self._bDirec = DOWN
        b = TimeSeg(self._x, self._y, self._bDirec, self._betaHP, self._betaVP, canvas)
        TimeSeg.createWave(b, canvas, Laser.centeredLaser)

    # store waves to come back out when we begin going foward
    def useCompBack(self, wave, canvas, x, y, l):
        Laser.useCompBack(self, wave, canvas, x, y, l)
        return True


class Mirror(Cmpnts):
    # The orientation from ground has to be 0, 45, 90, or 135. This may be extended later
    def __init__(self, canvas, x, y, orientation = 0):
        super().__init__(x, y, orientation)
        possibleorientationations = [LEFT, DIAG, UP, ANTI, DOWN, RIGHT]
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a mirror must be an int (in degrees) '
                             + 'from the set {-135, -90, -45, 0, 45, 90, 135}. You tired: ' + str(orientation))
        components[self._y][self._x] = self
        canvas.comps.append(self)
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "Mirror.png")))

    # This method decides what will happen to the wave when it encounters a mirror
    def useComp(self, wave, canvas, x, y, l):
        blocked = ((self._orientation - wave._direction) % 180 == 0)
        if not blocked:
            Mirror.reflectWave(wave, self._orientation, canvas)
        if not canvas.noVisMode:
            canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))  # Changes color
        return blocked

    # this is the method used when a wave is reflected
    def reflectWave(wave, direc, canvas):
        # this is used in the BS to check when we need to add
        # a negative to the output
        """ # BRL
        factor = -1
        if direc == HORZ or direc == VERT:
            wave._direction = wave._direction - 180
            if wave._direction == - 90:
                wave._direction = DOWN
            wave._direction = abs(wave._direction)
        else:
            # apply -1 to both parts of the wave
            wave._vComp *= -1
            wave._hComp *= -1
            if direc == DIAG:
                factor = 1
            else:
                factor = -1
            if wave._direction == RIGHT or wave._direction == LEFT:
                factor *= 1
            else:
                factor *= -1
            wave._direction += 90 * factor
            # make sure our direction didnt go over 360 or under 0
            wave._direction = wave._direction % FULL
        """ # BRL
        phi = direc % 180 # orientation of mirror
        theta = wave._direction % 360 # direction wave is traveling
        if phi == HORZ or phi == VERT:
            factor = 0 # neither a left nor right turn
            wave._direction = (theta - 180) % 360
        else: # phi == DIAG or phi == ANTI
            if phi == DIAG:
                if theta == RIGHT or theta == LEFT:
                    factor = -1 # left turn
                    wave._direction = (theta + 90) % 360
                else: # theta == UP or theta == DOWN
                    factor = +1 # right turn
                    wave._direction = (theta - 90) % 360
            else: # phi == ANTI:
                if theta == RIGHT or theta == LEFT:
                    factor = +1 # right turn
                    wave._direction = (theta - 90) % 360
                else: # theta == UP or theta == DOWN
                    factor = -1 # left turn
                    wave._direction = (theta + 90) % 360
        # BRL
        TimeSeg.speed(wave, canvas)
        return factor

    # used when stepping back
    def useCompBack(self, wave, canvas, x, y, l):
        Mirror.reflectWave(wave, self._orientation, canvas)


class NeutralDensityFilter(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0, optical_density = 10):
        # makes default orientation to vertical being 0 without changing original math
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation + 90) % 180
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a NDF must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
                               'You tired: ' + str(orientation))
        self._d = optical_density
        components[self._y][self._x] = self
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "NDF.png")))
        canvas.comps.append(self)

    # decreases the intensity of light by a factor give by the user
    def useComp(self, wave, canvas, x, y, l):
        # for the sake of using the components, the orientationation can be adjusted
        # since the orientationation for 0, 180 are the same and 90, 270 are the same
        self._orientation = self._orientation % HALF
        if (wave._direction + QUARTER) % HALF == self._orientation:
            wave.hBefore.append(wave._hComp)
            wave.vBefore.append(wave._vComp)
            if wave.hAfter != []:
                # we have gone in reverse so we need to get the old wave
                wave._hComp = wave.hAfter.pop()
                wave._vComp = wave.vAfter.pop()
            else:
                factor = 10 ** (-self._d / 2)
                wave._hComp *= factor
                wave._vComp *= factor
                # Destroy part of wave introduces a new vacuum component
                a = Cmpnts.createVacMode()
                b = Cmpnts.createVacMode()
                # if(canvas.noNoise == True):
                #     a = 0
                #     b = 0
                wave._hComp += a
                wave._vComp += b
            if not canvas.noVisMode:
                canvas.grid.itemconfig(l, fill=TimeSeg.color(wave)) # Changes color
            return False
        else:
            return True

    # used when stepping back to undo intensity reduction
    def useCompBack(self, wave, canvas, x, y, l):
        # go back to the state of the wave before it was filtered
        wave.hAfter.append(wave._hComp)
        wave.vAfter.append(wave._vComp)
        wave._hComp = wave.hBefore.pop()
        wave._vComp = wave.vBefore.pop()
        if not canvas.noVisMode:
            canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))


# angle=0,    phase=0:     H polarizer
# angle=180,  phase=0:     V polarizer
# angle=90,   phase=0:     D polarizer
# angle=90,   phase=180:   A polarizer
# angle=90,   phase=90:    R polarizer
# angle=90,   phase=-90:   L polarizer
class Polarizer(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0, angle = 0, phase = 0): # angle and phase determine polarizer
        # makes default orientation to vertical being 0 without changing original math
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation + 90) % 180
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a polarizer must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
                               'You tired: ' + str(orientation))
        self._angle = math.radians(angle)
        self._phase = math.radians(phase)
        components[self._y][self._x] = self
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "Polarizer.png")))
        if self._orientation == VERT:
            self._vis2 = self.orientationIndicator(canvas, self._scalX + 20, 'black', self._angle)
            self._vis3 = self.orientationIndicator(canvas, self._scalX + 25, 'grey', self._phase)
        else:
            self._vis2 = self.orientationIndicator(canvas, self._scalY + 20, 'black', self._angle)
            self._vis3 = self.orientationIndicator(canvas, self._scalY + 25, 'grey', self._phase)
        canvas.comps.append(self)

    # Apply a polarizing filter according to the input parameters.
    def useComp(self, wave, canvas, x, y, l):
        # for the sake of using the components, the orientationation can be adjusted
        # since the orientationation for 0, 180 are the same and 90, 270 are the same
        self._orientation = self._orientation % HALF
        if (wave._direction + QUARTER) % HALF == self._orientation:
            wave.hBefore.append(wave._hComp)
            wave.vBefore.append(wave._vComp)
            if wave.hAfter != []:
                # we have gone in reverse so we need to get back the old wave
                wave._hComp = wave.hAfter.pop()
                wave._vComp = wave.vAfter.pop()
            else:
                angle = self._angle
                phase = self._phase
                h = wave._hComp
                v = wave._vComp
                wave._hComp = h * math.cos(angle)**2 + v * imag_exp(-1 *phase)*math.sin(2*angle)/2
                wave._vComp = h * imag_exp(phase)*math.sin(2*angle)/2 + v * math.sin(angle)**2
                a = Cmpnts.createVacMode()
                b = Cmpnts.createVacMode()
                if (canvas.noNoise == True):
                    a = 0
                    b = 0
                wave._hComp +=  a * math.sin(angle)**2 - b * imag_exp(-1 *phase)*math.sin(2*angle)/2
                wave._vComp += -a * imag_exp(phase)*math.sin(2*angle)/2 + b * math.cos(angle)**2
            if not canvas.noVisMode:
                canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))
            return False
        else:
            return True

    # used to undo polarization when stepping back
    def useCompBack(self, wave, canvas, x, y, l):
        # go back to the state of the wave before it was polarized
        wave.hAfter.append(wave._hComp)
        wave.vAfter.append(wave._vComp)
        wave._hComp = wave.hBefore.pop()
        wave._vComp = wave.vBefore.pop()
        if not canvas.noVisMode:
            canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))

    # draws a line on the filter to act as a visual for the angle and phase angles
    def orientationIndicator(self, canvas, str, color, anglInRad):
        degree = math.degrees(anglInRad) % 180
        pixFromTop = pixPerDegree * degree
        # place the indicators based on the orientationation of the component
        if self._orientation == VERT:
            obj = canvas.grid.create_line(str, self._scalY + pixFromTop, str + 5, self._scalY + pixFromTop,
                                     fill=color, width=5)
        elif self._orientation == HORZ:
            obj = canvas.grid.create_line(self._scalX + pixFromTop, str, self._scalX + pixFromTop, str + 5,
                                     fill=color, width=5)
        return obj

    # bings the component in front of the wave
    def bringForward(self, canvas):
        if not canvas.noVisMode:
            canvas.grid.tag_raise(self._vis)
            canvas.grid.tag_raise(self._vis2)
            canvas.grid.tag_raise(self._vis3)


class PhaseDelay(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0, phase = 0): # angle and phase determine polarizer
        # makes default orientation to vertical being 0 without changing original math
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation + 90) % 360
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a polarizer must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
                               'You tired: ' + str(orientation))
        self._phase = phase % 360
        components[self._y][self._x] = self
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "PhaseDelay.png")))
        if self._orientation == VERT :
            self._vis2 = self.orientationIndicator(canvas)
        else:
            self._vis2 = self.orientationIndicator(canvas)
        canvas.comps.append(self)

    # Apply a polarizing filter according to the input parameters.
    def useComp(self, wave, canvas, x, y, l):
        # for the sake of using the components, the orientationation can be adjusted
        # since the orientationation for 0, 180 are the same and 90, 270 are the same
        self._orientation = self._orientation % HALF
        if (wave._direction + QUARTER) % HALF == self._orientation:
            wave.hBefore.append(wave._hComp)
            wave.vBefore.append(wave._vComp)
            if wave.hAfter != []:
                # we have gone back so we need to get the old wave
                wave._hComp = wave.hAfter.pop()
                wave._vComp = wave.vAfter.pop()
            else:
                if (canvas.debug == True):
                    # let the user know the phase is being changed
                    print('before phase', wave._hComp, wave._vComp)
                    print('phase', imag_exp( self._phase * math.pi / 180))
                wave._hComp *= imag_exp( self._phase * math.pi / 180)
                wave._vComp *= imag_exp( self._phase * math.pi / 180)
                if (canvas.debug == True):
                    print('after phase ', wave._hComp, wave._vComp)
                    print()
            if not canvas.noVisMode:
                canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))
            return False
        else:
            return True

    # used to undo polarization when stepping back
    def useCompBack(self, wave, canvas, x, y, l):
        # go back to the state of the wave before we changed its phase
        wave.hAfter.append(wave._hComp)
        wave.vAfter.append(wave._vComp)
        wave._hComp = wave.hBefore.pop()
        wave._vComp = wave.vBefore.pop()
        if not canvas.noVisMode:
            canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))

        # draws a line on the filter to act as a visual for the angle and phase angles

    # red horizontal line that indicates what the phase of the phase delay is
    def orientationIndicator(self, canvas):
        degree = self._phase
        pixPerDeg = 50 / 360
        scale =pixPerDeg * degree
        if(degree < 170):
            l = [5 - scale / 5, 3.5]
            width = min(l)
        else:
            l = [2.5 + scale / 5, 9]
            width = max(l)
        pixFromTop = pixPerDeg * degree
        if self._orientation == UP:
            obj = canvas.grid.create_line(self._scalX + 20 + width, self._scalY + pixFromTop, self._scalX + 30 - width,
                                     self._scalY + pixFromTop, fill='red', width=5)
        elif self._orientation == DOWN:
            obj = canvas.grid.create_line(self._scalX + 20 + width, self._scalY - 50 + pixFromTop, self._scalX + 30 - width,
                                     self._scalY + pixFromTop - 50, fill='red', width=5)
        elif self._orientation == RIGHT:
            obj = canvas.grid.create_line(self._scalX + pixFromTop - 50,self._scalY + 20 + width, self._scalX + pixFromTop -50,
                                     self._scalY + 30 - width, fill='red', width=5)
        elif self._orientation == LEFT:
            obj = canvas.grid.create_line(self._scalX + pixFromTop,self._scalY + 20 + width, self._scalX + pixFromTop,
                                     self._scalY + 30 - width, fill='red', width=5)
        return obj

    # bring forward visualization
    def bringForward(self, canvas):
        if not canvas.noVisMode:
            canvas.grid.tag_raise(self._vis)
            canvas.grid.tag_raise(self._vis2)


class QuarterWavePlate(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0, angle = 0):
        # makes default orientation to vertical being 0 without changing original math
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation + 90) % 180
        angle = angle % 180
        self._pixFromTop = pixPerDegree * angle
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a QWP must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
                               'You tired: ' + str(orientation))
        self._angle = math.radians(angle)
        components[self._y][self._x] = self
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "QWP.png")))
        self._vis2 = self.angleIndicator(canvas)
        canvas.comps.append(self)

    # how a quarter wave plate is applied to a wave. The matrix I use is from Jones Calculus which represents
    # a quarter wave plate with fast axis angle with respect to the horizontal
    def useComp(self, wave, canvas, x, y, l):
        # for the sake of using the components, the orientationation can be adjusted
        # since the orientationation for 0, 180 are the same and 90, 270 are the same
        self._orientation = self._orientation % HALF
        if (wave._direction + QUARTER) % HALF == self._orientation:
            wave.hBefore.append(wave._hComp)
            wave.vBefore.append(wave._vComp)
            if wave.hAfter != []:
                wave._hComp = wave.hAfter.pop()
                wave._vComp = wave.vAfter.pop()
            else:
                M = [[0, 0], [0, 0]]
                angle = self._angle
                M[0][0] = math.cos(angle)**2 + 1j*math.sin(angle)**2
                M[1][0] = (1 - 1j)/2 * math.sin(2*angle)
                M[0][1] = (1 - 1j)/2 * math.sin(2*angle)
                M[1][1] = math.sin(angle)**2 + 1j*math.cos(angle)**2
                TimeSeg.martixMult(wave, M)
            if not canvas.noVisMode:
                canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))
            return False
        else:
            return True

    # used to undo the rotation when going back
    def useCompBack(self, wave, canvas, x, y, l):
        wave.hAfter.append(wave._hComp)
        wave.vAfter.append(wave._vComp)
        wave._hComp = wave.hBefore.pop()
        wave._vComp = wave.vBefore.pop()
        if not canvas.noVisMode:
            canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))

    # draws a line on the plate to act as a visual for what the fast axis angle is
    def angleIndicator(self, canvas):
        # print(self._orientation, VERT, HORZ)
        if self._orientation == VERT:
            obj = canvas.grid.create_line(self._scalX + 20, self._scalY + self._pixFromTop, self._scalX + 30, self._scalY + self._pixFromTop,
                                     fill='black', width=5)
        elif self._orientation == HORZ:
            obj = canvas.grid.create_line(self._scalX + self._pixFromTop, self._scalY + 20, self._scalX + self._pixFromTop, self._scalY + 30,
                                     fill='black', width=5)
        return obj

    # bings the component in front of the wave
    def bringForward(self, canvas):
        if not canvas.noVisMode:
            canvas.grid.tag_raise(self._vis)
            canvas.grid.tag_raise(self._vis2)


class HalfWavePlate(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0, angle = 0):
        # makes default orientation to vertical being 0 without changing original math
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation + 90) % 180
        angle = angle % 180
        self._pixFromTop = pixPerDegree * angle
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a HWP must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
                               'You tired: ' + str(orientation))
        self._angle = math.radians(angle)
        components[self._y][self._x] = self
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "HWP.png")))
        self._vis2 = QuarterWavePlate.angleIndicator(self, canvas)
        canvas.comps.append(self)

    # how a half wave plate is applied to a wave. The matrix I use is from Jones Calculus which represents
    # a half wave plate with fast axis angle with respect to the horizontal
    def useComp(self, wave, canvas, x, y, l):
        # for the sake of using the components, the orientationation can be adjusted
        # since the orientationation for 0, 180 are the same and 90, 270 are the same
        self._orientation = self._orientation % HALF
        if (wave._direction + QUARTER) % HALF == self._orientation:
            wave.hBefore.append(wave._hComp)
            wave.vBefore.append(wave._vComp)
            if wave.hAfter != []:
                wave._hComp = wave.hAfter.pop()
                wave._vComp = wave.vAfter.pop()
            else:
                M = [[0, 0], [0, 0]]
                angle = self._angle
                M[0][0] = math.cos(2*angle)
                M[1][0] = math.sin(2*angle)
                M[0][1] = math.sin(2*angle)
                M[1][1] = -math.cos(2*angle)
                TimeSeg.martixMult(wave, M)
            if not canvas.noVisMode:
                canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))
            return False
        else:
            return True

    # used to undo the rotation when going back
    def useCompBack(self, wave, canvas, x, y, l):
        wave.hAfter.append(wave._hComp)
        wave.vAfter.append(wave._vComp)
        wave._hComp = wave.hBefore.pop()
        wave._vComp = wave.vBefore.pop()
        if not canvas.noVisMode:
            canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))

    # brings foward the visual component on top of the wave
    def bringForward(self, canvas):
        if not canvas.noVisMode:
            canvas.grid.tag_raise(self._vis)
            canvas.grid.tag_raise(self._vis2)


class BeamSplitter(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0, reflectivity = 0.5):
        # this makes 135 from horizontal the default without having to change original math done
        # makes default orientation to vertical being 0 without changing original math
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation + ANTI) % 180
        possibleorientationations = [LEFT, DIAG, UP, ANTI, DOWN, RIGHT]
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a beamsplitter must be an int (in degrees) '
                             + 'from the set {-135, -90, -45, 0, 45, 90, 135}. You tired: ' + str(orientation))
        if reflectivity < 0:
            raise ValueError('The reflectivity value for a beamsplitter must be an int greater than or equal to zero. '
                             + ' You tried: ' + str(reflectivity))
        self._reflectivity = reflectivity
        self._checked = False
        self._skip = False
        self.inputs = []
        self.outputs = []
        self.oneOrTwo = []
        self.oneOrTwoRev = []
        self._shoot = True
        self._vis = self.visualPictureBS(canvas, os.path.join(imgPath, "BeamSplit-Flat.png"),
                                         os.path.join(imgPath, "BeamSplit-NotFlat.png"))
        components[self._y][self._x] = self
        canvas.beamSplitters.append(self)
        canvas.comps.append(self)

    # What happends to the timeSeg of the wave as it goes through a beam splitter.
    # The wave will be split into two parts that are set using the r squared of the beamsplitter
    def useComp(self, wave, canvas, x, y, l):
        blocked = ((self._orientation - wave._direction) % 180 == 0)
        if not blocked:
            wave.recalVals(x, y)
            self.inputs.append(deepcopy(wave))
            if self.outputs != []:
                oneOrTwo = 2
                if self._shoot:
                    oneOrTwo = BeamSplitter.getReversedWave(self, canvas)
                else:
                    self._shoot = True
                if self.outputs == [] and oneOrTwo == 2:
                    self._shoot = False
                canvas.waveSegs.remove(wave)
                if not canvas.noVisMode:
                    canvas.waveVis.remove(l)
                    canvas.grid.delete(l)
                return False
            elif self._shoot:
                if(canvas.debug == True):
                    print('before', wave._hComp, wave._vComp, canvas.beamSplitters.index(self))
                self.getNewWave(wave, canvas, x, y, l)
                return False
            elif not self._shoot:
                self._shoot = True
        return True

    # if there has been a step back, the output was stored so we need to get the stored output and make it the new
    # output
    def getReversedWave(self, canvas):
        oneOrTwo = self.oneOrTwoRev.pop()
        if oneOrTwo == 1:
            self._shoot = True
        elif oneOrTwo == 2:
            self._shoot = False
        self.oneOrTwo.append(oneOrTwo)
        self.oneOrTwo.append(self.oneOrTwoRev.pop())
        wave1 = self.outputs.pop()
        TimeSeg.createWave(wave1, canvas, Laser.centeredLaser)
        wave2 = self.outputs.pop()
        TimeSeg.createWave(wave2, canvas, Laser.centeredLaser)
        self.bringForward(canvas)
        self._checked = True
        return oneOrTwo

    # if there are no stored waves, we will use this method to create the second output
    def getNewWave(self, wave, canvas, x, y, l):
        wave._originalDir = wave._direction
        factor = Mirror.reflectWave(wave, self._orientation, canvas)
        reflH = wave._hComp * math.sqrt(self._reflectivity) # BRL * -1
        reflV = wave._vComp * math.sqrt(self._reflectivity) # BRL * -1
        splitPart = TimeSeg(wave._x, wave._y, wave._direction, reflH, reflV, canvas)
        obj = PolarizingBeamSplitter.newWave(splitPart, canvas, x, y)
        self.bringForward(canvas)
        wave._hComp = factor * math.sqrt(1 - self._reflectivity) * wave._hComp
        wave._vComp = factor * math.sqrt(1 - self._reflectivity) * wave._vComp
        wave._direction = wave._originalDir
        if not canvas.noVisMode:
            if splitPart._direction - 180 == wave._direction or splitPart._direction + 180 == wave._direction:
                canvas.grid.tag_lower(obj)
        TimeSeg.speed(wave, canvas)
        self._checked = False
        canvas.splitCheckWaves.append(wave)
        if not canvas.noVisMode:
            canvas.splitCheckVis.append(l)
            canvas.splitCheckVis.append(obj)
        canvas.splitCheckWaves.append(splitPart)
        if (canvas.debug == True):
            print('after', wave._hComp, wave._vComp, splitPart._hComp, splitPart._vComp, canvas.beamSplitters.index(self))
            print()

    # used to but the wave back together when stepping back
    def useCompBack(self, wave, canvas, x, y, l):
        wave.recalVals(x, y)
        self.outputs.append(deepcopy(wave))
        oneOrTwo = self.oneOrTwo.pop()
        self.oneOrTwoRev.append(oneOrTwo)
        if not self._skip:
            newWave = self.inputs.pop()
            canvas.waveSegs.append(newWave)
            obj = Laser.centeredLaser(canvas, newWave)
            if not canvas.noVisMode:
                canvas.grid.itemconfig(obj, fill=TimeSeg.color(newWave))
                canvas.waveVis.append(obj)
                canvas.grid.move(obj, -1 * newWave._xSpeed, -1 * newWave._ySpeed)
            else:
                newWave._scalX += -1 * newWave._xSpeed
                newWave._scalY += -1 * newWave._ySpeed
            self.bringForward(canvas)
        if oneOrTwo == 1:
            self._skip = True
        elif oneOrTwo == 2:
            self._skip = False
        return True


class PolarizingBeamSplitter(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0, basis = "HV"):
        # this makes 135 from horizontal the default without having to change original math done
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation + 135) % 180
        self.basis = basis.upper()
        possibleorientationations = [LEFT, DIAG, UP, ANTI, DOWN, RIGHT]
        possiblemodes = ["HV", "VH", "DA", "AD", "RL", "LR"]
        if self.basis not in possiblemodes:
            raise ValueError('The basis for a polarizing beamsplitter must be one of the following : ["HV", "VH", "DA", "AD", "RL", "LR"]'
                             '. You tried: ' + self.basis)
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a polarizing beamsplitter must be an int (in degrees) '
                             + 'from the set {-135, -90, -45, 0, 45, 90, 135}. You tired: ' + str(orientation))
        self._checked = False
        self.inputs = []
        self.outputs = []
        self.oneOrTwo = []
        self.oneOrTwoRev = []
        self._skip = False
        self._shoot = True
        self._vis = self.visualPictureBS(canvas, os.path.join(imgPath, "PolarBeamSplit-Flat.png"),
                                         os.path.join(imgPath, "PolarBeamSplit-NotFlat.png"))
        components[self._y][self._x] = self
        canvas.comps.append(self)
        canvas.beamSplitters.append(self)

    # what happens to the timeSeg of the wave as it goes through a polarizing beamsplitter.
    # The wave will be split into its horizontal and vertical components. The horizontal
    # component of the wave is trasmitted while the vertical is reflected.
    def useComp(self, wave, canvas, x, y, l):
        block = BeamSplitter.useComp(self, wave, canvas, x, y, l)
        return block

    # if there are no waves that are in storage, create the second output with this method
    def getNewWave(self, wave, canvas, x, y, l):
        wave._originalDir = wave._direction
        Mirror.reflectWave(wave, self._orientation, canvas)
        # now we need to do the correct transformation based on the polarization
        if self.basis == "HV" or self.basis == "VH":
            splitH = 0
            splitV = wave._vComp * -1
            waveH = wave._hComp * -1
            waveV = 0
        elif self.basis == "DA" or self.basis == "AD":
            splitH = (wave._hComp - wave._vComp) * 1/2
            splitV = (wave._hComp - wave._vComp) * - 1/2
            waveH = (wave._hComp - wave._vComp) * 1/2
            waveV = waveH
        elif self.basis == "RL" or self.basis == "LR":
            # this one is spicey
            splitH = (wave._hComp + wave._vComp * complex(0, 1)) * 1/2
            splitV = splitH * complex(0, -1)
            waveH = (wave._hComp + wave._vComp * complex(0, -1)) * 1/2
            waveV = waveH * complex(0, 1)
        # this will be the same no matter the mode that we are in
        splitPart = TimeSeg(wave._x, wave._y, wave._direction, splitH, splitV, canvas)
        obj = PolarizingBeamSplitter.newWave(splitPart, canvas, x, y)
        self.bringForward(canvas)
        wave._direction = wave._originalDir
        if not canvas.noVisMode:
            if splitPart._direction - 180 == wave._direction or splitPart._direction + 180 == wave._direction:
                canvas.grid.tag_lower(obj)
        wave._hComp = waveH
        wave._vComp = waveV
        canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))
        TimeSeg.speed(wave, canvas)
        canvas.splitCheckWaves.append(wave)
        canvas.splitCheckVis.append(l)
        canvas.splitCheckWaves.append(splitPart)
        canvas.splitCheckVis.append(obj)
        self._checked = False
        if (canvas.debug == True):
            print('after', wave._hComp, wave._vComp, splitPart._hComp, splitPart._vComp, canvas.beamSplitters.index(self))
            print()

    # used to put the wave back together when stepping back
    def useCompBack(self, wave, canvas, x, y, l):
        BeamSplitter.useCompBack(self, wave, canvas, x, y, l)
        return True

    # creates the new visual of the split part of the wave and adds it to the array to check if there is more than one
    # input
    def newWave(wave, canvas, x, y):
        thickness = wave._thick
        diff = thickness / 2
        canvas.waveSegs.append(wave)
        if not canvas.noVisMode:
            if wave._direction == LEFT or wave._direction == RIGHT:
                obj = canvas.grid.create_line(x * 50 + 25 - diff, y * 50 + 25, x * 50 + 25 + diff, y * 50 + 25,
                                         fill=wave._color, width=thickness)
            elif wave._direction == UP or wave._direction == DOWN:
                obj = canvas.grid.create_line(x * 50 + 25 - diff, y * 50 + 25, x * 50 + 25 + diff, y * 50 + 25,
                                         fill=wave._color, width=thickness)
            canvas.waveVis.append(obj)
            return obj
        return None


# class SingleModeFiber(Cmpnts):
#     # orientation start and stop must be 0, 90, 180, 270 and we assume that the wire will be straight
#     def __init__(self, canvas, x_start, y_start, x_stop, y_stop, orientation_start, orientation_stop):
#         self._orientation_start = orientation_start % 360
#         self._orientation_stop = orientation_stop % 360
#         possibleorientationations = [LEFT, UP, RIGHT, DOWN]
#         if (type(self._orientation_start) != int or not (self._orientation_stop in possibleorientationations) or not
#         (self._orientation_start in possibleorientationations)):
#             raise ValueError('The orientation for the beginning and end of a SMF must be an int (in degrees) '
#                              + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
#                                'You tired: beginning orientationaion = ' + str(orientation_start) + ", ending orientation = "
#                              + str(orientation_stop))
#         self.checkXandY(x_start, y_start)
#         self.checkXandY(x_stop, y_stop)
#         self._x_start = x_start
#         self._y_start = y_start
#         self._x_stop = x_stop
#         self._y_stop = y_stop
#         self._by_start = self._y_start
#         self._by_stop = self._y_stop
#         components[self._by_start][self._x_start] = self
#         components[self._by_stop][self._x_stop] = self
#         self._angle = math.radians(randrange(360))
#         self._phase = math.radians(randrange(360))
#         self._lamb = math.radians(randrange(360))
#         canvas.comps.append(self)
#         self._points = self.pointToArray()
#         self._length = math.sqrt((self._points[6] - self._points[0]) ** 2 + (self._points[6] - self._points[1]) ** 2)
#         self._pauseLength = int(self._length / 5)
#         self._vis = canvas.grid.create_line(self._points, splinesteps=100000, smooth=True, width=7, fill="#CD853F")
#
#     # used to check if the starting and stopping positions are in the correct range
#     def checkXandY(self, x, y):
#         if type(x) != int or type(y) != int or x > WIDTHB or y > HEIGHTB or x < 0 or y < 0:
#             raise ValueError(
#                 'x and y coordinates must be integers in the domain [0, 17]. You tried: x = ' + str(x) + ', y = ' + str(
#                     y))
#
#     def pointToArray(self):  # Points for spline fit
#         pointStart = []
#         pointStop = []
#         if self._orientation_start == 0 or self._orientation_start == 180:
#             point1 = [self._x_start * scFac, self._by_start * scFac + 25]
#             point2 = [self._x_start * scFac + 50, self._by_start * scFac + 25]
#             if self._orientation_start == 0:
#                 pointStart = point2 + point1
#                 self._x_startCheck = point2[0] - 5
#                 self._y_startCheck = point2[1]
#             elif self._orientation_start == 180:
#                 pointStart = point1 + point2
#                 self._x_startCheck = point1[0] + 5
#                 self._y_startCheck = point1[1]
#             if self._y_start < self._y_stop:
#                 pointStart += [self._x_start * scFac + 25, self._by_start * scFac, self._x_start * scFac + 25,
#                                self._by_start * scFac + 50]
#             elif self._y_start > self._y_stop:
#                 pointStart += [self._x_start * scFac + 25, self._by_start * scFac + 50, self._x_start * scFac + 25,
#                                self._by_start * scFac]
#             else:
#                 midX = (self._x_start * scFac + self._x_stop * scFac) / 2
#                 midY = (self._by_start * scFac + self._by_stop * scFac) / 2 + 25
#                 pointStart += [midX, midY, midX, midY]
#             # self.horzorientationStartEnd(pointStart)
#         elif self._orientation_start == 90 or self._orientation_start == 270:
#             point1 = [self._x_start * scFac + 25, self._by_start * scFac]
#             point2 = [self._x_start * scFac + 25, self._by_start * scFac + 50]
#             if self._orientation_start == 90:
#                 pointStart = point1 + point2
#                 self._x_startCheck = point1[0]
#                 self._y_startCheck = point1[1] + 5
#             elif self._orientation_start == 270:
#                 pointStart = point2 + point1
#                 self._x_startCheck = point2[0]
#                 self._y_startCheck = point2[1] - 5
#             if self._x_start > self._x_stop:
#                 pointStart += [self._x_start * scFac + 50, self._by_start * scFac + 25, self._x_start * scFac,
#                                self._by_start * scFac + 25]
#             elif self._x_start < self._x_stop:
#                 pointStart += [self._x_start * scFac, self._by_start * scFac + 25, self._x_start * scFac + 50,
#                                self._by_start * scFac + 25]
#             else:
#                 midX = (self._x_start * scFac + self._x_stop * scFac) / 2 + 25
#                 midY = (self._by_start * scFac + self._by_stop * scFac) / 2
#                 pointStart += [midX, midY, midX, midY]
#             # self.vertorientationStartEnd(pointStart)
#         if self._orientation_stop == 0 or self._orientation_stop == 180:
#             point1 = [self._x_stop * scFac, self._by_stop * scFac + 25]
#             point2 = [self._x_stop * scFac + 50, self._by_stop * scFac + 25]
#             if self._y_stop < self._y_start:
#                 pointStop += [self._x_stop * scFac + 25, self._by_stop * scFac + 50, self._x_stop * scFac + 25,
#                               self._by_stop * scFac]
#             elif self._y_stop > self._y_start:
#                 pointStop += [self._x_stop * scFac + 25, self._by_stop * scFac, self._x_stop * scFac + 25,
#                               self._by_stop * scFac + 50]
#             else:
#                 midX = (self._x_start * scFac + self._x_stop * scFac) / 2
#                 midY = (self._by_start * scFac + self._by_stop * scFac) / 2 + 25
#                 pointStart += [midX, midY, midX, midY]
#             if self._orientation_stop == 0:
#                 pointStop += point1 + point2
#                 self._x_stopCheck = point2[0] - 5
#                 self._y_stopCheck = point2[1]
#             elif self._orientation_stop == 180:
#                 pointStop += point2 + point1
#                 self._x_stopCheck = point1[0] + 5
#                 self._y_stopCheck = point1[1]
#             # self.horzorientationStopEnd(pointStart, pointStop)
#         elif self._orientation_stop == 90 or self._orientation_stop == 270:
#             point1 = [self._x_stop * scFac + 25, self._by_stop * scFac]
#             point2 = [self._x_stop * scFac + 25, self._by_stop * scFac + 50]
#             if self._x_stop > self._x_start:
#                 pointStop += [self._x_stop * scFac, self._by_stop * scFac + 25, self._x_stop * scFac + 50,
#                               self._by_stop * scFac + 25]
#             elif self._x_stop < self._x_start:
#                 pointStop += [self._x_stop * scFac + 50, self._by_stop * scFac + 25, self._x_stop * scFac,
#                               self._by_stop * scFac + 25]
#             else:
#                 midX = (self._x_start * scFac + self._x_stop * scFac) / 2 + 25
#                 midY = (self._by_start * scFac + self._by_stop * scFac) / 2
#                 pointStart += [midX, midY, midX, midY]
#             if self._orientation_stop == 90:
#                 pointStop += point2 + point1
#                 self._x_stopCheck = point1[0]
#                 self._y_stopCheck = point1[1] + 5
#             elif self._orientation_stop == 270:
#                 pointStop += point1 + point2
#                 self._x_stopCheck = point2[0]
#                 self._y_stopCheck = point2[1] - 5
#             # self.vertorientationStopEnd(pointStart, pointStop)
#         points = pointStart + pointStop
#         return points
#
#     # points for SMF if the starting end is horizontal
#     def horzorientationStartEnd(self, pointStart):
#         point1 = [self._x_start * scFac, self._by_start * scFac + 25]
#         point2 = [self._x_start * scFac + 50, self._by_start * scFac + 25]
#         if self._orientation_start == 0:
#             pointStart = point2 + point1
#             self._x_startCheck = point2[0] - 5
#             self._y_startCheck = point2[1]
#         elif self._orientation_start == 180:
#             pointStart = point1 + point2
#             self._x_startCheck = point1[0] + 5
#             self._y_startCheck = point1[1]
#         if self._y_start > self._y_stop:
#             pointStart = [self._x_start * scFac + 25, self._by_start * scFac, self._x_start * scFac + 25,
#                            self._by_start * scFac + 50]
#         elif self._y_start < self._y_stop:
#             pointStart = [self._x_start * scFac + 25, self._by_start * scFac + 50, self._x_start * scFac + 25,
#                            self._by_start * scFac]
#         else:
#             midX = (self._x_start * scFac + self._x_stop * scFac) / 2
#             midY = (self._by_start * scFac + self._by_stop * scFac) / 2 + 25
#             pointStart += [midX, midY, midX, midY]
#
#     # points for SMF if the starting end is vertical
#     def vertorientationStartEnd(self, pointStart):
#         point1 = [self._x_start * scFac + 25, self._by_start * scFac]
#         point2 = [self._x_start * scFac + 25, self._by_start * scFac + 50]
#         if self._orientation_start == 90:
#             pointStart = point1 + point2
#             self._x_startCheck = point1[0]
#             self._y_startCheck = point1[1] + 5
#         elif self._orientation_start == 270:
#             pointStart = point2 + point1
#             self._x_startCheck = point2[0]
#             self._y_startCheck = point2[1] - 5
#         if self._x_start > self._x_stop:
#             pointStart += [self._x_start * scFac + 50, self._by_start * scFac + 25, self._x_start * scFac,
#                            self._by_start * scFac + 25]
#         elif self._x_start < self._x_stop:
#             pointStart += [self._x_start * scFac, self._by_start * scFac + 25, self._x_start * scFac + 50,
#                            self._by_start * scFac + 25]
#         else:
#             midX = (self._x_start * scFac + self._x_stop * scFac) / 2 + 25
#             midY = (self._by_start * scFac + self._by_stop * scFac) / 2
#             pointStart += [midX, midY, midX, midY]
#
#     # points for SMF if the stopping end is horizontal
#     def horzorientationStopEnd(self, pointStop):
#         point1 = [self._x_stop * scFac, self._by_stop * scFac + 25]
#         point2 = [self._x_stop * scFac + 50, self._by_stop * scFac + 25]
#         if self._y_stop > self._y_start:
#             pointStop += [self._x_stop * scFac + 25, self._by_stop * scFac + 50, self._x_stop * scFac + 25,
#                           self._by_stop * scFac]
#         elif self._y_stop < self._y_start:
#             pointStop += [self._x_stop * scFac + 25, self._by_stop * scFac, self._x_stop * scFac + 25,
#                           self._by_stop * scFac + 50]
#         else:
#             midX = (self._x_start * scFac + self._x_stop * scFac) / 2
#             midY = (self._by_start * scFac + self._by_stop * scFac) / 2 + 25
#             # pointStart += [midX, midY, midX, midY]
#         if self._orientation_stop == 0:
#             pointStop += point1 + point2
#             self._x_stopCheck = point2[0] - 5
#             self._y_stopCheck = point2[1]
#         elif self._orientation_stop == 180:
#             pointStop += point2 + point1
#             self._x_stopCheck = point1[0] + 5
#             self._y_stopCheck = point1[1]
#
#     # point for SMF if the stopping end is vertical
#     def vertorientationStopEnd(self, pointStop):
#         point1 = [self._x_stop * scFac + 25, self._by_stop * scFac]
#         point2 = [self._x_stop * scFac + 25, self._by_stop * scFac + 50]
#         if self._x_stop > self._x_start:
#             pointStop += [self._x_stop * scFac, self._by_stop * scFac + 25, self._x_stop * scFac + 50,
#                           self._by_stop * scFac + 25]
#         elif self._x_stop < self._x_start:
#             pointStop += [self._x_stop * scFac + 50, self._by_stop * scFac + 25, self._x_stop * scFac,
#                           self._by_stop * scFac + 25]
#         else:
#             midX = (self._x_start * scFac + self._x_stop * scFac) / 2 + 25
#             midY = (self._by_start * scFac + self._by_stop * scFac) / 2
#             # pointStart += [midX, midY, midX, midY]
#         if self._orientation_stop == 90:
#             pointStop += point2 + point1
#             self._x_stopCheck = point1[0]
#             self._y_stopCheck = point1[1] + 5
#         elif self._orientation_stop == 270:
#             pointStop += point1 + point2
#             self._x_stopCheck = point2[0]
#             self._y_stopCheck = point2[1] - 5
#
#     # when a wave gets to a single mode fiber, if it is in the correct orientation it will travel along
#     # the fiber and it will have some random self._unitary applied to it then it will be sent in the
#     # final orientation of the fiber
#     def useComp(self, wave, canvas, x, y, orientationStart, orientationStop, l):
#         if wave._direction + 180 == orientationStart or wave._direction - 180 == orientationStart:
#             if wave._pause == False:
#                 wave._pause = True
#                 if not canvas.noVisMode:
#                     canvas.grid.tag_lower(l)
#                 wave._count = 0
#                 wave._xSpeed = 0
#                 wave._ySpeed = 0
#                 wave.hBefore.append(wave._hComp)
#                 wave.vBefore.append(wave._vComp)
#             else:
#                 wave._count += 1
#             if wave._count > self._pauseLength:
#                 TimeSeg.applyUnitary(wave, self._angle, self._lamb, self._phase)
#                 splitPart = TimeSeg(int(self._points[x] / scFac), int(self._points[y] / scFac), orientationStop,
#                                     wave._hComp, wave._vComp, canvas)
#                 splitPart.hBefore = wave.hBefore.copy()
#                 splitPart.vBefore = wave.vBefore.copy()
#                 canvas.waveSegs.append(splitPart)
#                 SingleModeFiber.outgoingWave(canvas, splitPart)
#                 self.bringForward(canvas)
#                 canvas.waveSegs.remove(wave)
#                 if not canvas.noVisMode:
#                     canvas.waveVis.remove(l)
#                     canvas.grid.delete(l)
#             return False
#         else:
#             return True
#
#     # used to undo the random unitary operation when stepping back
#     def useCompBack(self, wave, canvas, x, y, orientationStart, orientationStop, l):
#         if wave._pause == False:
#             wave._pause = True
#             if not canvas.noVisMode:
#                 canvas.grid.tag_lower(l)
#             wave._count = self._pauseLength - 1
#             wave._xSpeed = 0
#             wave._ySpeed = 0
#         else:
#             wave._count -= 1
#         if wave._count < 0:
#             wave._hComp = wave.hBefore.pop(0)
#             wave._vComp = wave.vBefore.pop(0)
#             splitPart = TimeSeg(int(self._points[x] / scFac), int(self._points[y] / scFac), orientationStop,
#                                 wave._hComp, wave._vComp, canvas)
#             splitPart.hBefore = wave.hBefore.copy()
#             splitPart.vBefore = wave.vBefore.copy()
#             splitPart._xSpeed = -1 *  splitPart._xSpeed
#             splitPart._ySpeed = -1 * splitPart._ySpeed
#             canvas.waveSegs.append(splitPart)
#             SingleModeFiber.outgoingWave(canvas, splitPart)
#             self.bringForward(canvas)
#             canvas.waveSegs.remove(wave)
#             if not canvas.noVisMode:
#                 canvas.waveVis.remove(l)
#                 canvas.grid.delete(l)
#
#     # wave coming out of the fiber
#     def outgoingWave(canvas, wave):
#         if not canvas.noVisMode:
#             thickness = wave._thick
#             diff = thickness / 2
#             if wave._direction == RIGHT:
#                 canvas.waveVis.append(canvas.grid.create_line(wave._scalX - diff, wave._scalY + 25, wave._scalX + diff,
#                                                          wave._scalY + 25, fill=wave._color, width=thickness))
#             elif wave._direction == UP:
#                 canvas.waveVis.append(canvas.grid.create_line(wave._scalX + 25 - diff, wave._scalY, wave._scalX + 25 + diff,
#                                                          wave._scalY, fill=wave._color, width=thickness))
#             elif wave._direction == LEFT:
#                 canvas.waveVis.append(canvas.grid.create_line(wave._scalX - diff, wave._scalY + 25, wave._scalX + diff,
#                                                          wave._scalY + 25, fill=wave._color, width=thickness))
#             elif wave._direction == DOWN:
#                 canvas.waveVis.append(canvas.grid.create_line(wave._scalX + 25 - diff, wave._scalY, wave._scalX + 25 + diff,
#                                                          wave._scalY, fill=wave._color, width=thickness))


class PowerMeter(Cmpnts):
    # orientation is 0, 90, 180, 270 based on the propagation direction you want to measure.
    # For example to measure a wave moving right you input zero while to measure a wave moving down you input 270
    def __init__(self, canvas, x, y):
        # this is just so that we can still use the constructor for components
        orientation = 0
        super().__init__(x, y, orientation)
        self._power = 0
        self.image = Image.open(os.path.join(imgPath, "PM.png"))
        self.vis = ImageTk.PhotoImage(self.image)
        self._vis = canvas.grid.create_image(self._centerX, self._centerY, image=self.vis)
        self._label = Label(canvas.root, text=('0nW'), fg="Blue", height=1, width=6, font=("Helvetica", 6))
        canvas.grid.create_window(x * scFac + 24, self._y * scFac + 18, window=self._label)
        self._used = False
        self.deletedHereWave = []
        self.rounded = []
        self.readings = []
        self.perTimeStep = []
        self.notFixed = 0
        components[self._y][self._x] = self
        canvas.comps.append(self)
        canvas.powerMeters.append(self)
        self.back = False

    # this is how a power meter will measure the power of a wave that passes through it
    # our default wavelength is 785 nanometers
    def useComp(self, wave, canvas, x, y, l):
        if self.back and len(self.readings) != (len(canvas.timeStamps) - 1):
            self.rounded.pop()
            self.readings.pop()
            self.back = False
        self.multiple = False
        if self._used:
            self.multiple = True
        self._used = True
        self.powerCalc(wave)
        self._label.configure( text=(str(round(self._power)) + "" + self._unit))
        wave.recalVals(x, y)
        self.rounded.append(str((round(self._power))) + "" + self._unit)
        self.deletedHereWave.append(deepcopy(wave))
        # this is how I will keep track of how many waves went through a power meter at a given time so that we can
        # be sure to bring all of them back when we go in reverse
        if self.multiple:
            self.perTimeStep[-1] += 1
        else:
            self.perTimeStep.append(1)
        return True

    # brings back waves that were measured and measures the power of the wave brought back when stepping back
    def useCompBack(self, canvas):
        self.back = True
        if self.deletedHereWave != []:
            self.rounded.pop()
            self.readings.pop()
            for i in range(self.perTimeStep[-1]):
                # we need to bring back as many waves as the number of was in the perTimeStep list
                wave = self.deletedHereWave.pop(-1)
                if wave != '':
                    canvas.waveSegs.append(wave)
                    obj = Laser.centeredLaser(canvas, wave)
                    if not canvas.noVisMode:
                        canvas.grid.itemconfig(obj, fill=TimeSeg.color(wave))
                        canvas.waveVis.append(obj)
                        canvas.grid.move(obj, -1 * wave._xSpeed, -1 * wave._ySpeed)
                    else:
                        wave._scalX += -1 * wave._xSpeed
                        wave._scalY += -1 * wave._ySpeed
                self.bringForward(canvas)
        if self.deletedHereWave == []:
            if self.readings != []:
                reading = self.rounded.pop()
                self.readings.pop()
            else:
                reading = ("0nW")
        else:
            reading = self.rounded[-2]
        self._label.configure( text=(reading))

    def useDark(self):
        pass
        # hComp = Cmpnts.createVacMode()
        # vComp = Cmpnts.createVacMode()
        # B = (abs(hComp)) ** 2 + (abs(vComp)) ** 2
        # S = B * 1e6
        # lamb = 496.61e-9
        # h = 6.62607004e-34
        # c = 299792458
        # self._power = (h * c * S) / lamb
        # self.readings.append(self._power)
        # self.unit()
        # self._label.configure(text=(('%4.1f ' % self._power) + self._unit))

    # calculate the self._power
    def powerCalc(self, wave):
        hComp = wave._hComp
        vComp = wave._vComp
        # B is bin, S is segment of time
        B = (abs(hComp)) ** 2 + (abs(vComp)) ** 2
        S = B * 1e6
        lamb = 496.61e-9
        h = 6.62607004e-34
        c = 299792458
        newPower = (h * c * S) / lamb
        if newPower < 1e-9:
            newPower = 0
        if self.multiple:
            self._power = max(newPower, self.notFixed)
            self.notFixed = self._power
            self.unit()
            self.readings[-1] = self._power
            self.rounded[-1] = str((round(self._power))) + "" + self._unit
        else:
            self._power = newPower
            self.notFixed = self._power
            self.unit()
            self.readings.append(self._power)
            self.rounded.append(str((round(self._power))) + "" + self._unit)

    # get the correct self._unit for the self._power
    def unit(self):
        self._unit = 'W'
        if self._power < 1e-9:
            self._power = 0
            self._unit = 'nW'
        elif self._power < 1e-6:
            self._power /= 1e-9
            self._unit = 'nW'
        elif self._power < 1e-3:
            self._power /= 1e-6
            self._unit = 'μW'
        elif self._power < 1:
            self._power /= 1e-3
            self._unit = 'mW'


class Detector(Cmpnts):
    # orientation is 0, 90, 180, 270 based on the probogation directetion you want to measure
    # for example to measure a wave moving right you input zero while to measure
    # a wave moving down you input 270
    def __init__(self, canvas, x, y, orientation = 0, dark_count_rate = 1, probability_dark_count = -1):
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        super().__init__(x, y, orientation)
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a detector must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
                               'You tried: ' + str(orientation))
        if dark_count_rate <= 0:
            dark_count_rate = 1
        elif dark_count_rate > 1000:
            dark_count_rate = 1000
        self._dark_count_rate = dark_count_rate
        self._count = 0
        self._invldMes = 0
        self.deletedHereWave = []
        self.countAtMove = []
        self._used = False
        self._detections = []
        self._wasThereCount = False
        self._probability_dark_count = probability_dark_count
        # self._probability_dark_count = probability_dark_count
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "Det.png")))
        self._vis2 = self.light(canvas, 'black')
        self._label = Label(canvas.root, text='0 cnts', fg="Blue", height=1, width=5, font=("Helvetica", 7))
        components[self._y][self._x] = self
        canvas.detectors.append(self)
        canvas.comps.append(self)
        self.placeLabel(canvas)

    # place the label on the decector that will read when there is a count
    def placeLabel(self, canvas):
        canvas.grid.create_window(self._x * scFac + 24, self._y * scFac + 18, window=self._label)
        if self._orientation == 180:
            canvas.grid.create_window(self._x * scFac + 25, self._y * scFac + 50, window=self._label)
        elif self._orientation == 270:
            canvas.grid.create_window(self._x * scFac + 25, self._y * scFac + 20, window=self._label)
        elif self._orientation == 0:
            canvas.grid.create_window(self._x * scFac + 25, self._y * scFac + 45, window=self._label)
        elif self._orientation == 90:
            canvas.grid.create_window(self._x * scFac + 25, self._y * scFac + 45, window=self._label)

    # if the wave is traveling in the direction that the detector was set to dectec then it will attempt
    # to be measured if not that wave is blocked. Either way the wave is deleted from the list of waves
    def useComp(self, wave, canvas, x, y, l):
        self._used = True
        if wave._direction == self._orientation + 180 or wave._direction == self._orientation - 180:
            if self._probability_dark_count != -1:
                gamma = math.sqrt(-1 / 2 * math.log(1 - math.sqrt(1 - self._probability_dark_count)))
                intensityH = (abs(wave._hComp)) ** 2
                intensityV = (abs(wave._vComp)) ** 2
                if intensityH > gamma ** 2 or intensityV > gamma ** 2:
                    self.countDetected(canvas)
                else:
                    self._invldMes += 1
                    canvas.grid.itemconfig(self._vis2, fill='black')
                    self._wasThereCount = False
                    self.countAtMove.append('I')
                    self._detections.append(" ")
            else:
                gamma_squared = - 1 / 2 * math.log(1 - math.sqrt(1 - self._dark_count_rate/1000))
                intensityH = (abs(wave._hComp)) ** 2
                intensityV = (abs(wave._vComp)) ** 2
                if intensityH > gamma_squared or intensityV > gamma_squared:
                    self.countDetected(canvas)
                else:
                    self._invldMes += 1
                    canvas.grid.itemconfig(self._vis2, fill='black')
                    self._wasThereCount = False
                    self.countAtMove.append('I')
                    self._detections.append(" ")
        self._label.configure(text=str(self._count) + " cnts")
        wave.recalVals(x, y)
        self.deletedHereWave.append(deepcopy(wave))
        return True

    # if the detector is not used then it checks if there is a dark count
    def darkCounts(self, canvas):  # Creates vacuum mode, adds count if high enough
        if (canvas.noNoise == False):
            noiseH = Cmpnts.createVacMode()
            noiseV = Cmpnts.createVacMode()
            intensityH = (abs(noiseH)) ** 2
            intensityV = (abs(noiseV)) ** 2
            if self._probability_dark_count != -1:
                gamma = math.sqrt(-1 / 2 * math.log(1 - math.sqrt(1 - self._probability_dark_count)))
                if intensityH > gamma ** 2 or intensityV > gamma ** 2:
                    self.countDetected(canvas)
                else:
                    canvas.grid.itemconfig(self._vis2, fill='black')
                    self._wasThereCount = False
                    self.countAtMove.append('N')
                    self._detections.append(" ")
            else:
                gamma_squared = - 1 / 2 * math.log(1 - math.sqrt(1 - self._dark_count_rate/1000))
                if intensityH > gamma_squared or intensityV > gamma_squared:
                    self.countDetected(canvas)
                else:
                    canvas.grid.itemconfig(self._vis2, fill='black')
                    self._wasThereCount = False
                    self.countAtMove.append('N')
                    self._detections.append(" ")
            self.deletedHereWave.append('')
            self._label.configure(text=str(self._count) + " cnts")

    # if there is a count detected, we incriment the total number of counts
    # and set wasThereCount to true and append C to count at move
    def countDetected(self, canvas):
        self._count += 1
        canvas.grid.itemconfig(self._vis2, fill='yellow')
        self._detections.append("C")
        self._wasThereCount = True
        self.countAtMove.append('C')

    # used to bring back a measured wave and see if that wave made a count when stepping back
    def useCompBack(self, canvas):
        if self.deletedHereWave != []:
            last = len(self.deletedHereWave) - 1
            wave = self.deletedHereWave.pop(last)
            count = self.countAtMove.pop(last)
            self._detections.pop()
            if count == 'C':
                self._count -= 1
            elif count == 'I':
                self._invldMes -= 1
            self._label.configure(text=str(self._count) + " cnts")
            if wave != '':
                canvas.waveSegs.append(wave)
                obj = Laser.centeredLaser(canvas, wave)
                if not canvas.noVisMode:
                    canvas.grid.itemconfig(obj, fill=TimeSeg.color(wave))
                    canvas.waveVis.append(obj)
                self.bringForward(canvas)
                if self.countAtMove == [] or self.countAtMove[last - 1] == 'I' or self.countAtMove[last - 1] == 'N':
                    canvas.grid.itemconfig(self._vis2, fill='black')
                elif self.countAtMove[last - 1] == 'C':
                    canvas.grid.itemconfig(self._vis2, fill='yellow')
                if not canvas.noVisMode:
                    canvas.grid.move(obj, -1 * wave._xSpeed, -1 * wave._ySpeed)
                else:
                    wave._scalX += -1 * wave._xSpeed
                    wave._scalY += -1 * wave._ySpeed
            else:
                canvas.grid.itemconfig(self._vis2, fill='black')

    # bring the decector in front of the wave
    def bringForward(self, canvas):
        if not canvas.noVisMode:
            canvas.grid.tag_raise(self._vis)
            canvas.grid.tag_raise(self._vis2)

    # old way of printing out the detection results
    # # prints the total counts for each category, and how long the simulation would have run in real time
    # def printResult(self, canvas):
    #     index = canvas.detectors.index(self)
    #     print("Detector", (index+1))
    #     #print("Number of counts:", self._count)
    #     print(self._detections)


# not to use these anymore because results will be printed out with the all possible combinations
# of the detectors
class CoincidenceCounter(Cmpnts):
    # the index of det one and two will be based off of 1 being the first detector, not zero
    def __init__(self, canvas, detector_one, detector_two):
        self._counts = 0
        self.countAtMove = []
        self._dets = canvas.detectors.copy()
        try:
            self._detOne = canvas.detectors[detector_one - 1]
            self._detTwo = canvas.detectors[detector_two - 1]
        except:
            raise ValueError('Please select two detectors that are defied. The detectors are numbered in the order you '
                             'defined them with 1 being the first one you defined. You tried detectors: ' + str(detector_one)
                             + ", " + str(detector_two))
        self._dets.remove(self._detOne)
        self._dets.remove(self._detTwo)
        self._detOne.bringForward(canvas)
        self._detTwo.bringForward(canvas)
        canvas.conCounters.append(self)

    # check to see if there was a coincidence between the two specified detectors
    def checkCoincidence(self):
        if (self._detOne._wasThereCount and self._detTwo._wasThereCount) == True:
            count = False
            i = 0
            while i < len(self._dets) and count == False:
                count = self._dets[i]._wasThereCount == True
                i+= 1
            if count == False:
                self._counts += 1
                self.countAtMove.append('C')
            else:
                self.countAtMove.append('N')
        else:
            self.countAtMove.append('N')

    # check to see if there was a coincidence when going back in time
    def checkBack(self, canvas): # Rewind
        if self.countAtMove == []:
            pass
        else:
            count = self.countAtMove.pop()
            if count == 'C':
                self._counts -= 1

    # # prints the total counts for each category
    def printResult(self, canvas):
        index = canvas.conCounters.index(self)
        print("Coincidence Counter", (index + 1))
        print("Number of counts:", self._counts, "\n")


class BeamBlocker(Cmpnts):
    # orientation is 0, 90, 180, 270 based on the propagation direction you want to measure.
    # For example to measure a wave moving right you input zero while to measure a wave moving down you input 270
    def __init__(self, canvas, x, y):
        # this is just so that we can still use the constructor for components
        orientation = 0
        super().__init__(x, y, orientation)
        self.image = Image.open(os.path.join(imgPath, "BeamBlocker.png"))
        self.vis = ImageTk.PhotoImage(self.image)
        self._vis = canvas.grid.create_image(self._centerX, self._centerY, image=self.vis)
        self.deletedHereWave = []
        components[self._y][self._x] = self
        canvas.comps.append(self)
        canvas.beamblockers.append(self)

    # this is how a power meter will measure the power of a wave that passes through it
    # our default wavelength is 785 nanometers
    def useComp(self, wave, canvas, x, y, l):
        wave.recalVals(x, y)
        self.deletedHereWave.append(deepcopy(wave))
        return True

    # brings back waves that were measured and measures the power of the wave brought back when stepping back
    def useCompBack(self, canvas):
        self.back = True
        if self.deletedHereWave != []:
            wave = self.deletedHereWave.pop(-1)
            if wave != '':
                canvas.waveSegs.append(wave)
                obj = Laser.centeredLaser(canvas, wave)
                if not canvas.noVisMode:
                    canvas.grid.itemconfig(obj, fill=TimeSeg.color(wave))
                    canvas.waveVis.append(obj)
                    canvas.grid.move(obj, -1 * wave._xSpeed, -1 * wave._ySpeed)
                else:
                    wave._scalX += -1 * wave._xSpeed
                    wave._scalY += -1 * wave._ySpeed
                self.bringForward(canvas)


class Rotator(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0, angle = 0):
        # makes default orientation to vertical being 0 without changing original math
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation + 90) % 180
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a polarizer must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
                               'You tired: ' + str(orientation))
        self._angle = angle % 360
        angle = self._angle % 180
        self._pixFromTop = pixPerDegree * angle
        components[self._y][self._x] = self
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "Rotator.png")))
        self._vis2 = QuarterWavePlate.angleIndicator(self, canvas)
        canvas.comps.append(self)

    # Apply a polarizing filter according to the input parameters.
    def useComp(self, wave, canvas, x, y, l):
        # for the sake of using the components, the orientationation can be adjusted
        # since the orientationation for 0, 180 are the same and 90, 270 are the same
        self._orientation = self._orientation % HALF
        if wave._direction % 180 == self._orientation % 180:
            wave.hBefore.append(wave._hComp)
            wave.vBefore.append(wave._vComp)
            if wave.hAfter != []:
                # we have gone back so we need to get the old wave
                wave._hComp = wave.hAfter.pop()
                wave._vComp = wave.vAfter.pop()
            else:
                U = [[math.cos(self._angle), -math.sin(self._angle)], [math.sin(self._angle), math.cos(self._angle)]]
                wave.martixMult(U)
            if not canvas.noVisMode:
                canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))
            return False
        else:
            return True

    # used to undo polarization when stepping back
    def useCompBack(self, wave, canvas, x, y, l):
        # go back to the state of the wave before we changed its phase
        wave.hAfter.append(wave._hComp)
        wave.vAfter.append(wave._vComp)
        wave._hComp = wave.hBefore.pop()
        wave._vComp = wave.vBefore.pop()
        if not canvas.noVisMode:
            canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))

        # draws a line on the filter to act as a visual for the angle and phase angles

    # bring forward visualization
    def bringForward(self, canvas):
        if not canvas.noVisMode:
            canvas.grid.tag_raise(self._vis)
            canvas.grid.tag_raise(self._vis2)


class PhaseRetarder(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0, phase = 0):
        # makes default orientation to vertical being 0 without changing original math
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation + 90) % 360
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a polarizer must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
                               'You tired: ' + str(orientation))
        self._phase = phase % 360
        angle = self._phase % 180
        self._pixFromTop = pixPerDegree * angle
        components[self._y][self._x] = self
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "PhaseRetarder.png")))
        self._vis2 = QuarterWavePlate.angleIndicator(self, canvas)
        canvas.comps.append(self)

    # Apply a polarizing filter according to the input parameters.
    def useComp(self, wave, canvas, x, y, l):
        # for the sake of using the components, the orientationation can be adjusted
        # since the orientationation for 0, 180 are the same and 90, 270 are the same
        self._orientation = self._orientation % HALF
        if (wave._direction + QUARTER) % HALF == self._orientation:
            wave.hBefore.append(wave._hComp)
            wave.vBefore.append(wave._vComp)
            if wave.hAfter != []:
                # we have gone back so we need to get the old wave
                wave._hComp = wave.hAfter.pop()
                wave._vComp = wave.vAfter.pop()
            else:
                wave._vComp *= imag_exp(self._phase * math.pi / 180)
            if not canvas.noVisMode:
                canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))
            return False
        else:
            return True

    # used to undo polarization when stepping back
    def useCompBack(self, wave, canvas, x, y, l):
        # go back to the state of the wave before we changed its phase
        wave.hAfter.append(wave._hComp)
        wave.vAfter.append(wave._vComp)
        wave._hComp = wave.hBefore.pop()
        wave._vComp = wave.vBefore.pop()
        if not canvas.noVisMode:
            canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))

        # draws a line on the filter to act as a visual for the angle and phase angles

    # bring forward visualization
    def bringForward(self, canvas):
        if not canvas.noVisMode:
            canvas.grid.tag_raise(self._vis)
            canvas.grid.tag_raise(self._vis2)


class Depolarizer(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0):
        # makes default orientation to vertical being 0 without changing original math
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation + 90) % 360
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a polarizer must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
                               'You tired: ' + str(orientation))
        components[self._y][self._x] = self
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "Depolarizer.png")))
        canvas.comps.append(self)

    # Apply a polarizing filter according to the input parameters.
    def useComp(self, wave, canvas, x, y, l):
        # for the sake of using the components, the orientationation can be adjusted
        # since the orientationation for 0, 180 are the same and 90, 270 are the same
        self._orientation = self._orientation % HALF
        if (wave._direction + QUARTER) % HALF == self._orientation:
            wave.hBefore.append(wave._hComp)
            wave.vBefore.append(wave._vComp)
            if wave.hAfter != []:
                # we have gone back so we need to get the old wave
                wave._hComp = wave.hAfter.pop()
                wave._vComp = wave.vAfter.pop()
            else:
                angle = math.radians(randrange(360))
                phase = math.radians(randrange(360))
                lamb = math.radians(randrange(360))
                TimeSeg.applyUnitary(wave, angle, lamb, phase)
            if not canvas.noVisMode:
                canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))
            return False
        else:
            return True

    # used to undo polarization when stepping back
    def useCompBack(self, wave, canvas, x, y, l):
        # go back to the state of the wave before we changed its phase
        wave.hAfter.append(wave._hComp)
        wave.vAfter.append(wave._vComp)
        wave._hComp = wave.hBefore.pop()
        wave._vComp = wave.vBefore.pop()
        if not canvas.noVisMode:
            canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))

        # draws a line on the filter to act as a visual for the angle and phase angles

    # bring forward visualization
    def bringForward(self, canvas):
        if not canvas.noVisMode:
            canvas.grid.tag_raise(self._vis)


class Dephaser(Cmpnts):
    def __init__(self, canvas, x, y, orientation = 0): # angle and phase determine polarizer
        # makes default orientation to vertical being 0 without changing original math
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation + 90) % 180
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a polarizer must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
                               'You tired: ' + str(orientation))
        components[self._y][self._x] = self
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "Dephaser.png")))
        canvas.comps.append(self)

    # Apply a dephaser according to random phi.
    def useComp(self, wave, canvas, x, y, l):
        # for the sake of using the components, the orientationation can be adjusted
        # since the orientationation for 0, 180 are the same and 90, 270 are the same
        self._orientation = self._orientation % HALF
        if (wave._direction + QUARTER) % HALF == self._orientation:
            wave.hBefore.append(wave._hComp)
            wave.vBefore.append(wave._vComp)
            if wave.hAfter != []:
                # we have gone back so we need to get the old wave
                wave._hComp = wave.hAfter.pop()
                wave._vComp = wave.vAfter.pop()
            else:
                if (canvas.debug == True):
                    # let the user know the phase is being changed
                    print('before phase', wave._hComp, wave._vComp)
                phase = uniform(0, 1) * 2 * math.pi
                print("before", wave._hComp, wave._vComp)
                wave._hComp *= imag_exp(phase)
                wave._vComp *= imag_exp(phase)
                print(wave._hComp, wave._vComp)
                if (canvas.debug == True):
                    print('after phase ', wave._hComp, wave._vComp)
                    print()
            if not canvas.noVisMode:
                canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))
            return False
        else:
            return True

    # used to undo phase change when stepping back
    def useCompBack(self, wave, canvas, x, y, l):
        # go back to the state of the wave before we changed its phase
        wave.hAfter.append(wave._hComp)
        wave.vAfter.append(wave._vComp)
        wave._hComp = wave.hBefore.pop()
        wave._vComp = wave.vBefore.pop()
        if not canvas.noVisMode:
            canvas.grid.itemconfig(l, fill=TimeSeg.color(wave))

    # bring forward visualization
    def bringForward(self, canvas):
        if not canvas.noVisMode:
            canvas.grid.tag_raise(self._vis)


class TimeDelay(Cmpnts):
    def __init__(self, canvas, x, y, orientation=0, delay = 0):
        # makes default orientation to vertical being 0 without changing original math
        possibleorientationations = [UP, DOWN, LEFT, RIGHT]
        # print(x, y)
        super().__init__(x, y, orientation)
        self._orientation = (self._orientation ) % 180
        if delay < 0:
            delay = 1
        self._delay = delay
        if type(self._orientation) != int or not (self._orientation in possibleorientationations):
            raise ValueError('The orientation for a polarizer must be an int (in degrees) '
                             + 'from the set {-360, -270, -180, -90, 0, 90, 180, 270, 360}. '
                               'You tired: ' + str(orientation))
        components[self._y][self._x] = self
        # TODO: CHANGE PICTURE
        self._vis = self.visualPictureFlat(canvas, Image.open(os.path.join(imgPath, "TimeDelay.png")))
        canvas.comps.append(self)

    # hold the waves for a delay
    def useComp(self, wave, canvas, x, y, l):
        if wave._direction % 180 == self._orientation % 180:
            
            if wave._pause == False:
                wave._pause = True
                if not canvas.noVisMode:
                    canvas.grid.tag_lower(l)
                wave._count = 0
                wave._storeX = wave._xSpeed
                wave._storeY = wave._ySpeed
                wave._xSpeed = 0
                wave._ySpeed = 0
                wave.hBefore.append(wave._hComp)
                wave.vBefore.append(wave._vComp)
            else:
                wave._count += 1
            if wave._count > self._delay:
                wave._xSpeed = wave._storeX
                wave._ySpeed = wave._storeY
                wave._pause = False
                # if not canvas.noVisMode:
                #     canvas.grid.tag_raise(l)
                self.bringForward(canvas)
            return False
        return True

    # hold in reverse
    def useCompBack(self, wave, canvas, x, y, l):
        if wave._direction == self._orientation + 180 or wave._direction == self._orientation - 180:
            if wave._pause == False:
                wave._pause = True
                if not canvas.noVisMode:
                    canvas.grid.tag_lower(l)
                wave._count = self._pauseLength - 1
                wave._storeX = wave._xSpeed
                wave._storeY = wave._ySpeed
                wave._xSpeed = 0
                wave._ySpeed = 0
            else:
                wave._count -= 1
            if wave._count < 0:
                wave._xSpeed = wave._storeX
                wave._ySpeed = wave._storeY
                wave._pause = False
        self.bringForward(canvas)

    # bring forward visualization
    def bringForward(self, canvas):
            if not canvas.noVisMode:
                canvas.grid.tag_raise(self._vis)


def conj(num):
    conjg = num.real + -1 * num.imag * 1j
    return conjg


def imag_exp(num):
    result = math.cos(num) + 1j * math.sin(num)
    return result

