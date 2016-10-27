#Models Tetris; each game will reference one tetrisGrid object

import tetrisController
import random

class tetrisGrid:

    """
    A tetrisGrid is represented by a matrix of either 0 indicating and empty
    space or a color value 1-7
    _________________
    |...0123456789...|
    |..____________..|
    |19|..........|  |
    |18|...3......|  |
    |17|..333.....|  |
    |16|..........|  |
    | -| - - - - -| -|
    |01|...77.....|  |
    |00|..772222..|  |
    |..|__________|  |
    |___0123456789___|

    TODO: 
    <> Implement score keeping
    <> Implement Levels
    """
    colors = {"black": 0, "red": 1, "green": 2, "yellow": 3, "blue": 4, "magenta": 5, "cyan": 6, "white": 7}
    #Cardinal directions, clockwise from North
    dirN = 0
    dirE = 1
    dirS = 2
    dirW = 3

    def __init__(self, controller):
        self.controller = controller
        self.debug = True
        self.score = 0
        self.level = 0
        self.gameOver = False
        self.grid = [[0 for i in range(10)] for i in range(20)]
        self.nextBlock = Block()
        self.currentBlock = self.nextBlock
        self.setNextBlock()
        #self.printd("MODEL CREATED")
        #self.controller.printd("FOO")

    def getGrid(self):
        """
        returns a representation of the game grid
        """
        return self.grid

    def setNextBlock(self):
        """
        Sets the current block to the next block, and puts it in the grid.
        If we cannot place a new block, the game is over.
        """
        self.currentBlock = self.nextBlock
        self.controller.notifyViewLinesRemoved(self.lineScan())
        self.nextBlock = Block()
        collision = self.collisionCheck(self.currentBlock.location)
        if not collision:
            self.__setLoc__(self.currentBlock.location, self.currentBlock.color)
        else:
            self.gameOver = True
            self.controller.notifyViewGameOver()
        return not collision
        
    def lineScan(self):
        """
        Scan for complete lines and remove them. Should only be called
        after a block has come to rest. Returns a list of indeces of removed lines
        """
        toRemove = []

        for i in range(20):
            full = True
            for box in self.grid[i]:
                if not box:
                    full = False
                    break
            if full:
                toRemove += [i]

        toreturn = toRemove
        #print("LINES TO REMOVE: " + str(toRemove))
        while(toRemove):
            #self.printd("ENTER REMOVE LOOP")
            k = toRemove.pop()
            self.grid = self.grid[:k] + self.grid[k+1:]
            self.grid += [[0 for i in range(10)]]
        #self.printd("LINES REMOVED: " + str(toreturn))
        return toreturn

    def rotateBlock(self, rot="cw"):
        """
        Rotate the current block either clockwise (cw) or counterclockwise (cc)
        """
        oldloc = self.currentBlock.location
        self.__clearLoc__(oldloc)
        newloc = self.currentBlock.rotate(rot, False)
        collision = self.collisionCheck(newloc)
        if not collision:
            #self.__clearLoc__(self.currentBlock.location)
            self.currentBlock.rotate(rot, True)
            self.__setLoc__(self.currentBlock.location, self.currentBlock.color)
        else:
            self.__setLoc__(oldloc, self.currentBlock.color)
        return not collision

    def progressBlock(self):
        """
        Guides the current block on its journey ever downward.
        If the block lands on something we ditch it and add the next block
        """
        moved = self.moveBlock(self.dirS)
        if not moved:
            self.setNextBlock()
        return moved

    def dropBlock(self):
        """
        Drop the block until it comes to rest
        """
        x, y = self.currentBlock.origin
        oldloc = self.currentBlock.location
        self.__clearLoc__(oldloc)
        newloc = self.currentBlock.moveTo( (x, y-1), False)
        while( not self.collisionCheck(newloc)):
            x, y = x, y-1
            newloc = self.currentBlock.moveTo( (x, y-1), False)
        #self.__clearLoc__(self.currentBlock.location)
        self.currentBlock.moveTo( (x, y), True)
        self.__setLoc__(self.currentBlock.location, self.currentBlock.color)
        self.setNextBlock()

    def moveBlock(self, drr):
        """
        Moves block by given cardinal drrection drr
        Returns True or False based on successful move.
        """
        oldloc = self.currentBlock.location
        self.__clearLoc__(oldloc)
        newloc = self.currentBlock.step(drr, False)
        collision = self.collisionCheck(newloc)
        #self.printd("BLOCK MOVED: " + str(not collision))
        if not collision:
            #self.__clearLoc__(self.currentBlock.location)
            self.currentBlock.step(drr, True)
            self.__setLoc__(self.currentBlock.location, self.currentBlock.color)
        else:
            self.__setLoc__(oldloc, self.currentBlock.color)
        return not collision

    def collisionCheck(self, loc):
        """
        Returns True if a block in loc would cause a colision, and False otherwise
        """
        for point in loc:
            x, y = point
            if not 0 <= x < 10 or not 0 <= y < 20:
                #self.printd("COLLISION: OUT-OF-BOUNDS")
                return True
            #if not self.valAtPoint(*point) == 0:
            if not self.valAtPoint(*point) == 0:
                #self.printd("COLLISION: POINT OCCUPIED")
                return True
        return False

    def valAtPoint(self, x, y):
        """
        Wrapper so we can use x, y coordinates
        """
        return self.grid[y][x]

    def printd(self, str):
        if self.debug: self.controller.printd(str)

    def __clearLoc__(self, loc):
        for point in loc:
            x, y = point
            self.grid[y][x] = 0

    def __setLoc__(self, loc, color):
        for point in loc:
            x, y = point
            self.grid[y][x] = self.colors[color]
        

