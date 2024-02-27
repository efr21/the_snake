import pygame
import random


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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Инициализация базового игрового объекта."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на игровом поле."""
        pass


class Apple(GameObject):
    """Инициализация яблока."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """
        Устанавливает случайную позицию яблока
        на игровом поле, не пересекаясь с змейкой.
        """
        while True:
            new_position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        apple_rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, apple_rect)
        pygame.draw.rect(surface, BORDER_COLOR, apple_rect, 1)


class Snake(GameObject):
    """Инициализация змейки."""

    def __init__(self):
        super().__init__((GRID_WIDTH // 2 * GRID_SIZE,
                          GRID_HEIGHT // 2 * GRID_SIZE), SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT  
        self.next_direction = None

    def update_direction(self, event):
        """Обновляет направление движения змейки
        в зависимости от нажатой клавиши.
        """
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
        new_head = ((x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new_head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()
        self.position = self.positions[0]

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            pygame.draw.rect(surface, self.body_color,
                             (*position, GRID_SIZE, GRID_SIZE))

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.__init__()


def handle_keys(snake):
    """Обрабатывает нажатия клавиш и изменяет направление движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    snake = Snake()
    apple = Apple()

    while True:
        # Регулируем скорость игры
        clock.tick(SPEED)

        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)  # Обработка действий пользователя

        snake.move()  # Обновление позиции змейки

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()


# Метод draw класса Apple
def draw(self, surface):
    """Отображает яблоко на экране."""
    rect = pygame.Rect(
        (self.position[0], self.position[1]),
        (GRID_SIZE, GRID_SIZE)
    )
    pygame.draw.rect(surface, self.body_color, rect)
    pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


# Метод draw класса Snake
def draw(self, surface):
    """Отображает змейку на переданной поверхности."""
    for position in self.positions[:-1]:
        rect = (
            pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
    head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, self.body_color, head_rect)
    pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
    if self.last:
        last_rect = pygame.Rect(
            (self.last[0], self.last[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


# Метод обновления направления после нажатия на кнопку
def update_direction(self):
    """Обновляет направление движения игрового объекта
    на следующее направление, если оно установлено.
    """
    if self.next_direction:
        self.direction = self.next_direction
        self.next_direction = None
