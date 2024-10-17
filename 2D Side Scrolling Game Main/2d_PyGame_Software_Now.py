import pygame
import random

# Initialize Pygame and set up the screen
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Hero Game")

# Clock and FPS settings
clock = pygame.time.Clock()
FPS = 60

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Font setup for text rendering
font = pygame.font.Font(None, 36)

# Player class to handle player movement, jumping, shooting, health, and damage
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.jump_power = 10
        self.gravity = 0.5
        self.y_velocity = 0
        self.max_health = 3
        self.health = self.max_health
        self.lives = 3
        self.is_jumping = False
    
    # Handle key inputs for player movement and jumping
    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = -self.jump_power
        
        # Prevent the player from moving out of screen bounds
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))
    
    # Apply gravity to simulate jumping/falling
    def apply_gravity(self):
        self.rect.y += self.y_velocity
        self.y_velocity += self.gravity
        if self.rect.y >= HEIGHT - 50:
            self.rect.y = HEIGHT - 50
            self.is_jumping = False
    
    # Update player actions
    def update(self):
        self.handle_movement()
        self.apply_gravity()

    # Shoot projectiles from the player
    def shoot(self):
        return Projectile(self.rect.centerx, self.rect.centery, 10)

    # Handle damage taken by the player
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.health = self.max_health
            else:
                return True
        return False

# Projectile class for handling player shots
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()

# Enemy class that defines enemy movement and health
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.randint(2, 4)
        self.health = 50
    
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.kill()

# Collectible class for coins or other objects the player can collect
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(topleft=(x, y))

# Intro screen to capture player's name and age
def game_intro():
    intro = True
    name, age = "", ""

    while intro:
        SCREEN.fill(WHITE)
        welcome_message = font.render("Welcome! Enter your name and age to start", True, BLACK)
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

# Game over screen with options to restart or quit
def game_over_screen():
    game_over = True
    while game_over:
        SCREEN.fill(WHITE)
        game_over_message = font.render("Game Over! Press R to Restart or Q to Quit", True, BLACK)
        SCREEN.blit(game_over_message, (100, HEIGHT // 2))

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

# Main game loop to control game flow, spawning, and updating entities
def start_game():
    player_group = pygame.sprite.Group()
    projectile_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    collectible_group = pygame.sprite.Group()

    player = Player(100, HEIGHT - 50)
    player_group.add(player)

    score = 0

    def spawn_enemy():
        enemy = Enemy(WIDTH + random.randint(100, 300), HEIGHT - 50)
        enemy_group.add(enemy)

    def spawn_collectible():
        collectible = Collectible(random.randint(100, WIDTH), HEIGHT - 80)
        collectible_group.add(collectible)

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
                    projectile = player.shoot()
                    projectile_group.add(projectile)

        # Update game elements
        player_group.update()
        projectile_group.update()
        enemy_group.update()
        collectible_group.update()

        # Player-enemy collision handling
        if pygame.sprite.spritecollideany(player, enemy_group):
            if player.take_damage():
                running = False
                game_over_screen()

        # Projectile-enemy collision handling
        for projectile in pygame.sprite.groupcollide(projectile_group, enemy_group, True, False).keys():
            hit_enemy = pygame.sprite.spritecollideany(projectile, enemy_group)
            if hit_enemy:
                hit_enemy.health -= 10
                if hit_enemy.health <= 0:
                    hit_enemy.kill()
                    score += 10

        # Player-collectible collision handling
        if pygame.sprite.spritecollideany(player, collectible_group):
            collected_item = pygame.sprite.spritecollideany(player, collectible_group)
            if collected_item:
                collected_item.kill()
                score += 5

        # Render all game objects and stats
        SCREEN.fill(WHITE)
        player_group.draw(SCREEN)
        projectile_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        collectible_group.draw(SCREEN)

        health_display = font.render(f"Health: {player.health}", True, BLACK)
        lives_display = font.render(f"Lives: {player.lives}", True, BLACK)
        score_display = font.render(f"Score: {score}", True, BLACK)

        SCREEN.blit(health_display, (10, 10))
        SCREEN.blit(lives_display, (10, 40))
        SCREEN.blit(score_display, (10, 70))

        pygame.display.flip()

    pygame.quit()

# Start the game with intro and main loop
game_intro()
start_game()