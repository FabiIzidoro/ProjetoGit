import pygame
from __init__ import (
    bala_img, granada_img,
    bala_grupo, inimigo_grupo, explode_grupo, 
)

from constants import TELA_LARGURA, GRAVIDADE, TERRA_TAMANHO

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.velocidade = 10
        self.image = bala_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direcao = direcao

    def update(self, jogador, mundo):
        self.rect.x += (self.direcao * self.velocidade)
        if self.rect.right < 0 or self.rect.left > TELA_LARGURA:
            self.kill()

        for terra in mundo.obstaculo_list:
            if terra[1].colliderect(self.rect):
                self.kill()

        if pygame.sprite.spritecollide(jogador, bala_grupo, False):
            if jogador.vivo:
                jogador.saude_vida -= 5
                self.kill()

        for inimigo in inimigo_grupo:
            if pygame.sprite.groupcollide(inimigo_grupo, bala_grupo, False, True):
                if inimigo.vivo:
                    inimigo.saude_vida -= 25
                    self.kill()


class Granada(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.tempo = 100
        self.vel_y = -10
        self.velocidade = 7
        self.image = granada_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direcao = direcao

    def update(self, jogador, mundo):
        self.vel_y += GRAVIDADE
        dx = self.direcao * self.velocidade
        dy = self.vel_y



        for terra in mundo.obstaculo_list:
            if terra[1].colliderect(self.rect):#(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.velocidade = 0
                self.vel_y = 0
                dy = 0
                if self.rect.centerx < terra[1].centerx:
                    self.rect.right = terra[1].left

                else:
                    self.rect.left = terra[1].right    
                #self.direcao *= -1
                #dx = -self.direcao * self.velocidade
                #if terra[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #self.velocidade = 0
                    #if self.vel_y < 0:
                        #self.vel_y = 0
                        #dy = terra[1].bottom - self.rect.top
                    #elif self.vel_y >= 0:
                        #self.vel_y = 0
                        #dy = terra[1].top - self.rect.bottom

        if self.rect.left + dx < 0 or self.rect.right + dx > TELA_LARGURA:
            self.direcao *= -1
            dx = -self.direcao * self.velocidade  # para granada não sumir no lobby

        self.rect.x += dx
        self.rect.y += dy

        self.tempo -= 1
        if self.tempo <= 0:  # precisa explodir
            self.kill()
            explode = Explode(self.rect.x, self.rect.y, 0.5)
            explode_grupo.add(explode)

            if abs(self.rect.centerx - jogador.rect.centerx) < TERRA_TAMANHO * 2 and \
                    abs(self.rect.centery - jogador.rect.centery) < TERRA_TAMANHO * 2:
                jogador.saude_vida -= 50

            for inimigo in inimigo_grupo:

                if abs(self.rect.centerx - inimigo.rect.centerx) < TERRA_TAMANHO * 2 and \
                        abs(self.rect.centery - inimigo.rect.centery) < TERRA_TAMANHO * 2:
                    inimigo.saude_vida -= 50


class Explode(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(
                f'img/explode/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(
                img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0

        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        EXPLODE_VELOCIDADE = 4
        self.counter += 1

        if self.counter >= EXPLODE_VELOCIDADE:
            self.counter = 0
            self.frame_index += 1

        if self.frame_index >= len(self.images):
            self.kill()
        else:
            self.image = self.images[self.frame_index]
