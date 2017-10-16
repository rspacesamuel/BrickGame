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
CURR_BRICK_SETTLED = False


        
def main():
    global BOARD, CURR_BRICK_SETTLED, BLOCKS_ACROSS, BLOCKS_DOWN
    gameSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("Place the bricks")
    gameSurface.fill(GAME_BKGRND_COLOR)
    gameBorderRect = (INNER_WINDOW_TOPX, INNER_WINDOW_TOPY, WINDOW_WIDTH-100, WINDOW_HEIGHT-200)
    pygame.draw.rect(gameSurface, BLACK, gameBorderRect, 2)
    class Brick:
        brickBorderColor = GRAY
        brickWidth = 25
        brickHeight = 25
        
        def __init__(self, topLeftX, topLeftY):
            self._brickTopLeftX = topLeftX
            self._brickTopLeftY = topLeftY
            self._currentActiveBrick = False
            self._nextActiveBrick = False
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

        def shiftBrick(self,row,col,direction):
            global BOARD, BLOCKS_ACROSS
            if direction == "LEFT":
                if col > 0:
                    #reset current brick to Board defaults
                    self._currentActiveBrick = False
                    pygame.draw.rect(gameSurface, GAME_BKGRND_COLOR, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 0)
                    pygame.draw.rect(gameSurface, Brick.brickBorderColor, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 1)
                    #move current brick to the left
                    nextCol = col - 1
                    BOARD[row][nextCol].drawLSBrick()

            if direction == "RIGHT":
                if col <= BLOCKS_ACROSS - 1:
                    #reset current brick to Board defaults
                    self._currentActiveBrick = False
                    self._nextActiveBrick = False
                    pygame.draw.rect(gameSurface, GAME_BKGRND_COLOR, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 0)
                    pygame.draw.rect(gameSurface, Brick.brickBorderColor, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 1)
                    #move current brick to the left
                    nextCol = col + 1
                    BOARD[row][nextCol].drawLSBrick()
                    BOARD[row][nextCol]._nextActiveBrick = True
                    
                
                
            
 
    BOARD = [[Brick(*Brick.calculateTopLeftXY(blocksAcross)) for blocksAcross in range(BLOCKS_ACROSS)] for _ in range(BLOCKS_DOWN)]

    for i in range(4):
        BOARD[i][int(BLOCKS_ACROSS/2)].drawLSBrick()
       
    while True:
        if CURR_BRICK_SETTLED == True:
            break
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        for row, rowBrick in enumerate(BOARD):
                            for column, brick in enumerate(rowBrick):
                                if brick._currentActiveBrick == True:
                                    brick.shiftBrick(row,column,"LEFT")
                                    if row == BLOCKS_DOWN - 1:
                                        CURR_BRICK_SETTLED = True
                                    

                    elif event.key == K_RIGHT:
                        for row, rowBrick in enumerate(BOARD):
                            for column, brick in enumerate(rowBrick):
                                if brick._currentActiveBrick == True:
                                    if brick._nextActiveBrick == False:
                                        brick.shiftBrick(row,column,"RIGHT")
                                        if row == BLOCKS_DOWN - 1:
                                            CURR_BRICK_SETTLED = True
                                    

            for row, rowBrick in enumerate(BOARD):
                for column, brick in enumerate(rowBrick):
                    if brick._currentActiveBrick == True and row < BLOCKS_DOWN-1:
                        nextRow = row + 1
                        BOARD[nextRow][column]._nextActiveBrick = True
                    elif brick._currentActiveBrick == True and row == BLOCKS_DOWN-1:
                        CURR_BRICK_SETTLED = True

            #Move brick down if it hasn't reached bottom (default brick movement with no key input)
            if CURR_BRICK_SETTLED == False:
                for row, rowBrick in enumerate(BOARD):
                    for column, brick in enumerate(rowBrick):
                          
                        #move brick down
                        if brick._nextActiveBrick == True:
                            brick.drawLSBrick()

                        #and erase the tail
                        elif brick._currentActiveBrick == True:
                            #below statements belong to __init__ but we aren't calling __init__ to avoid re-initializing topX,topY
                            brick._currentActiveBrick = False
                            pygame.draw.rect(gameSurface, GAME_BKGRND_COLOR, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 0)
                            pygame.draw.rect(gameSurface, Brick.brickBorderColor, (brick._brickTopLeftX,brick._brickTopLeftY,brick.brickWidth,brick.brickHeight), 1)

            pygame.time.wait(500)
            pygame.display.update()
            
if __name__ == '__main__':
    main()
