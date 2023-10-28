import pygame
import csv

from constants import (
    TELA_ALTURA, TELA_LARGURA, TERRA_TAMANHO,
    TERRA_TIPO, LINHAS, COLUNAS,
)

pygame.init()

font = pygame.font.SysFont('Futura', 25)  # instalar fonte


tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption('JOGO EM PYGAME')  # Título da janela

relogio = pygame.time.Clock()

tela_rolar = 0
bg_rolar = 0
nivel = 1

    
movimento_esquerda = False
movimento_direita = False
atirar = False
granada = False
granada_jogada = False

start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()

restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
painel1_img = pygame.image.load('img/background/painel1.png').convert_alpha()
painel2_img = pygame.image.load('img/background/painel2.png').convert_alpha()
montanha_img = pygame.image.load('img/background/montanha.png').convert_alpha()
nuven_img = pygame.image.load('img/background/nuven.png').convert_alpha()


img_list = []
for x in range(TERRA_TIPO):
    img = pygame.image.load(f'img/terra/{x}.png')
    img = pygame.transform.scale(img, (TERRA_TAMANHO, TERRA_TAMANHO))
    img_list.append(img)

# carregando imagens
bala_img = pygame.image.load('img/icones/bala.png').convert_alpha()
granada_img = pygame.image.load('img/icones/granada.png').convert_alpha()
caixa_granada_img = pygame.image.load(
    'img/icones/caixa_granada.png').convert_alpha()
caixa_municao_img = pygame.image.load(
    'img/icones/caixa_municao.png').convert_alpha()
caixa_vida_img = pygame.image.load('img/icones/caixa_vida.png').convert_alpha()

item_caixas = {
    'Vida': caixa_vida_img,
    'Municao': caixa_municao_img,
    'Granada': caixa_granada_img,
}

# Inicializando grupos de sprites
inimigo_grupo = pygame.sprite.Group()
bala_grupo = pygame.sprite.Group()
granada_grupo = pygame.sprite.Group()
explode_grupo = pygame.sprite.Group()
item_caixa_grupo = pygame.sprite.Group()

decoracao_grupo = pygame.sprite.Group()
agua_grupo = pygame.sprite.Group()
sair_grupo = pygame.sprite.Group()

terra_data = []
for linha in range(LINHAS):
    # cria uma lista com "COLUNAS" elementos, todos inicializados com -1
    l = [-1] * COLUNAS
    terra_data.append(l)


def reiniciar_nivel():
    inimigo_grupo.empty()
    bala_grupo.empty()
    granada_grupo.empty()
    explode_grupo.empty()
    item_caixa_grupo.empty()

    decoracao_grupo.empty()
    agua_grupo.empty()
    sair_grupo.empty()

    data = []
    for _ in range(LINHAS):
        # cria uma lista com "COLUNAS" elementos, todos inicializados com -1
        l = [-1] * COLUNAS
        terra_data.append(l)
    return data


with open(f'nivel{nivel}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, linha in enumerate(reader):
        for y, terra in enumerate(linha):
            terra_data[x][y] = int(terra)

print(terra_data)


def desenhar_text(text, font, text_color, x, y):  # localidade de display texto
    img = font.render(text, True, text_color)
    tela.blit(img, (x, y))
