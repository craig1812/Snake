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
        self.movementlist = {}
        self.direction = 'RIGHT'  # Initial direction of the snake
        self.next_direction = False
        self.prev_direction = False
        self.startingposition = False
        self.adjacent_coordinates = 0


        self.cpu_track = []

    def reset(self):
        self.body.clear()
        self.x, self.y = self.START_POS
        self.movecount = 0
        self.score = 0
        self.startingposition = True

    # def move_x(self):
        
    #     self.movecount += 1
    #     self.x += self.speed

    # def move_y(self):
    #     pass

    def get_exp_coordinates(self):
        x_bar = (self.snake[0],self.rect_list[0][0])
        y_bar = (self.snake[1],self.rect_list[0][1])
        coordinate_left = [(x_bar[0]-(x-1),self.snake[1]) if x_bar[0] > x_bar[1] else (x_bar[0]+(x-1),x_bar[1]) for x in range(1,abs(x_bar[0]-x_bar[1]),30)]
        get_x_coords = coordinate_left[-1][0]
        coordinate_top = [(get_x_coords, y_bar[0]-(y-1)) if y_bar[0] > y_bar[1] else (get_x_coords, y_bar[0]+(y-1)) for y in range(1,abs(y_bar[0]-y_bar[1]),30)]
        return coordinate_left + coordinate_top



    def cpu_search_quadrants(self):
        left_rect = pygame.Rect(self.x-30, self.y, self.width, self.height)
        right_rect = pygame.Rect(self.x+30, self.y, self.width, self.height)
        top_rect = pygame.Rect(self.x, self.y-30, self.width, self.height)
        bottom_rect = pygame.Rect(self.x, self.y+30, self.width, self.height)

        # rect_adjusted = [elem for elem in list(left_rect) if elem not in self.body ]

        collide_left = left_rect.collidelist(self.body)
        collide_right = right_rect.collidelist(self.body)
        collide_top = top_rect.collidelist(self.body)
        collide_bottom = bottom_rect.collidelist(self.body)

        return [collide_left, collide_right, collide_top, collide_bottom]




    def cpu_move(self):
        collision_quadrants = self.cpu_search_quadrants()
        print(collision_quadrants)
        self.prev_direction = self.direction
        moved = False

        if self.adjacent_coordinates == 0 and self.score == 0:
            self.movecount+=1
            self.score = 0
        #     # self.snake.move_ip(0,0)
        # else: 
        #         self.snake.move_ip(self.x, self.y)
        #         self.movecount+=1
        # if self.collision_target() == True or not self.collision_target():
        #     pass
        
        elif self.adjacent_coordinates[0] < 0 and collision_quadrants[0] == -1:
            self.direction == 'LEFT'
            self.x -= self.speed
            self.snake.move_ip(self.x,self.y)
            self.movecount+=1
            moved = True

        elif self.adjacent_coordinates[0] > 0 and collision_quadrants[1] == -1:
            self.direction == 'RIGHT'            
            self.x += self.speed
            self.snake.move_ip(self.x,self.y)
            self.movecount+=1
            moved = True
        
        elif self.adjacent_coordinates[1] < 0 and collision_quadrants[2] == -1:
            self.direction == 'UP'
            self.y -= self.speed
            self.snake.move_ip(self.x,self.y)
            self.movecount+=1
            moved = True

        elif self.adjacent_coordinates[1] > 0 and collision_quadrants[3] == -1:
            self.direction == 'DOWN'
            self.y += self.speed
            self.snake.move_ip(self.x,self.y)
            self.movecount+=1
            moved = True

        else: print('I''m trapped!')

        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        self.movementlist[self.movecount] = self.direction
            

    


        self.snake = pygame.Rect(self.x, self.y, self.width, self.height)


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


        # print(self.direction)

        if not moved:
            self.x += 0
            self.y += 0



        self.snake = pygame.Rect(self.x, self.y, self.width, self.height)
        # print(self.snake)


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

    def get_stepwise_coordinates(self):
        if self.movecount != 0 :
            target_left = self.rect_list[0].left
            target_top = self.rect_list[0].top
            adjacent_coordinates_left = target_left - self.body[-1][0]
            adjacent_coordinates_top = target_top - self.body[-1][1]
            self.adjacent_coordinates = (adjacent_coordinates_left, adjacent_coordinates_top)
            return self.adjacent_coordinates 
            # print(f"target: {target_left}, {target_top}")
            # print(f"current: {self.body[0][0]}, {self.body[0][1]}")
            # print(f"adjacent: {adjacent_coordinates_left}, {adjacent_coordinates_top}")


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
        # print(bodyadjust)
        # print(self.body)
        if self.snake.collidelist(bodyadjust) >= 0:
            self.reset()
    

        
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.snake)
        for rect in self.rect_list:
            pygame.draw.rect(win, (255, 0, 0), rect)
        for snakesize in self.body:
            pygame.draw.rect(win, self.color, snakesize)            
        pygame.display.update()

    # def update_path_point(self):
    #     target = self.rect_list[0]
    #     rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height()) 
    #     if rect.collidepoint(target): #create rectangle, use this to see if colliding with target
    #         self.current_point += 1 #if colliding, move to next point


player_snake = AbstractSnake()

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        # # # Capture arrow key presses
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_RIGHT and player_snake.direction != 'LEFT':
        #         player_snake.next_direction = 'RIGHT'
        #     elif event.key == pygame.K_LEFT and player_snake.direction != 'RIGHT':
        #         player_snake.next_direction = 'LEFT'
        #     elif event.key == pygame.K_UP and player_snake.direction != 'DOWN':
        #         player_snake.next_direction = 'UP'
        #     elif event.key == pygame.K_DOWN and player_snake.direction != 'UP':
        #         player_snake.next_direction = 'DOWN'
        # # player_snake.cpu_move()
        # Capture arrow key presses
        # print(player_snake.movecount)
    WIN.fill((0, 0, 0))  # Clear the screen

    player_snake.draw(WIN)
    # player_snake.move()
    player_snake.cpu_move()

    player_snake.target_block_populate()
    player_snake.remove_tail()
    player_snake.collision_boarder()
    # player_snake.collision_snake()
    print(player_snake.get_stepwise_coordinates())
    # print(player_snake.get_exp_coordinates())

    pygame.display.update()

pygame.quit()
