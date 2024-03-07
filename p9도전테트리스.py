# import pygame

# pygame.init()

# background=pygame.display.set_mode((1200,900))
# pygame.display.set_caption("Tetris")

# x_pos=background.get_size()[0]//2
# y_pos=background.get_size()[1]//2

# play=True
# while play:
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             play=False
#         if event.type==pygame.KEYDOWN:
#             if event.key==pygame.K_UP:
#                 y_pos-=20
#             if event.key==pygame.K_DOWN:
#                 y_pos+=20
#             if event.key==pygame.K_LEFT:
#                 x_pos-=20
#             if event.key==pygame.K_RIGHT:
#                 x_pos+=20
#     pygame.draw.circle(background,(0,0,255),(x_pos,y_pos),5)
#     pygame.display.update()
            
# pygame.quit()
import pygame
import random

# 게임 보드의 크기 설정
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30
SCREEN_WIDTH = BOARD_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = BOARD_HEIGHT * BLOCK_SIZE

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 테트리스 블록의 모양 정의
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3],
     [3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 0],
     [0, 6, 6]],

    [[7, 7, 7, 7]]
]

# 테트리스 블록 색상 매핑
SHAPE_COLORS = [
    WHITE,
    RED,
    GREEN,
    BLUE,
    WHITE,
    RED,
    GREEN,
    BLUE
]

# 테트리스 게임 클래스 정의
class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris Game")
        self.clock = pygame.time.Clock()
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_shape = self.new_shape()
        self.game_over = False

    def new_shape(self):
        shape = random.choice(SHAPES)
        color = SHAPE_COLORS[SHAPES.index(shape)]
        return {'shape': shape, 'color': color, 'x': BOARD_WIDTH // 2 - len(shape[0]) // 2, 'y': 0}

    def draw_board(self):
        self.screen.fill(BLACK)
        for y, row in enumerate(self.board):
            for x, block in enumerate(row):
                if block:
                    pygame.draw.rect(self.screen, SHAPE_COLORS[block - 1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.update()

    def draw_shape(self):
        shape = self.current_shape['shape']
        color = self.current_shape['color']
        x, y = self.current_shape['x'], self.current_shape['y']
        for row_idx, row in enumerate(shape):
            for col_idx, block in enumerate(row):
                if block:
                    pygame.draw.rect(self.screen, color, ((x + col_idx) * BLOCK_SIZE, (y + row_idx) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def move_shape(self, dx, dy):
        if not self.check_collision(self.current_shape, dx, dy):
            self.current_shape['x'] += dx
            self.current_shape['y'] += dy
        else:
            if dy:
                self.merge_shape()
                self.current_shape = self.new_shape()
                if self.check_collision(self.current_shape, 0, 0):
                    self.game_over = True

    def rotate_shape(self):
        rotated_shape = [list(reversed(row)) for row in zip(*self.current_shape['shape'])]
        if not self.check_collision({'shape': rotated_shape, 'x': self.current_shape['x'], 'y': self.current_shape['y']}):
            self.current_shape['shape'] = rotated_shape

    def merge_shape(self):
        for row_idx, row in enumerate(self.current_shape['shape']):
            for col_idx, block in enumerate(row):
                if block:
                    self.board[self.current_shape['y'] + row_idx][self.current_shape['x'] + col_idx] = block

    def check_collision(self, shape, dx=0, dy=0):
        for row_idx, row in enumerate(shape['shape']):
            for col_idx, block in enumerate(row):
                if block:
                    x = shape['x'] + col_idx + dx
                    y = shape['y'] + row_idx + dy
                    if not (0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT) or self.board[y][x]:
                        return True
        return False

    def clear_lines(self):
        lines_to_clear = [idx for idx, row in enumerate(self.board) if all(row)]
        for idx in lines_to_clear:
            del self.board[idx]
            self.board.insert(0, [0] * BOARD_WIDTH)

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_shape(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_shape(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_shape(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_shape()

            self.move_shape(0, 1)
            self.clear_lines()
            self.draw_board()
            self.draw_shape()
            pygame.display.update()
            self.clock.tick(10)

if __name__ == '__main__':
    game = TetrisGame()
    game.run()