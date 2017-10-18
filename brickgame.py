#UNDER CONSTRUCTION. TREAD LIGHTLY.

import pygame, sys, itertools
from pygame.locals import *

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
INNER_WINDOW_TOPX = 50
INNER_WINDOW_TOPY = 100

WHITE = (255,255,255)
PALEGREEN = (152,251,152)
GAME_BKGRND_COLOR = WHITE
WALLCOLOR = PALEGREEN

GREEN = (0,100,0)
BLACK = (0,0,0)
GRAY = (220,220,220)
BOARD = []
PREV_BOARD = []

BRICK_BORDER_COLOR = BLACK
BLOCKS_ACROSS = 12
BLOCKS_DOWN = 16
END_OF_ROW = False
TOP_LEFT_X = INNER_WINDOW_TOPX-25
TOP_LEFT_Y = INNER_WINDOW_TOPY
CURR_BRICK_SETTLED = True


        
def main():
    global BOARD, CURR_BRICK_SETTLED, BLOCKS_ACROSS, BLOCKS_DOWN
    bottomRow = -1
    bottomColumn = -1
    dontMoveLeft = False
    dontMoveRight = False
    gameSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("Place the bricks")
    gameSurface.fill(GAME_BKGRND_COLOR)
    gameBorderRect = (INNER_WINDOW_TOPX, INNER_WINDOW_TOPY, WINDOW_WIDTH-100, WINDOW_HEIGHT-200)
    pygame.draw.rect(gameSurface, BLACK, gameBorderRect, 2)
    class Brick:
        brickBorderColor = GRAY
        brickWidth = 25
        brickHeight = 25
        
        def __init__(self, topLeftX, topLeftY, brickRow, brickCol):
            self._brickTopLeftX = topLeftX
            self._brickTopLeftY = topLeftY
            self._brickRow = brickRow
            self._brickColumn = brickCol
            self._currentActiveBrick = False
            self._nextActiveBrick = False
            self._brickSettled = False
            self._bottomRow = False
            self._currentlyMovingAcross = False
            #draw background wall (the board)
            pygame.draw.rect(gameSurface, GAME_BKGRND_COLOR, (self._brickTopLeftX,self._brickTopLeftY,self.brickWidth,self.brickHeight), 0)
            pygame.draw.rect(gameSurface, Brick.brickBorderColor, (self._brickTopLeftX,self._brickTopLeftY,self.brickWidth,self.brickHeight), 1)
        
        def calculateTopLeftXY(blockAcross):
            global BLOCKS_ACROSS, TOP_LEFT_X, TOP_LEFT_Y, END_OF_ROW, INNER_WINDOW_TOPX
            if blockAcross == BLOCKS_ACROSS-1:
                END_OF_ROW = True
                TOP_LEFT_X += Brick.brickWidth
            elif END_OF_ROW == True:
                END_OF_ROW = False
                TOP_LEFT_X = INNER_WINDOW_TOPX
                TOP_LEFT_Y += Brick.brickHeight
            else:
                TOP_LEFT_X += Brick.brickWidth
            return (TOP_LEFT_X, TOP_LEFT_Y)

        def drawLSBrick(self):
            lsBrickColor = GREEN
            lsBrickBorderColor = BRICK_BORDER_COLOR
            self._currentActiveBrick = True
            self._nextActiveBrick = False
            pygame.draw.rect(gameSurface, lsBrickColor, (self._brickTopLeftX,self._brickTopLeftY,Brick.brickWidth,Brick.brickHeight),0)
            pygame.draw.rect(gameSurface, lsBrickBorderColor, (self._brickTopLeftX,self._brickTopLeftY,Brick.brickWidth,Brick.brickHeight),1)

        def shiftBrick(self,direction):
            global BOARD, BLOCKS_ACROSS
            if direction == "LEFT":
                if self._brickColumn > 0:
                    #reset current brick to Board defaults
                    self._currentActiveBrick = False
                    pygame.draw.rect(gameSurface, GAME_BKGRND_COLOR, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 0)
                    pygame.draw.rect(gameSurface, Brick.brickBorderColor, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 1)
                    #move current brick to the left
                    nextCol = self._brickColumn - 1
                    BOARD[self._brickRow][nextCol].drawLSBrick()
                    
            if direction == "RIGHT":
                if self._brickColumn < BLOCKS_ACROSS - 1:
                    #reset current brick to Board defaults
                    self._currentActiveBrick = False
                    self._nextActiveBrick = False
                    pygame.draw.rect(gameSurface, GAME_BKGRND_COLOR, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 0)
                    pygame.draw.rect(gameSurface, Brick.brickBorderColor, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 1)
                    #move current brick to the right
                    nextCol = self._brickColumn + 1
                    BOARD[self._brickRow][nextCol].drawLSBrick()
                    BOARD[self._brickRow][nextCol]._currentActiveBrick = True
                    BOARD[self._brickRow][nextCol]._currentlyMovingAcross = True
                    
                                        
    BOARD = [[Brick(*Brick.calculateTopLeftXY(blocksAcross),blocksDown, blocksAcross) for blocksAcross in range(BLOCKS_ACROSS)] for blocksDown in range(BLOCKS_DOWN)]

     
    while True:
        lastKeyPressed = -1
        if CURR_BRICK_SETTLED == True:
            for i in range(4):
                BOARD[i][int(BLOCKS_ACROSS/2)].drawLSBrick()
                bottomRow = i
            BOARD[bottomRow][int(BLOCKS_ACROSS/2)]._bottomRow = True
            CURR_BRICK_SETTLED = False
            dontMoveLeft = False
            dontMoveRight = False
            
        else:
            #Run through all bricks.
            #1. Reset bricks from "currently moving ACROSS" because at this point no brick should be moving ACROSS.
            #2. If there are already settled bricks on either sides of the moving brick, it can't move any further ACROSS.
            for row, rowBrick in enumerate(BOARD):
                for column, brick in enumerate(rowBrick):
                    brick._currentlyMovingAcross = False
                    if brick._bottomRow == True:
                        if column > 0 and row < BLOCKS_DOWN-1:
                            if BOARD[row+1][column-1]._brickSettled == True:
                                dontMoveLeft = True
                        if column < BLOCKS_ACROSS-1 and row < BLOCKS_DOWN-1:
                            if BOARD[row+1][column+1]._brickSettled == True:
                                dontMoveRight = True
                                
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        if dontMoveLeft == False:
                            for row, rowBrick in enumerate(BOARD):
                                for column, brick in enumerate(rowBrick):
                                    if brick._currentActiveBrick == True and brick._brickSettled == False:
                                        brick.shiftBrick("LEFT")
                                        if row == BLOCKS_DOWN - 1:
                                            CURR_BRICK_SETTLED = True
                                        

                    elif event.key == K_RIGHT:
                        lastKeyPressed = K_RIGHT
                        if dontMoveRight == False:
                            for row, rowBrick in enumerate(BOARD):
                                for column, brick in enumerate(rowBrick):
                                    brick._bottomRow = False
                                    if brick._currentActiveBrick == True and brick._brickSettled == False:
                                        if brick._currentlyMovingAcross == False:
                                            brick.shiftBrick("RIGHT")
                                            if row == BLOCKS_DOWN - 1:
                                                CURR_BRICK_SETTLED = True

                    elif event.key == K_DOWN:
                        lastKeyPressed = K_DOWN

            #Make next brick below active, so it moves down:
            for row, rowBrick in enumerate(BOARD):
                for column, brick in enumerate(rowBrick):
                    brick._bottomRow = False
                    if brick._currentActiveBrick == True and row < BLOCKS_DOWN-1:
                        nextRow = row + 1
                        BOARD[nextRow][column]._nextActiveBrick = True
                        bottomRow = nextRow
                        bottomColumn = column
                    elif brick._currentActiveBrick == True and row == BLOCKS_DOWN-1:
                        CURR_BRICK_SETTLED = True
            BOARD[bottomRow][bottomColumn]._bottomRow = True
                  

            #Move brick down if it hasn't reached bottom (default downward brick movement with no key input)
            if CURR_BRICK_SETTLED == False:
                for row, rowBrick in enumerate(BOARD):
                    for column, brick in enumerate(rowBrick):

                        #Is the brick going to land on top of an already settled brick?
                        if brick._bottomRow == True and row < BLOCKS_DOWN-1:
                            if BOARD[row+1][column]._brickSettled == True:
                                    CURR_BRICK_SETTLED = True
                                                    
                        #move brick down
                        if brick._nextActiveBrick == True:
                            brick.drawLSBrick()
                            
                        #and erase the tail
                        elif brick._currentActiveBrick == True:
                            #below statements belong to __init__ but we aren't calling __init__ to avoid re-initializing topX,topY
                            brick._currentActiveBrick = False
                            pygame.draw.rect(gameSurface, GAME_BKGRND_COLOR, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 0)
                            pygame.draw.rect(gameSurface, Brick.brickBorderColor, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 1) 

            #Brick has settled down. Mark it as settled.
            if CURR_BRICK_SETTLED == True:
                for row, rowBrick in enumerate(BOARD):
                    for column, brick in enumerate(rowBrick):
                        if brick._currentActiveBrick == True:
                            brick._currentActiveBrick = False
                            brick._nextActiveBrick = False
                            brick._bottomRow = False
                            brick._currentlyMovingAcross = False
                            brick._brickSettled = True
                

            pygame.display.update()

            if lastKeyPressed == K_DOWN:
                pygame.time.wait(200)
            else:
                pygame.time.wait(500)
                        
if __name__ == '__main__':
    main()

