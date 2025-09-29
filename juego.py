import pygame
import random
import math


WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 6
SPAWN_INTERVAL = 900  
GAME_TIME = 60  


WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (34,177,76)
DARK_GREEN = (20,120,50)
RED = (200,30,30)
GRAY = (120,120,120)
BLUE = (0,100,255)
YELLOW = (255,200,0)
BROWN = (139,69,19)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 50
        self.height = 30
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._draw_player()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 0

    def _draw_player(self):
   
        surf = self.image
        surf.fill((0,0,0,0))
        pygame.draw.ellipse(surf, BLACK, (3, self.height-14, 14, 14))  # rueda izq
        pygame.draw.ellipse(surf, BLACK, (self.width-17, self.height-14, 14, 14))  # rueda der
        pygame.draw.polygon(surf, BLUE, [(10,10),(30,10),(35,20),(20,20)])  # cuerpo
        pygame.draw.line(surf, BLACK, (30,10),(40,5),2)  # manubrio

    def update(self):
        keys = pygame.key.get_pressed()
        self.speed_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = PLAYER_SPEED
        self.rect.x += self.speed_x
       
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class FallingObject(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
       
        self.kind = kind
        self.size = random.randint(24, 48)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self._draw_kind()
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH-20), -self.size))
        self.speed_y = random.uniform(2.0, 4.0) + random.random()*2

       
        if self.kind == "good":
            self.value = random.choice([5, 8, 12])  
        else:
            self.value = -random.choice([6, 10, 14])  

    def _draw_kind(self):
        s = self.image
        s.fill((0,0,0,0))
        if self.kind == "good":
           
            choice = random.choice(["tree","solar","bike"])
            if choice == "tree":
                pygame.draw.rect(s, BROWN, (self.size//2 - 4, self.size-12, 8, 12))
                pygame.draw.circle(s, DARK_GREEN, (self.size//2, self.size-18), 14)
            elif choice == "solar":
                pygame.draw.rect(s, YELLOW, (6,6,self.size-12,self.size//2))
                for i in range(6):
                    ang = i * math.pi*2 / 6
                    x = self.size//2 + math.cos(ang)*(self.size//2-6)
                    y = self.size//2 + math.sin(ang)*(self.size//2-6)
                    pygame.draw.line(s, YELLOW, (self.size//2,self.size//2),(x,y),2)
            else:
               
                pygame.draw.ellipse(s, BLACK, (4, self.size-14, 10, 10))
                pygame.draw.ellipse(s, BLACK, (self.size-14, self.size-14, 10, 10))
                pygame.draw.line(s, BLUE, (8,self.size-20),(self.size-12,self.size-20),3)
        else:
           
            choice = random.choice(["car","factory"])
            if choice == "car":
                pygame.draw.rect(s, RED, (4, self.size-18, self.size-8, 12))
                pygame.draw.ellipse(s, BLACK, (6, self.size-10, 8, 8))
                pygame.draw.ellipse(s, BLACK, (self.size-14, self.size-10, 8, 8))
            else:
                pygame.draw.rect(s, GRAY, (6, 6, self.size-12, self.size-12))
                pygame.draw.rect(s, BLACK, (self.size//2-4, 0, 8, 8))
               
                pygame.draw.circle(s, GRAY, (self.size-6, 4), 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 50:
            self.kill()


# ---------- Funciones auxiliares ----------
def draw_text(surface, text, size, x, y, center=False):
    font = pygame.font.SysFont("arial", size)
    txt = font.render(text, True, BLACK)
    rect = txt.get_rect()
    if center:
        rect.center = (x,y)
    else:
        rect.topleft = (x,y)
    surface.blit(txt, rect)

def show_pause(surface):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255,255,255,180))
    surface.blit(overlay, (0,0))
    draw_text(surface, "PAUSA - Presiona ESPACIO para continuar", 28, WIDTH//2, HEIGHT//2, center=True)


def save_readme():
    readme = """Instrucciones del juego:
- Mover con flechas izquierda/derecha o A/D.
- Recoger objetos verdes/amarillos para REDUCIR la huella de carbono.
- Evitar autos y fábricas que aumentan la huella.
- Cada objeto muestra los kg CO2 que ahorras o emites.
- Objetivo: obtener mayor 'kg CO2 ahorrados' al finalizar.
"""
    with open("Huella_instrucciones.txt", "w", encoding="utf-8") as f:
        f.write(readme)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Huella de Carbono - Reduce tu impacto")
    clock = pygame.time.Clock()

   
    all_sprites = pygame.sprite.Group()
    falling = pygame.sprite.Group()

    player = Player(WIDTH//2, HEIGHT-60)
    all_sprites.add(player)


    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, SPAWN_INTERVAL)
    start_ticks = pygame.time.get_ticks()
    paused = False

    score = 0  
    total_collected = 0
    level = 1

    save_readme()

    running = True
    while running:
        dt = clock.tick(FPS)
        elapsed_sec = (pygame.time.get_ticks() - start_ticks)/1000
        remaining = max(0, GAME_TIME - int(elapsed_sec))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            if event.type == spawn_event and not paused:
               
                kind = "good" if random.random() < 0.65 - min(0.3, level*0.02) else "bad"
                obj = FallingObject(kind)
                all_sprites.add(obj)
                falling.add(obj)

        if not paused:
            all_sprites.update()

           
            hits = pygame.sprite.spritecollide(player, falling, True)
            for h in hits:
                score += h.value
                total_collected += 1
               
                if total_collected % 10 == 0:
                    level += 1
                   
                    new_interval = max(300, SPAWN_INTERVAL - level*40)
                    pygame.time.set_timer(spawn_event, new_interval)

           
            if remaining <= 0:
                running = False

       
        screen.fill((230, 255, 240))  
       
        pygame.draw.rect(screen, (200,255,200), (0,0, WIDTH, 50))
        draw_text(screen, f"Tiempo: {remaining}s", 22, 10, 10)
        draw_text(screen, f"kg CO2 ahorrados: {score}", 22, 240, 10)
        draw_text(screen, f"Nivel: {level}", 22, 540, 10)

        all_sprites.draw(screen)

       
        facts = [
            "Caminar o usar bici reduce emisiones por vehículo.",
            "Plantar árboles ayuda a absorber CO2.",
            "La energía solar reduce huella de carbono.",
           
        ]
        if random.random() < 0.003:  
            draw_text(screen, random.choice(facts), 18, WIDTH//2, 70, center=True)

        if paused:
            show_pause(screen)

        pygame.display.flip()

   
    screen.fill(WHITE)
    draw_text(screen, "FIN DEL JUEGO", 40, WIDTH//2, HEIGHT//2 - 60, center=True)
    draw_text(screen, f"kg CO2 Ahorrados: {score}", 32, WIDTH//2, HEIGHT//2, center=True)
    draw_text(screen, "Presiona ESC para salir o R para reiniciar", 20, WIDTH//2, HEIGHT//2 + 60, center=True)
    pygame.display.flip()


    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False
                if event.key == pygame.K_r:
                    main()
                    return

    pygame.quit()

if __name__ == "__main__":
    main()