import curses

class foo:
    def __init__(self, scr, pos):
        self.stdscr = scr
        self.pos = pos
        self.mpos = (3, 3)
        self.mI = 0

    def endCurses(self):
        curses.nocbreak(); self.stdscr.keypad(0); curses.echo()
        curses.endwin()

    def drawWindow(self, y, x, size):
        for i in range(size):
            self.stdscr.addstr(y+i, x, 'X')
            self.stdscr.addstr(y, x+i, 'X')
            self.stdscr.addstr(y + size - i, x + size, 'X')
            self.stdscr.addstr(y + size, x + size -i, 'X')
        self.stdscr.addstr(y + size, x, 'X')
        self.stdscr.addstr(y, x + size, 'X')

    def passKey(self, c):
        if c == curses.KEY_LEFT:
            y, x = self.pos
            self.stdscr.addstr(y, x, ' ')
            x = max(0, x-1)
            self.stdscr.addstr(y, x, 'X')
            self.pos = (y, x)
        elif c == curses.KEY_RIGHT:
            y, x = self.pos
            self.stdscr.addstr(y, x, ' ')
            x = min(10, x+1)
            self.stdscr.addstr(y, x, 'X')
            self.pos = (y, x)
        elif c == curses.KEY_UP:
            y, x = self.pos
            self.stdscr.addstr(y, x, ' ')
            y = max(0, y-1)
            self.stdscr.addstr(y, x, 'X')
            self.pos = (y, x)
        elif c == curses.KEY_DOWN:
            y, x = self.pos
            self.stdscr.addstr(y, x, ' ')
            y = min(10, y+1)
            self.stdscr.addstr(y, x, 'X')
            self.pos = (y, x)

    def roamer(self):
        y, x = self.mpos
        #x += (self.mI % 10) * -1 ** (self.mI/10)
        x = min(x+1, 12)
        self.stdscr.addstr(y, x, 'X')
        self.mpos = y, x
        self.mI += 1

stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
stdscr.nodelay(1)
pos = (3, 3)
f = foo(stdscr, pos)

while(1):
    c = stdscr.getch()
    f.roamer()
    if c == ord('q'):
        break
    elif c == ord('j'):
        stdscr.addstr("SUP")
    elif c == ord('f'):
        stdscr.addstr(10, 10, "FOO")
    elif c == ord('w'):
        f.drawWindow(10, 10, 5)
    elif c == ord('c'):
        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
        stdscr.addstr("Pretty text", curses.color_pair(7))
        stdscr.refresh()
    else:
        f.passKey(c)



#drawWindow(10, 10, 5)

#curses.nocbreak(); stdscr.keypad(0); curses.echo()
#curses.endwin()

def endCurses():
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()

f.endCurses()


