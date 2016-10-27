import tetrisModel
import tetrisController
import tetrisView
import curses

stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
stdscr.nodelay(1)
controller = tetrisController.tetrisController(stdscr)
view = controller.view
endGame = False

"""
Listen for key event.
Apply key event.
Progress block.
Break on endgame.
"""

"""
while(1):
    c = stdscr.getch()
    if endGame:
        break
    elif c == ord('q'):
        break
    elif c == ord('p'):
        view.drawPause()
        while(1):
            c = stdscr.getch()
            if c == ord('p'):
                break
        view.drawDebug("KEY PRESS: " + str(c))
    view.passKey(c)
    controller.step()
    view.drawBoard()
    view.drawInfo()
    if view.gameOver:
        while(1):
            c = stdscr.getch()
            if c == ord('q'):
                endGame = True
                break
"""
curses.halfdelay(5)

while(1):
    c = stdscr.getch()
    #view.drawBoard()
    #view.drawInfo()
    if c == ord('q'):
        break
    elif view.gameOver:
        while(1):
            c = stdscr.getch()
            if c == ord('q'):
                break
        break
    elif c == ord('p'):
        view.drawPause()
        while(1):
            c = stdscr.getch()
            if c == ord('p'):
                break
        continue
    elif c == ord(' '):
        view.passKey(c)
    elif c == curses.KEY_LEFT:
        view.passKey(c)
    elif c == curses.KEY_RIGHT:
        view.passKey(c)
    elif c == curses.KEY_DOWN:
        view.passKey(c)
    elif c == curses.KEY_UP:
        view.passKey(c)

    view.drawBoard()
    view.drawInfo()
    controller.step()
        

curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()
