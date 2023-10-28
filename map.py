
from __init__ import (
    img_list, tela, inimigo_grupo,
    item_caixa_grupo, decoracao_grupo, agua_grupo, sair_grupo,
)

from constants import TERRA_TAMANHO

from objects import Decoracao, Agua, Sair, ItemCaixa, BarraVida

from players import Soldado


class Mundo():
    def __init__(self):
        self.obstaculo_list = []

    def processo_data(self, data):
        self.nivel_lenght = len(data[0])
        jogador, barra_vida = None, None

        for y, linha in enumerate(data):
            for x, terra in enumerate(linha):
                if terra >= 0:
                    img = img_list[terra]
                    img_rect = img.get_rect()
                    img_rect.x = x * TERRA_TAMANHO
                    img_rect.y = y * TERRA_TAMANHO
                    terra_data = (img, img_rect)

                    if terra >= 0 and terra <= 8:
                        self.obstaculo_list.append(terra_data)

                    elif terra >= 9 and terra <= 10:
                        agua = Agua(img, x * TERRA_TAMANHO, y * TERRA_TAMANHO)
                        agua_grupo.add(agua)

                    elif terra >= 11 and terra <= 14:
                        decoracao = Decoracao(
                            img, x * TERRA_TAMANHO, y * TERRA_TAMANHO)
                        decoracao_grupo.add(decoracao)

                    elif terra == 15:
                        jogador = Soldado(
                            'jogador', x * TERRA_TAMANHO, y * TERRA_TAMANHO, 1.65, 5, 20, 5)
                        barra_vida = BarraVida(
                            10, 10, jogador.saude_vida, jogador.saude_vida)
                    elif terra == 16:
                        inimigo = Soldado(
                            'inimigo', x * TERRA_TAMANHO, y * TERRA_TAMANHO, 1.65, 2, 20, 0)
                        inimigo_grupo.add(inimigo)

                    elif terra == 17:
                        item_caixa = ItemCaixa(
                            'Municao', x * TERRA_TAMANHO, y * TERRA_TAMANHO)
                        item_caixa_grupo.add(item_caixa)

                    elif terra == 18:
                        item_caixa = ItemCaixa(
                            'Granada', x * TERRA_TAMANHO, y * TERRA_TAMANHO)
                        item_caixa_grupo.add(item_caixa)

                    elif terra == 19:
                        item_caixa = ItemCaixa(
                            'Vida', x * TERRA_TAMANHO, y * TERRA_TAMANHO)
                        item_caixa_grupo.add(item_caixa)

                    elif terra == 20:
                        sair = Sair(img, x * TERRA_TAMANHO, y * TERRA_TAMANHO)
                        sair_grupo.add(sair)

        return jogador, barra_vida

    def draw(self):
        for terra in self.obstaculo_list:
            tela.blit(terra[0], terra[1])
