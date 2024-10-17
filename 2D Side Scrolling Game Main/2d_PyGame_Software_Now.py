import pygame
import random

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Hero Adventure")

# Set game speed
clock = pygame.time.Clock()
FPS = 60

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Font setup
font = pygame.font.Font(None, 36)

# Player class for character control
class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.velocity = 5
        self.jump_height = 10
        self.gravity = 0.5
        self.y_speed = 0
        self.max_health = 3
        self.current_health = self.max_health
        self.lives = 3
        self.is_jumping = False
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.y_speed = -self.jump_height

        # Prevent player from moving off-screen
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

    def apply_gravity(self):
        self.rect.y += self.y_speed
        self.y_speed += self.gravity
        if self.rect.y >= HEIGHT - 50:
            self.rect.y = HEIGHT - 50
            self.is_jumping = False
    
    def update(self):
        self.move()
        self.apply_gravity()

    def fire_projectile(self):
        return Projectile(self.rect.centerx, self.rect.centery, 10)

    def take_damage(self):
        self.current_health -= 1
        if self.current_health <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.current_health = self.max_health
            else:
                return True  # Game over if lives are zero
        return False

# Projectile class for shooting
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, speed):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.speed = speed
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()

# Enemy class for hostile units
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.speed = random.randint(2, 4)
        self.health = 50
    
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.kill()

# Collectible class for items to be collected
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

# Display introduction screen to gather player info
def intro_screen():
    intro = True
    name = ""
    age = ""

    while intro:
        SCREEN.fill(WHITE)
        welcome_message = font.render("Welcome! Enter your name and age", True, BLACK)
        SCREEN.blit(welcome_message, (100, 150))

        name_display = font.render(f"Name: {name}", True, BLACK)
        age_display = font.render(f"Age: {age}", True, BLACK)

        SCREEN.blit(name_display, (100, 200))
        SCREEN.blit(age_display, (100, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name and age:
                    intro = False
                elif event.unicode.isalpha():
                    name += event.unicode
                elif event.unicode.isdigit() and len(age) < 2:
                    age += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    if age:
                        age = age[:-1]
                    elif name:
                        name = name[:-1]

        pygame.display.update()
    
    return name

# Game over screen to display score and restart options
def display_game_over(final_score):
    game_over = True
    while game_over:
        SCREEN.fill(WHITE)
        over_message = font.render(f"Game Over! Your score: {final_score}", True, BLACK)
        restart_message = font.render("Press R to Restart or Q to Quit", True, BLACK)
        SCREEN.blit(over_message, (100, HEIGHT // 2 - 50))
        SCREEN.blit(restart_message, (100, HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start_game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        pygame.display.update()

# Main game loop
def start_game():
    player_name = intro_screen()

    # Group initializations
    player_group = pygame.sprite.Group()
    projectile_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    collectible_group = pygame.sprite.Group()

    # Player instance
    player = Player(100, HEIGHT - 50)
    player_group.add(player)

    score = 0

    def spawn_enemy():
        new_enemy = Enemy(WIDTH + random.randint(100, 300), HEIGHT - 50)
        enemy_group.add(new_enemy)

    def spawn_collectible():
        new_collectible = Collectible(random.randint(100, WIDTH), HEIGHT - 80)
        collectible_group.add(new_collectible)

    enemy_timer = 0
    collectible_timer = 0

    running = True
    while running:
        clock.tick(FPS)
        enemy_timer += 1
        collectible_timer += 1

        if enemy_timer > 100:
            spawn_enemy()
            enemy_timer = 0

        if collectible_timer > 200:
            spawn_collectible()
            collectible_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    new_projectile = player.fire_projectile()
                    projectile_group.add(new_projectile)

        # Update entities
        player_group.update()
        projectile_group.update()
        enemy_group.update()
        collectible_group.update()

        if pygame.sprite.spritecollideany(player, enemy_group):
            if player.take_damage():
                running = False
                display_game_over(score)

        for proj in pygame.sprite.groupcollide(projectile_group, enemy_group, True, False).keys():
            enemy = pygame.sprite.spritecollideany(proj, enemy_group)
            if enemy:
                enemy.health -= 10
                if enemy.health <= 0:
                    enemy.kill()
                    score += 10

        if pygame.sprite.spritecollideany(player, collectible_group):
            item = pygame.sprite.spritecollideany(player, collectible_group)
            if item:
                item.kill()
                score += 5

        # Draw elements on screen
        SCREEN.fill(WHITE)
        player_group.draw(SCREEN)
        projectile_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        collectible_group.draw(SCREEN)

        # Display score, player info, health, and lives
        name_display = font.render(f"Player: {player_name}", True, BLACK)
        health_display = font.render(f"Health: {player.current_health}", True, BLACK)
        lives_display = font.render(f"Lives: {player.lives}", True, BLACK)
        score_display = font.render(f"Score: {score}", True, BLACK)

        SCREEN.blit(name_display, (10, 10))
        SCREEN.blit(health_display, (10, 50))
        SCREEN.blit(lives_display, (10, 90))
        SCREEN.blit(score_display, (10, 130))

        pygame.display.update()

    pygame.quit()

# Start the game
start_game()
