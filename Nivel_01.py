import pygame
import csv
import button

from constants import TELA_ALTURA, BG, RED, TELA_LARGURA, FPS

from __init__ import (
    tela, nuven_img,
    montanha_img, painel1_img, painel2_img,
    font, start_img, restart_img, terra_data,
    exit_img, bala_img, granada_img, nivel, relogio,
    desenhar_text, reiniciar_nivel,
    inimigo_grupo, bala_grupo, granada_grupo, explode_grupo,
    item_caixa_grupo, decoracao_grupo, agua_grupo, sair_grupo,

    tela_rolar, bg_rolar, nivel,   
    movimento_esquerda, movimento_direita,
    atirar, granada, granada_jogada
)

from map import Mundo
from guns import Granada


mundo = Mundo()
jogador, barra_vida = mundo.processo_data(terra_data)


# criando botoes
start_button = button.Button(
    TELA_LARGURA // 2 - 130, TELA_ALTURA // 2 - 150, start_img, 1)

exit_button = button.Button(TELA_LARGURA // 2 - 110,
                            TELA_ALTURA // 2 * 50, exit_img, 1)

restart_button = button.Button(
    TELA_LARGURA // 2 - 100, TELA_ALTURA // 2 - 50, restart_img, 1)


def desenho_bg():

    tela.fill(BG)
    width = nuven_img.get_width()
    for x in range(5):
        # posicionando no topo
        tela.blit(nuven_img, ((x * width)-bg_rolar * 0.5, 0))

        tela.blit(montanha_img, ((x * width)-bg_rolar * 0.6, TELA_ALTURA -
                  montanha_img.get_height() - 300))  # cortando da forma certa

        tela.blit(painel1_img, ((x * width)-bg_rolar * 0.7,
                  TELA_ALTURA - painel1_img.get_height() - 150))

        tela.blit(painel2_img, ((x * width)-bg_rolar * 0.8,
                  TELA_ALTURA - painel2_img.get_height()))


game_started = False

run = True
while run:
    relogio.tick(FPS)
    if game_started == False:

        tela.fill(BG)  # se inicia tudo
        if start_button.draw(tela):
            game_started = True
            
        if exit_button.draw(tela):
            run = False

    else:

        desenho_bg()
        
        barra_vida.desenhar_barra(jogador.saude_vida)

        desenhar_text('Munição:', font, RED, 10, 35)
        for x in range(jogador.monicao):
            tela.blit(bala_img, (90 + (x*10), 40))

        desenhar_text('Granadas:', font, RED, 10, 60)
        for x in range(jogador.granadas):
            tela.blit(granada_img, (135 + (x*15), 60))

        jogador.atualizar()
        jogador.desenho()

        for inimigo in inimigo_grupo:
            inimigo.ai_inimigo(jogador, mundo)
            inimigo.atualizar()
            inimigo.desenho()

        bala_grupo.update(jogador, mundo)
        granada_grupo.update(jogador, mundo)
        explode_grupo.update()
        item_caixa_grupo.update(jogador)

        decoracao_grupo.update()
        agua_grupo.update()
        sair_grupo.update()

        bala_grupo.draw(tela)
        granada_grupo.draw(tela)
        explode_grupo.draw(tela)
        item_caixa_grupo.draw(tela)

        decoracao_grupo.draw(tela)
        agua_grupo.draw(tela)
        sair_grupo.draw(tela)

        if jogador.vivo:
            if atirar:
                jogador.atirar()

            elif granada and granada_jogada == False and jogador.granadas > 0:
                granada = Granada(jogador.rect.centerx + (
                    0.5 * jogador.rect.size[0] * jogador.direcao), jogador.rect.top, jogador.direcao)
                granada_grupo.add(granada)
                jogador.granadas -= 1  # contagem de granadas
                granada_jogada = True

            tela_rolar = jogador.movimento(movimento_esquerda, movimento_direita, mundo)
            bg_rolar -= tela_rolar

        else:
            if jogador.frame_index == len(jogador.animacao_lista[jogador.acao]) - 1:
                tela_rolar = 0
                if restart_button.draw(tela):
                    bg_rolar = 0

                terra_data = []  # Inicialize a lista vazia

            with open(f'nivel{nivel}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for linha in reader:
                    linha_int = [int(terra) for terra in linha]
                    terra_data.append(linha_int)




            
            meu_mundo = Mundo()
            reiniciar_nivel()
            jogador, barra_vida = meu_mundo.processo_data(terra_data)


        mundo.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False    
                        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                movimento_esquerda = True
            if event.key == pygame.K_d:
                movimento_direita = True
            if event.key == pygame.K_SPACE:
                atirar = True
            if event.key == pygame.K_q:
                granada = True
            if event.key == pygame.K_w and jogador.vivo:
                jogador.pular = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                movimento_esquerda = False
            if event.key == pygame.K_d:
                movimento_direita = False
            if event.key == pygame.K_SPACE:
                atirar = False
            if event.key == pygame.K_q:
                granada = False
                granada_jogada = False

    pygame.display.update()

pygame.quit()
