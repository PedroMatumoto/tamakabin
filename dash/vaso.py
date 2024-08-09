import sys

import pygame
from PIL import Image

size=(800,600)
FORMAT = "RGBA"


def pil_to_game(img):
    data = img.tobytes("raw", FORMAT)
    return pygame.image.fromstring(data, img.size, FORMAT)

def get_gif_frame(img, frame):
    img.seek(frame)
    return  img.convert(FORMAT)


def init():
    return pygame.display.set_mode(size)

def exit():
    pygame.quit()


# Função para desenhar a barra de vida com cores personalizadas
def draw_health_bar(screen, x, y, current_life, max_life, bar_color, border_color):
    # Configurações da barra de vida
    bar_width = 200
    bar_height = 20
    fill = (current_life / max_life) * bar_width

    # Desenha a borda da barra com a cor especificada
    pygame.draw.rect(screen, border_color, (x, y, bar_width, bar_height),border_radius=5)

    # Desenha a vida restante com a cor especificada
    pygame.draw.rect(screen, bar_color, (x, y, fill, bar_height),border_radius=5)


max_life = 100
current_life = 100

# Carrega a imagem do ícone (substitua 'icon.png' pelo caminho do seu arquivo de ícone)
umidityicon = pygame.image.load('umidity-icon.png')
umidityicon = pygame.transform.scale(umidityicon, (40, 40))  # Ajuste o tamanho conforme necessário

temperatureicon = pygame.image.load('temperature-icon.png')
temperatureicon = pygame.transform.scale(temperatureicon, (40, 40))

lighticon = pygame.image.load('light-icon.png')
lighticon = pygame.transform.scale(lighticon, (40, 40))

def main(screen, path_to_image):
    gif_img = Image.open(path_to_image)
    if not getattr(gif_img, "is_animated", False):
        print(f"Imagem em {path_to_image} não é um gif animado")
        return
    current_frame = 0
    clock = pygame.time.Clock()
    # colocar cor de fundo
    screen.fill((82, 82, 82))
    while True:
        frame = pil_to_game(get_gif_frame(gif_img, current_frame))
        screen.blit(frame, (120, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        umidity_bar_color = (0, 0, 255)
        temperature_bar_color = (255, 0, 0)
        light_bar_color = (255, 255, 0)
        border_color = (255, 255, 255)

        current_frame = (current_frame + 1) % gif_img.n_frames
         # Desenha a barra de vida na posição (x=20, y=20)
         # adiciona ícones de umidade, temperatura e luz
        screen.blit(umidityicon, (40, 240))
        draw_health_bar(screen, 90, 250, current_life, max_life, umidity_bar_color, border_color)
        screen.blit(temperatureicon, (40, 300))
        draw_health_bar(screen, 90, 310, current_life, max_life, temperature_bar_color, border_color)
        screen.blit(lighticon, (40, 360))
        draw_health_bar(screen, 90, 370, current_life, max_life, light_bar_color, border_color)

        pygame.display.flip()
        clock.tick(10)



main(init(),'idle-bounce.gif' )
