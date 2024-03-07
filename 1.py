import pygame
import random

# 게임 설정
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# 테트리스 조각 모양
SHAPES = [
    [[1, 1, 1, 1]],  # 직선
    [[1, 1, 1], [0, 1, 0]],  # T자형
    [[1, 1, 0], [0, 1, 1]],  # Z자형
    [[0, 1, 1], [1, 1, 0]],  # 반대 Z자형
    [[1, 1], [1, 1]]  # 네모
]

# 테트리스 조각 색상
COLORS = [
    (255, 0, 0),  # 빨강
    (0, 255, 0),  # 초록
    (0, 0, 255),  # 파랑
    (255, 255, 0),  # 노랑
    (255, 165, 0)  # 주황
]

# 테트리스 보드 초기화
def create_board():
    return [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

# 새로운 블록 생성
def new_block():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return shape, color, 0, 3

# 블록을 보드에 그리기
def draw_block(screen, block, offset_x, offset_y):
    shape, color, x, y = block
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j]:
                pygame.draw.rect(screen, color, pygame.Rect((offset_x + j) * BLOCK_SIZE, (offset_y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK, pygame.Rect((offset_x + j) * BLOCK_SIZE, (offset_y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# 충돌 감지
# 충돌 감지
def collide(board, block):
    shape, _, x, y = block
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j]:
                if (
                    x + j < 0
                    or x + j >= BOARD_WIDTH
                    or y + i >= BOARD_HEIGHT
                    or board[y + i][x + j] != 0
                ):
                    return True
    return False

# 블록을 보드에 추가
def add_to_board(board, block):
    shape, _, x, y = block
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j]:
                board[i + y][j + x] = 1

# 줄 삭제
def remove_row(board, row):
    del board[row]
    return [[0] * BOARD_WIDTH] + board

# 보드에서 완전한 줄 삭제
def remove_complete_rows(board):
    complete_rows = [i for i, row in enumerate(board) if all(row)]
    for row in complete_rows:
        board = remove_row(board, row)
    return board, len(complete_rows)

# 메인 함수
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("테트리스")

    clock = pygame.time.Clock()
    board = create_board()
    game_over = False

    current_block = new_block()
    next_block = new_block()

    while not game_over:
        screen.fill(WHITE)

        # 현재 블록 그리기
        draw_block(screen, current_block, 0, 0)

        # 보드 그리기
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if board[y][x]:
                    pygame.draw.rect(screen, GRAY, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, BLACK, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        pygame.display.flip()

        # 블록 이동 및 회전
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            current_block = (current_block[0], current_block[1], current_block[2] - 1, current_block[3])
            if collide(board, current_block):
                current_block = (current_block[0], current_block[1], current_block[2] + 1, current_block[3])
        if keys[pygame.K_RIGHT]:
            current_block = (current_block[0], current_block[1], current_block[2] + 1, current_block[3])
            if collide(board, current_block):
                current_block = (current_block[0], current_block[1], current_block[2] - 1, current_block[3])
        if keys[pygame.K_DOWN]:
            current_block = (current_block[0], current_block[1], current_block[2], current_block[3] + 1)
            if collide(board, current_block):
                current_block = (current_block[0], current_block[1], current_block[2], current_block[3] - 1)
        if keys[pygame.K_UP]:
            rotated_shape = list(zip(*current_block[0][::-1]))
            current_block = (rotated_shape, current_block[1], current_block[2], current_block[3])
            if collide(board, current_block):
                rotated_shape = list(zip(*rotated_shape[::-1]))
                current_block = (rotated_shape, current_block[1], current_block[2], current_block[3])

        # 중력 적용
        if not keys[pygame.K_DOWN]:
            current_block = (current_block[0], current_block[1], current_block[2], current_block[3] + 1)
            if collide(board, current_block):
                current_block = new_block()
                board = add_to_board(board, current_block)
                board, num_rows_removed = remove_complete_rows(board)

        # 게임 종료
        if any(board[0]):
            game_over = True

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()