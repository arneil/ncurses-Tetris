#Handles curses

import curses
import tetrisController

"""
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)

#curses.beep()

curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()
"""

class tetrisView:

    colors = {"black": 0, "red": 1, "green": 2, "yellow": 3, "blue": 4, "magenta": 5, "cyan": 6, "white": 7}
    block_shape = '-'
    keys = {curses.KEY_LEFT: "left",
            curses.KEY_RIGHT: "right",
            curses.KEY_UP: "up",
            curses.KEY_DOWN: "down",
            ord(' '): "space"
            }

    def __init__(self, controller, scr):
        self.controller = controller
        #print "INIT"
        self.stdscr = scr
        #y, x coords
        self.location = (3, 3)
        self.gameOver = False
        self.dIndex = 1
        self.initColor()
        self.drawFrame()
        self.drawNextBlockFrame()
        #self.drawInfo()
        self.hideCursor()
        #self.drawBoard()
        #self.drawDebug("VIEW CREATED")

    def linesRemoved(self, lines):
        pass

    def initColor(self):
        #curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_CYAN)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def drawGameOver(self):
        self.gameOver = True
        y, x = self.location
        y += 1; x += 1
        for dy in range(20):
            for dx in range(10):
                self.stdscr.addstr(y+dy, x+dx, '-')
        self.stdscr.addstr(y+9, x, "GAME OVER;")
        self.stdscr.addstr(y+10, x, "Q TO QUIT.")

    def passKey(self, key):
        self.controller.passKey(self.keys[key])

    def drawBoard(self):
        board = self.controller.getBoard()
        y, x = self.location
        y += 1; x += 1
        for dy in range(20):
            for dx in range(10):
                color = board[dy][dx]
                #Whoops, messed up coordinates. Duct tape conversion
                dy = -1*dy + 19
                if color == 0:
                    self.stdscr.addstr(y+dy, x+dx, ' ')
                else:
                    self.stdscr.addstr(y+dy, x+dx, self.block_shape, curses.color_pair(color))

    def drawFrame(self):
        #print "DRAW FRAME"
        y, x = self.location
        self.stdscr.addstr(y, x, '#')
        self.stdscr.addstr(y, x+11, '#')
        self.stdscr.addstr(y+21, x, '#')
        self.stdscr.addstr(y+21, x+11, '#')
        for i in range(10):
            self.stdscr.addstr(y, x+1+i, '=')
            self.stdscr.addstr(y+21, x+1+i, '=')
        for i in range(20):
            self.stdscr.addstr(y+1+i, x, '|')
            self.stdscr.addstr(y+1+i, x+11, '|')

    def drawNextBlockFrame(self):
        y, x = self.location
        x += 15
        self.stdscr.addstr(y, x, '#')
        self.stdscr.addstr(y, x+7, '#')
        self.stdscr.addstr(y+7, x, '#')
        self.stdscr.addstr(y+7, x+7, '#')
        for i in range(6):
            self.stdscr.addstr(y, x+1+i, '=')
            self.stdscr.addstr(y+7, x+1+i, '=')
        for i in range(6):
            self.stdscr.addstr(y+1+i, x, '|')
            self.stdscr.addstr(y+1+i, x+7, '|')

    def drawInfo(self):
        y, x = self.location
        x += 15; y += 9
        info = self.controller.getInfo()
        gameOver = info[0]
        score = info[1]
        level = info[2]
        block = info[3]
        self.stdscr.addstr(y, x, "Level: " + str(level))
        self.stdscr.addstr(y+1, x, "Score: " + str(score))
        self.drawNextBlock(block)
        if gameOver:
            self.gameOver = True
            self.drawGameOver()
        
    def drawNextBlock(self, block):
        self.__clearNextBlockFrame__()
        y, x = self.location
        x += 18; y += 3
        for point in block.shape:
            px, py = point
            self.stdscr.addstr(y+py, x+px, self.block_shape, curses.color_pair(self.colors[block.color]))

    def drawPause(self):
        y, x = self.location
        y += 1; x += 1
        for dy in range(20):
            for dx in range(10):
                self.stdscr.addstr(y+dy, x+dx, '-')
        self.stdscr.addstr(y+9, x, "==PAUSED==")

    def hideCursor(self):
        curses.curs_set(0)

    def cursesEnd(self):
        curses.nocbreak(); self.stdscr.keypad(0); curses.echo()
        curses.endwin()

    def drawDebug(self, str):
        y, x = 3, 30
        self.stdscr.addstr(y, x, "#=====DEBUG=====#")
        self.stdscr.addstr(y+self.dIndex, x, str + "     ")
        self.dIndex = max(1, (self.dIndex + 1) % 22)

    def linesRemoved(self, lines):
        pass

    def __clearNextBlockFrame__(self):
        y, x = self.location
        x += 16; y += 1
        for dy in range(6):
            for dx in range(6):
                self.stdscr.addstr(y+dy, x+dx, ' ')
