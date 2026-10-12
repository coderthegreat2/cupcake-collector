import pygame, random, os, asyncio

async def main():
    pygame.init()

    font = pygame.font.SysFont("Arial", 24)
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    player_speed = 5

    player_rect = pygame.Rect(100, 0, 32, 48)
    player_dx = 0
    player_dy = 0

    pheight = 32
    pwidth = 32

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sprite_player = pygame.image.load(os.path.join(SCRIPT_DIR, "assets/madeline_celeste.png")).convert_alpha()
    sprite_player = pygame.transform.scale_by(sprite_player,3)


    score = 0

    GRAVITY = 0.8
    JUMP_HEIGHT = -15
    on_ground = False

    platforms = [
        pygame.Rect(0, 550, 800, 50),
        pygame.Rect(100, 400, 250, 20),
        pygame.Rect(450, 200, 250, 20)
    ]

    platform_movement = [0,2,-2]

    cupcakes = []
    for _ in range(10):
        x = random.randint(50, 700)
        y = random.randint(50, 500)

        cupcakes.append(pygame.Rect(x,y,16,16))

    # The Game Loop & Event Handling
    while running:

        for i in range(3):
            if(platform_movement[i] < 0):
                if(platforms[i].left < 100):
                    platform_movement[i] = -platform_movement[i]
            elif(platform_movement[i] > 0):
                if(platforms[i].left > 450):
                    platform_movement[i] = -platform_movement[i]

            platforms[i].left += platform_movement[i]


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player_dx = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_dx = -player_speed
        if keys[pygame.K_RIGHT]:
            player_dx = player_speed
        if keys[pygame.K_UP] and on_ground:
            player_dy = JUMP_HEIGHT
            on_ground = False

        player_dy += GRAVITY

        player_rect.x += player_dx
        if player_rect.left < 0: player_rect.left = 0
        if player_rect.right > WIDTH: player_rect.right = WIDTH

        player_rect.y += player_dy
        on_ground = False

        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_dy > 0:
                    player_rect.bottom = platform.top
                    player_dy = 0
                    on_ground = True
                elif player_dy < 0:
                    player_rect.top = platform.bottom
                    player_dy = 0

        if player_rect.bottom > 550:
            player_rect.bottom = 550
            player_vel_y = 0
            is_grounded = True

        for cupcake in cupcakes[:]:
            if player_rect.colliderect(cupcake):
                cupcakes.remove(cupcake)
                score += 1

        # Rendering (Drawing) Graphics
        screen.fill((20, 24, 40))

        for platform in platforms:
            pygame.draw.rect(screen, (111,194,118), platform)

        for cupcake in cupcakes:
            pygame.draw.circle(screen, (255,255,0), cupcake.center, 8)
        
        score_text = font.render(f"Score: {score}",True,(255,255,255))
        screen.blit(score_text, (20,20))

        screen.blit(sprite_player, (player_rect.x-30,player_rect.y-48))

        pygame.display.flip()

        # Frame Rate & Cleanup
        clock.tick(60)
        await asyncio.sleep(0)


    pygame.quit()
asyncio.run(main())