class Block:

    """
    shapes = {"left-el": [[0, 1, 0], [0, 1, 0], [1, 1, 0]],
              "right-el": [[0, 1, 0], [0, 1, 0], [0, 1, 1]],
              "z-block": [[0, 1, 0], [1, 1, 0], [1, 0, 0]],
              "s-block": [[0, 1, 0], [0, 1, 1], [0, 0, 1]],
              "square": [[0, 0, 0], [1, 1, 0], [1, 1, 0]],
              "t-block": [[0, 1, 0], [0, 1, 1], [0, 1, 0]],
              "line": [[0, 1, 0] for i in range(4)]
              }
    """
    """
    shapes = {"left-el": [(0, 0), (0, 1), (0, -1), (-1, -1)],
              "right-el": [(0, 0), (0, 1), (1, -1), (0, -1)],
              "z-block": [(0, 0), (0, 1), (-1, -1), (-1, 0)],
              "s-block": [(0, 0), (0, 1), (1, 0), (1, -1)],
              "square": [(0, 0), (0, 1), (1, 1), (1, 0)],
              "t-block": [(0, 0), (0, 1), (1, 0), (0, -1)],
              "line": [(0, 0), (0, 1), (0, -1), (0, -2)]
              }
    """

    shapes = {"left-el": [(0, 0), (-1, 0), (1, 0), (1, -1)],
              "right-el": [(0, 0), (-1, 0), (1, 0), (-1, -1)],
              "z-block": [(0, 0), (-1, 0), (0, -1), (1, -1)],
              "s-block": [(0, 0), (-1, -1), (0, -1), (1, 0)],
              "square": [(0, 0), (0, -1), (1, -1), (1, 0)],
              "t-block": [(0, 0), (-1, 0), (1, 0), (0, -1)],
              "line": [(0, 0), (-1, 0), (1, 0), (2, 0)]
              }

    colors = {"left-el": "blue",
              "right-el": "cyan",
              "z-block": "magenta",
              "s-block": "green",
              "square": "red",
              "t-block": "yellow",
              "line": "white"}

    dirN = 0
    dirE = 1
    dirS = 2
    dirW = 3
    
    def __init__(self):
        self.key = random.choice(self.shapes.keys())
        self.shape = self.shapes[self.key]
        self.color = self.colors[self.key]
        self.horizontal = False
        # (y, x) coordinates
        self.origin = (4, 19)
        self.__updateLocation__()
        """
        print "[] NEW BLOCK: ", self.key
        print "[] ORIGIN: ", self.origin
        print "[] LOCATION: ", self.location
        """

    def rotate(self, rot, commit):
        if rot == "cw":
            loc = self.__calculateRotate__("cw")
            if commit:
                self.shape = loc
                self.__updateLocation__()
                return self.location
            else:
                tmp = self.shape
                self.shape = loc
                toreturn = self.__calculateMove__(self.origin)
                self.shape = tmp
                return toreturn
        elif rot == "cc":
            loc = self.__calculateRotate__("cc")
            if commit:
                self.shape = loc
                self.__updateLocation__()
                return self.location
            else:
                tmp = self.shape
                self.shape = loc
                toreturn = self.__calculateMove__(self.origin)
                self.shape = tmp
                return toreturn
        else:
            return False

    def moveTo(self, coord, commit):
        if commit:
            self.origin = coord
            self.__updateLocation__()
            return self.location
        else:
            return self.__calculateMove__(coord)

    def step(self, drr, commit):
        if drr == self.dirN:
            coord = (self.origin[0], self.origin[1] + 1)
            toreturn = self.__calculateMove__(coord)
        elif drr == self.dirS:
            coord = (self.origin[0], self.origin[1] - 1)
            toreturn = self.__calculateMove__(coord)
        elif drr == self.dirE:
            coord = (self.origin[0] + 1, self.origin[1])
            toreturn = self.__calculateMove__(coord)
        elif drr == self.dirW:
            coord = (self.origin[0] - 1, self.origin[1])
            toreturn = self.__calculateMove__(coord)
        else:
            return False

        if commit:
            self.origin = coord
            self.__updateLocation__()
            return self.location
        else:
            return toreturn

    def __updateLocation__(self):
        #print "UPDATE LOCATION"
        self.location = self.__calculateMove__(self.origin)

    def __calculateMove__(self, coord):
        return [(point[0] + coord[0], point[1] + coord[1]) for point in self.shape]

    def __calculateRotate__(self, rot):
        if rot == "cw":
            new = self.__transpose__(self.shape)
            return [(point[0] * 1, point[1] * -1) for point in new]
        elif rot == "cc":
            new = self.__transpose__(self.shape)
            return [(point[0] * -1, point[1] * 1) for point in new]
        else:
            return False
        
    def __transpose__(self, points):
        return [(point[1], point[0]) for point in points]

#b = Block()
        
