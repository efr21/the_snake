import random
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый игровой объект."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, surface):
        """Отрисовывает ячейку на игровой поверхности."""
        cell_rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, cell_rect)
        pygame.draw.rect(surface, BORDER_COLOR, cell_rect, 1)

    def draw(self, surface):
        """Отрисовывает объект на игровом поле."""
        self.draw_cell(surface)


class Apple(GameObject):
    """Яблоко."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока на игровом поле."""
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(surface)


class Snake(GameObject):
    """Змейка."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE,
                           GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self, event):
        """Обновляет направление движения змейки."""
        if event.key == pygame.K_UP and self.direction != DOWN:
            self.next_direction = UP
        elif event.key == pygame.K_DOWN and self.direction != UP:
            self.next_direction = DOWN
        elif event.key == pygame.K_LEFT and self.direction != RIGHT:
            self.next_direction = LEFT
        elif event.key == pygame.K_RIGHT and self.direction != LEFT:
            self.next_direction = RIGHT

    def move(self):
        """Обновляет позицию змейки."""
        self.direction = self.next_direction or self.direction
        x, y = self.position
        dx, dy = self.direction
        new_head = ((x + dx * GRID_SIZE) % SCREEN_WIDTH, (y + dy * GRID_SIZE)
                    % SCREEN_HEIGHT)

        # Проверяем столкновение с яблоком
        if new_head == apple.position:
            self.length += 1
            apple.randomize_position()

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

        # Обновляем позицию головы змейки
        self.position = self.positions[0]

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш и изменяет направление движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            snake.update_direction(event)


def main():
    """Основной игровой цикл."""
    snake = Snake()
    global apple
    apple = Apple()

    while True:
        clock.tick(SPEED)

        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.move()

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
