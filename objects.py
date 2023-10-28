import pygame

from __init__ import item_caixas, tela, tela_rolar

from constants import BLACK, RED, YELLOW, TERRA_TAMANHO


class Decoracao(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TERRA_TAMANHO // 2, y +
                            (TERRA_TAMANHO - self.image.get_height()))


class Agua(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TERRA_TAMANHO // 2, y +
                            (TERRA_TAMANHO - self.image.get_height()))


class Sair(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TERRA_TAMANHO // 2, y +
                            (TERRA_TAMANHO - self.image.get_height()))


class ItemCaixa(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_caixas[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TERRA_TAMANHO // 2, y +
                            (TERRA_TAMANHO - self.image.get_height()))

    def update(self, jogador):  # pegar objetos
        self.rect.x += tela_rolar
        if pygame.sprite.collide_rect(self, jogador):
            if self.item_type == 'Vida':
                jogador.saude_vida += 25

                if jogador.saude_vida > jogador.maximo_saude:
                    jogador.saude_vida = jogador.maximo_saude

            elif self.item_type == 'Municao':
                jogador.monicao += 15

            elif self.item_type == 'Granada':
                jogador.granadas += 3

            self.kill()


class BarraVida():
    def __init__(self, x, y, saude_vida, maximo_saude):
        self.x = x
        self.y = y
        self.saude_vida = saude_vida
        self.maximo_saude = maximo_saude

    def desenhar_barra(self, saude_vida):
        self.saude_vida = saude_vida
        por_vida = self.saude_vida / self.maximo_saude

        pygame.draw.rect(tela, BLACK, (self.x - 2, self.y - 2, 164, 24))
        pygame.draw.rect(tela, RED, (self.x, self.y, 160, 20))
        pygame.draw.rect(tela, YELLOW, (self.x, self.y, 160 * por_vida, 20))
