import pygame
import time
import random
# from snakeCPU

pygame.init()
clock = pygame.time.Clock()
FPS = 5  # difficulty dependent on frame rate
run = True

WIDTH, HEIGHT = 360, 360
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')
WIN.fill((0, 0, 0))


class AbstractSnake:
    START_POS = (WIDTH // 2, HEIGHT // 2)
    rewards = {}

    def __init__(self):
        self.width = 30
        self.height = 30
        self.speed = 30
        self.head = None
        self.randomblock = None
        self.movecount = 0
        self.length = 1
        self.color = (50, 205, 50)
        self.score = 0
        self.x, self.y = self.START_POS
        self.snake = pygame.Rect(self.x, self.y, self.width, self.height)
        self.START_RECT = pygame.Rect(self.START_POS[0], self.START_POS[1], self.width, self.height)
        self.rect_list = []
        self.body = []
        self.direction = 'RIGHT'  # Initial direction of the snake
        self.next_direction = False

    def reset(self):
        self.body.clear()
        self.x, self.y = self.START_POS
        self.movecount = 0
        self.score = 0

    def move(self):
        
        keys = pygame.key.get_pressed()
        moved = False
        # to remove choppy movement use this code:
               # Handle continuous movement in the current direction
        if self.direction == 'RIGHT':
            self.x += self.speed
            self.movecount += 1
            moved = True
        if self.direction == 'LEFT':
            self.x -= self.speed
            self.movecount += 1
            moved = True
        if self.direction == 'UP':
            self.y -= self.speed
            self.movecount += 1
            moved = True
        if self.direction == 'DOWN':
            self.y += self.speed
            self.movecount += 1
            moved = True
     
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


        print(self.direction)

        if not moved:
            self.x += 0
            self.y += 0



        self.snake = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def generate_target_block(self):
        def filterexisting():
            filterdups = True
            existingheightandwidth = [(i[0],i[1]) for i in self.body]
            rect = pygame.Rect(random.randrange(0, WIDTH, 30), random.randrange(0, HEIGHT, 30), 30, 30)
            if (rect.left,rect.top) in existingheightandwidth:
                rect = pygame.Rect(random.randrange(0, WIDTH, 30), random.randrange(0, HEIGHT, 30), 30, 30)
            else:
                filterdups = False
            return rect
        rect = filterexisting()
        self.score += 1        
        self.rewards[self.score] = rect
        self.rect_list.clear()
        self.rect_list.append(rect)

    def collision_target(self):
        reward = self.rewards.get(self.score)
        if reward is not None:
            return reward.colliderect(self.snake)

    def target_block_populate(self):
        if self.movecount == 1:
            self.generate_target_block() 

        elif self.collision_target():
            self.generate_target_block()

    def remove_tail(self):
        self.body.append((self.x, self.y, self.width, self.height))
        self.body = [item for i, item in enumerate(self.body) if item not in self.body[:-self.score]]
        # print(self.body)

    def collision_boarder(self):
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
            self.reset()
        if self.x < 0:
            self.x = 0
            self.reset()
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.reset()
        if self.y < 0:
            self.y = 0
            self.reset()

    def collision_snake(self):
        bodyadjust = self.body[:-1]
        print(bodyadjust)
        print(self.body)
        if self.snake.collidelist(bodyadjust) >= 0:
            self.reset()


        # print(bodyadjust)
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.snake)
        for rect in self.rect_list:
            pygame.draw.rect(win, (255, 0, 0), rect)
        for snakesize in self.body:
            pygame.draw.rect(win, self.color, snakesize)            
        pygame.display.update()


player_snake = AbstractSnake()

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        # Capture arrow key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and player_snake.direction != 'LEFT':
                player_snake.next_direction = 'RIGHT'
            elif event.key == pygame.K_LEFT and player_snake.direction != 'RIGHT':
                player_snake.next_direction = 'LEFT'
            elif event.key == pygame.K_UP and player_snake.direction != 'DOWN':
                player_snake.next_direction = 'UP'
            elif event.key == pygame.K_DOWN and player_snake.direction != 'UP':
                player_snake.next_direction = 'DOWN'


    WIN.fill((0, 0, 0))  # Clear the screen
    print(player_snake.snake)
    player_snake.draw(WIN)
    player_snake.move()
    player_snake.target_block_populate()
    player_snake.remove_tail()
    player_snake.collision_boarder()
    player_snake.collision_snake()

    pygame.display.update()

pygame.quit()
