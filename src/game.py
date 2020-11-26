
import sys
import time
from random import randrange as rng
import pygame

# colors 
BG_COLOR = 200, 200, 200
BORDER_COLOR = 125, 125, 125
COLOR_LIVE = 240, 240, 240
COLOR_DEAD = 25, 25, 25

# cell definitions
CELL_SIZE = CELL_W, CELL_H = 20, 20
BORDER_SIZE = 3
RATIO = 19, 10
MULTIPLIER = 4

# refresh rate (ms)
REFRESH = 50

# font
FONTFACE = 'arial'
FONTSIZE = 25

# define
BOARD_W = CELL_W * RATIO[0] * MULTIPLIER
BOARD_H = CELL_H * RATIO[1] * MULTIPLIER
BOARD_X = CELL_W * 1 * MULTIPLIER
BOARD_Y = CELL_H * 1 * MULTIPLIER

BOARD_SIZE = BOARD_W, BOARD_H
BOARD_POS = BOARD_X, BOARD_Y

BOARD_BG_SIZE = BOARD_W + BORDER_SIZE * 2, BOARD_H + BORDER_SIZE * 2
BOARD_BG_POS = BOARD_X - BORDER_SIZE, BOARD_Y - BORDER_SIZE

SCREEN_W = BOARD_W + (2 * CELL_W * MULTIPLIER)
SCREEN_H = BOARD_H + (2 * CELL_H * MULTIPLIER)
SCREEN_SIZE = SCREEN_W, SCREEN_H

TEXT_POS = BOARD_X, BOARD_Y - CELL_H * MULTIPLIER / 2
TEXT_SIZE = CELL_W * 10, FONTSIZE

LIVE = True
DEAD = False


class GameOfLife():

    """ Game of life main class """

    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Game Of Life v0.1")

        self.generation = 1
        self.cell_arr = {} # Array with the cells and their states

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.board = pygame.Surface(BOARD_SIZE)
        self.board_bg = pygame.Surface(BOARD_BG_SIZE)

        self.text_surface = pygame.Surface(TEXT_SIZE)
        self.font = pygame.font.SysFont(FONTFACE, FONTSIZE)
        self.update_text()

        for nx, x in enumerate(range(0, BOARD_W, CELL_W)):
            for ny, y in enumerate(range(0, BOARD_H, CELL_H)):
                self.cell_arr[(nx, ny)] = self.create_cell(x, y, CELL_W, CELL_H, rng(0, 2))

        self.screen.fill(BG_COLOR)
        self.board.fill(BORDER_COLOR)
        self.board_bg.fill(BORDER_COLOR)
        self.text_surface.fill(BG_COLOR)
        self.screen.blit(self.board_bg, BOARD_BG_POS)
        self.screen.blit(self.board, BOARD_POS)
        self.screen.blit(self.text_surface, TEXT_POS)
        pygame.display.flip()


    def create_cell(self, x, y, w, h, state=DEAD):

        ofs = BORDER_SIZE / 2
        color = COLOR_DEAD
        rect = pygame.Rect(x+ofs, y+ofs, w-ofs, h-ofs)

        if state == LIVE:
            color = COLOR_LIVE

        pygame.draw.rect(self.board, color, rect, 0)

        return ((x, y), state)

    
    def update_gen(self):

        max_x = RATIO[0] * MULTIPLIER
        max_y = RATIO[1] * MULTIPLIER

        arr = self.cell_arr # current array
        re_arr = {} # return array

        for pos, cell in arr.items():

            cx = pos[0]     # cell array position x
            cy = pos[1]     # cell array position y
            px = cell[0][0] # cell position x
            py = cell[0][1] # cell position y
            nl = 0          # neighbours alive counter
            st = DEAD       # default state

            for ox in range(-1, 2):         # offset x
                for oy in range (-1, 2):    # offset y

                    nx = cx + ox # neighbour x
                    ny = cy + oy # neighbour y

                    if nx < 0 or ny < 0:
                        continue
                    if nx >= max_x or ny >= max_y:
                        continue
                    if ox == 0 and oy == 0:
                        continue

                    if arr[(nx, ny)][1] == LIVE:
                        nl += 1

            if cell[1] == LIVE and 2 <= nl <= 3:
                st = LIVE
            elif cell[1] == DEAD and nl == 3:
                st = LIVE

            re_arr[pos] = self.create_cell(px, py, CELL_W, CELL_H, st)

        return re_arr


    def update_text(self):
        self.text_surface.fill(BG_COLOR)
        self.counter = self.font.render(str(self.generation), True, (50, 50, 50))
        self.text_surface.blit(self.counter, (0,0))


    def draw(self):

        self.cell_arr = self.update_gen()
        
        self.update_text()
        self.screen.blit(self.board, BOARD_POS)
        self.screen.blit(self.text_surface, TEXT_POS)

        pygame.display.flip()

    
    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


    def run(self):

        while True:
            
            self.generation += 1

            time.sleep(REFRESH/1000)

            self.handle_events()
            self.draw()

if __name__ == '__main__':
    game = GameOfLife()
    game.run()