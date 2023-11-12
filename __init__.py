import pygame
import csv

from constants import (
    TELA_ALTURA, TELA_LARGURA, TERRA_TAMANHO,
    TERRA_TIPO, LINHAS, COLUNAS,
)

pygame.init()
pygame.display.set_caption('JOGO EM PYGAME')  # Título da janela

varibles = {
    "font": pygame.font.SysFont('Futura', 25),  # instalar fonte
    "tela": pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA)),
    "relogio": pygame.time.Clock(),

    "tela_rolar": 0,
    "bg_rolar": 0,
    "nivel": 1,

    "movimento_esquerda": False,
    "movimento_direita": False,
    "atirar": False,
    "granada": False,
    "granada_jogada": False,

    "start_img": pygame.image.load('img/start_btn.png').convert_alpha(),
    "exit_img": pygame.image.load('img/exit_btn.png').convert_alpha(),

    "restart_img": pygame.image.load('img/restart_btn.png').convert_alpha(),
    "painel1_img": pygame.image.load('img/background/painel1.png').convert_alpha(),
    "painel2_img": pygame.image.load('img/background/painel2.png').convert_alpha(),
    "montanha_img": pygame.image.load('img/background/montanha.png').convert_alpha(),
    "nuven_img": pygame.image.load('img/background/nuven.png').convert_alpha(),

    "img_list": [],

    # carregando imagens
    "bala_img": pygame.image.load('img/icones/bala.png').convert_alpha(),
    "granada_img": pygame.image.load('img/icones/granada.png').convert_alpha(),
    "caixa_granada_img": pygame.image.load(
        'img/icones/caixa_granada.png').convert_alpha(),
    "caixa_municao_img": pygame.image.load(
        'img/icones/caixa_municao.png').convert_alpha(),
    "caixa_vida_img": pygame.image.load('img/icones/caixa_vida.png').convert_alpha(),

    # Inicializando grupos de sprites
    "inimigo_grupo": pygame.sprite.Group(),
    "bala_grupo": pygame.sprite.Group(),
    "granada_grupo": pygame.sprite.Group(),
    "explode_grupo": pygame.sprite.Group(),
    "item_caixa_grupo": pygame.sprite.Group(),

    "decoracao_grupo": pygame.sprite.Group(),
    "agua_grupo": pygame.sprite.Group(),
    "sair_grupo": pygame.sprite.Group(),

    "terra_data": [],
}

for x in range(TERRA_TIPO):
    img = pygame.image.load(f'img/terra/{x}.png')
    img = pygame.transform.scale(img, (TERRA_TAMANHO, TERRA_TAMANHO))
    varibles["img_list"].append(img)


item_caixas = {
    'Vida': varibles["caixa_vida_img"],
    'Municao': varibles["caixa_municao_img"],
    'Granada': varibles["caixa_granada_img"],
}


for linha in range(LINHAS):
    # cria uma lista com "COLUNAS" elementos, todos inicializados com -1
    l = [-1] * COLUNAS
    varibles["terra_data"].append(l)


def reiniciar_nivel():
    varibles["inimigo_grupo"].empty()
    varibles["bala_grupo"].empty()
    varibles["granada_grupo"].empty()
    varibles["explode_grupo"].empty()
    varibles["item_caixa_grupo"].empty()

    varibles["decoracao_grupo"].empty()
    varibles["agua_grupo"].empty()
    varibles["sair_grupo"].empty()


with open(f'nivel{varibles["nivel"]}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, linha in enumerate(reader):
        for y, terra in enumerate(linha):
            varibles["terra_data"][x][y] = int(terra)

# print(terra_data)


def desenhar_text(text, font, text_color, x, y):  # localidade de display texto
    img = font.render(text, True, text_color)
    varibles["tela"].blit(img, (x, y))
