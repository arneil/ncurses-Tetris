#Middle Man

import tetrisView
import tetrisModel

class tetrisController:
    """
    Listens for key events from the viewer and responds appropriately.
    Sends updated game boards to the viewer.
    """

    def __init__(self, scr):
        self.stdscr = scr
        self.view = tetrisView.tetrisView(self, self.stdscr)
        self.game = tetrisModel.tetrisGrid(self)
        self.gameOver = False
        #self.printd("CONTROLLER CREATED")

    def passKey(self, key):
        if key == "left":
            self.game.moveBlock(self.game.dirW)
        elif key == "right":
            self.game.moveBlock(self.game.dirE)
        elif key == "up":
            self.game.rotateBlock()
        elif key == "down":
            self.game.moveBlock(self.game.dirS)
        elif key == "space":
            self.game.dropBlock()
        else:
            return False

    def getBoard(self):
        return self.game.getGrid()

    def getInfo(self):
        return [self.game.gameOver, self.game.score, self.game.level, self.game.nextBlock]

    def step(self):
        self.game.progressBlock()

    def notifyViewGameOver(self):
        """
        Called by the model following the end of the game
        """
        self.view.drawGameOver()
        self.gameOver = True

    def notifyViewLinesRemoved(self, lines):
        """
        Called by the model following the removal of lines.
        Asks the view to do that flashy thing
        """
        self.view.linesRemoved(lines)

    def printd(self, str):
        self.view.drawDebug(str)
