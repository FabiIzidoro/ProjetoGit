import pygame
import csv
import button

from constants import TELA_ALTURA, BG, RED, TELA_LARGURA, FPS

from __init__ import (
    desenhar_text, reiniciar_nivel,
    varibles
)

from map import Mundo
from guns import Granada


meu_mundo = Mundo()
jogador, barra_vida = meu_mundo.processo_data(varibles["terra_data"])


# criando botoes
start_button = button.Button(
    TELA_LARGURA // 2 - 130, TELA_ALTURA // 2 - 150, varibles["start_img"], 1)

exit_button = button.Button(TELA_LARGURA // 2 - 110,
                            TELA_ALTURA // 2 * 50, varibles["exit_img"], 1)

restart_button = button.Button(
    TELA_LARGURA // 2 - 100, TELA_ALTURA // 2 - 50, varibles["restart_img"], 1)


def desenho_bg():

    varibles["tela"].fill(BG)
    width = varibles["nuven_img"].get_width()
    for x in range(5):
        # posicionando no topo
        varibles["tela"].blit(varibles["nuven_img"], ((x * width)-varibles["bg_rolar"] * 0.5, 0))

        varibles["tela"].blit(varibles["montanha_img"], ((x * width)-varibles["bg_rolar"] * 0.6, TELA_ALTURA -
                  varibles["montanha_img"].get_height() - 300))  # cortando da forma certa

        varibles["tela"].blit(varibles["painel1_img"], ((x * width)-varibles["bg_rolar"] * 0.7,
                  TELA_ALTURA - varibles["painel1_img"].get_height() - 150))

        varibles["tela"].blit(varibles["painel2_img"], ((x * width)-varibles["bg_rolar"] * 0.8,
                  TELA_ALTURA - varibles["painel2_img"].get_height()))


game_started = False
restarted = False
run = True

while run:
    varibles["relogio"].tick(FPS)

    if restarted:
        if restart_button.draw(varibles["tela"]):
            restarted = False
            varibles["bg_rolar"] = 0
            
            meu_mundo.obstaculo_list.clear()
            reiniciar_nivel()
            varibles["terra_data"].clear()
        
            with open(f'nivel{varibles["nivel"]}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for linha in reader:
                    linha_int = [int(terra) for terra in linha]
                    varibles["terra_data"].append(linha_int)
            
            jogador, barra_vida = meu_mundo.processo_data(varibles["terra_data"])
            
    elif game_started == False:

        varibles["tela"].fill(BG)  # se inicia tudo
        if start_button.draw(varibles["tela"]):
            game_started = True
            
        if exit_button.draw(varibles["tela"]):
            run = False

    else:
        desenho_bg()
        barra_vida.desenhar_barra(jogador.saude_vida)

        # Desenha as informações do player, como munições e granadas
        desenhar_text('Munição:', varibles["font"], RED, 10, 35)
        for x in range(jogador.monicao):
            varibles["tela"].blit(varibles["bala_img"], (90 + (x*10), 40))

        desenhar_text('Granadas:', varibles["font"], RED, 10, 60)
        for x in range(jogador.granadas):
            varibles["tela"].blit(varibles["granada_img"], (135 + (x*15), 60))

        jogador.atualizar()
        jogador.desenho()

        for inimigo in varibles["inimigo_grupo"]:
            inimigo.ai_inimigo(jogador, meu_mundo)
            inimigo.atualizar()
            inimigo.desenho()

        varibles["bala_grupo"].update(jogador, meu_mundo)
        varibles["granada_grupo"].update(jogador, meu_mundo)
        varibles["explode_grupo"].update()
        varibles["item_caixa_grupo"].update(jogador)

        varibles["decoracao_grupo"].update()
        varibles["agua_grupo"].update()
        varibles["sair_grupo"].update()

        varibles["bala_grupo"].draw(varibles["tela"])
        varibles["granada_grupo"].draw(varibles["tela"])
        varibles["explode_grupo"].draw(varibles["tela"])
        varibles["item_caixa_grupo"].draw(varibles["tela"])

        varibles["decoracao_grupo"].draw(varibles["tela"])
        varibles["agua_grupo"].draw(varibles["tela"])
        varibles["sair_grupo"].draw(varibles["tela"])

        print("TELA_ROLAR -=> ", varibles["tela_rolar"])
        for _obj in meu_mundo.obstaculo_list:
            _obj[1].x += varibles["tela_rolar"]

        if jogador.vivo:
            if varibles["atirar"]:
                jogador.atirar()

            elif varibles["granada"] and varibles["granada_jogada"] == False and jogador.granadas > 0:
                varibles["granada"] = Granada(jogador.rect.centerx + (
                    0.5 * jogador.rect.size[0] * jogador.direcao), jogador.rect.top, jogador.direcao)
                varibles["granada_grupo"].add(varibles["granada"])
                jogador.granadas -= 1  # contagem de granadas
                varibles["granada_jogada"] = True

            varibles["tela_rolar"] = jogador.movimento(varibles["movimento_esquerda"], varibles["movimento_direita"], meu_mundo)
            varibles["bg_rolar"] -= varibles["tela_rolar"]

        elif jogador.frame_index == len(jogador.animacao_lista[jogador.acao]) - 1:
            restarted = True

        meu_mundo.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False    
                        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                varibles["movimento_esquerda"] = True
            if event.key == pygame.K_d:
                varibles["movimento_direita"] = True
            if event.key == pygame.K_SPACE:
                varibles["atirar"] = True
            if event.key == pygame.K_q:
                varibles["granada"] = True
            if event.key == pygame.K_w and jogador.vivo:
                jogador.pular = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                varibles["movimento_esquerda"] = False
            if event.key == pygame.K_d:
                varibles["movimento_direita"] = False
            if event.key == pygame.K_SPACE:
                varibles["atirar"] = False
            if event.key == pygame.K_q:
                varibles["granada"] = False
                varibles["granada_jogada"] = False

    pygame.display.update()

pygame.quit()
