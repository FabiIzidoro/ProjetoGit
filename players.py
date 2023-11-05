import pygame
import os
import random

from __init__ import bala_grupo, agua_grupo, bg_rolar, tela

from constants import TELA_ALTURA, TELA_LARGURA, TERRA_TAMANHO, GRAVIDADE, LIXO

from guns import Bala


class Soldado(pygame.sprite.Sprite):
    def __init__(self, jogador_tipo, x, y, scale, velocidade, monicao, granadas):

        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.jogador_tipo = jogador_tipo
        self.velocidade = velocidade
        self.monicao = monicao
        self.inicio_monicao = monicao
        self.vel_y = 0
        self.atirar_bala_count = 0
        self.granadas = granadas
        self.saude_vida = 100
        self.maximo_saude = self.saude_vida  # Corrigido: inicializando com um valor
        self.direcao = 1
        self.pular = False
        self.no_ar = True
        self.virar = False

        self.animacao_lista = []
        self.frame_index = 0
        self.acao = 0
        self.atualizar_tempo = pygame.time.get_ticks()
        self.movimento_counter = 0  # movimento
        self.visao = pygame.Rect(0, 0, 150, 20)
        self.ocioso = False
        self.ocioso_counter = 0

        animacao_tipo = ['jogador_idle', 'correr', 'pular', 'morto']

        for animacao in animacao_tipo:
            temp_list = []
            numero_de_frames = len(os.listdir(f'img/{self.jogador_tipo}/{animacao}'))

            for i in range(numero_de_frames):
                img = pygame.image.load(f'img/{self.jogador_tipo}/{animacao}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animacao_lista.append(temp_list)

        self.image = self.animacao_lista[self.acao][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def atualizar(self):
        self.atualizar_animacao()
        self.checar_a_vida()
        if self.atirar_bala_count > 0:
            self.atirar_bala_count -= 1

    def movimento(self, movimento_esquerda, movimento_direita, mundo):
        if self.no_ar:
            self.atualizar_acao(2)

        elif movimento_esquerda or movimento_direita:
            self.atualizar_acao(1)

        else:
            self.atualizar_acao(0)

        tela_rolar = 0
        dx = 0
        dy = 0

        if movimento_esquerda:
            dx = -self.velocidade
            self.virar = True
            self.direcao = -1

        if movimento_direita:
            dx = self.velocidade
            self.virar = False  # Certifique-se de definir virar como False para se mover para a direita
            self.direcao = 1


        if self.pular == True and self.no_ar == False:
            self.vel_y = -11
            self.pular = False
            self.no_ar = True

        self.vel_y += GRAVIDADE
        if self.vel_y > 10:
            self.vel_y = 0

        dy += self.vel_y

        for terra in mundo.obstaculo_list:
            if terra[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                
                if self.jogador_tipo == 'jogador':
                    # print("COLIDE X -=> ", terra[1], self.rect)
                    if self.rect.left + dx < 0 or self.rect.right + dx > TELA_LARGURA:
                        dx = 0
                dx = 0

            if terra[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                print("COLIDE Y -=> ", terra[1], self.rect)
                if self.vel_y >= 0:  # reduzindo velocidade a obstaculos
                    self.no_ar = False
                self.vel_y = 0
                # self.no_ar = False
                dy = terra[1].top - self.rect.bottom

            # elif self.vel_y >= 0:
                # print("self.vel_y >= 0")
                # self.vel_y -= GRAVIDADE
                # if self.vel_y < 0:
                #     self.vel_y = 0
                #     self.no_ar = False
                #     dy = terra[1].top - self.rect.bottom

        # se caso cair, ele morre
        if pygame.sprite.spritecollide(self, agua_grupo, False):
            self.saude_vida = 0

        if self.rect.bottom > TELA_ALTURA:
            self.saude_vida = 0

        if self.jogador_tipo == 'jogador':
            if self.rect.left + dx < 0 or self.rect.right + dx > TELA_LARGURA:
                dx = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.jogador_tipo == 'jogador':
            if (self.rect.right > TELA_LARGURA - LIXO and bg_rolar < (mundo.nivel_lenght * TERRA_TAMANHO) - TELA_LARGURA) or (self.rect.left < LIXO and bg_rolar > abs(dx)):
                self.rect.x -= dx
                tela_rolar = -dx

        return tela_rolar

    def atirar(self):
        if self.atirar_bala_count == 0 and self.monicao > 0:
            self.atirar_bala_count = 20
            bala = Bala(self.rect.centerx + (0.6 *
                        self.rect.size[0] * self.direcao), self.rect.centery, self.direcao)
            bala_grupo.add(bala)
            self.monicao -= 1

    def ai_inimigo(self, jogador, mundo):
        ai_inimigo_direita = False
        ai_inimigo_esquerda = False
        if self.vivo and jogador.vivo:  # jogador e inimigo vivo
            if self.ocioso == False and random.randint(1, 200) == 1:
                self.atualizar_acao(0)
                self.ocioso = True
                self.ocioso_counter = 50
            if self.visao.colliderect(jogador.rect):
                self.atualizar_acao(0)
                self.atirar()
            else:
                if self.ocioso == False:
                    if self.direcao == 1:  # direcao do jogador for igual a 1, a posicao direita do inimigo vai ser verdadeira
                        ai_inimigo_direita = True
                else:
                    ai_inimigo_direita = False
                ai_inimigo_esquerda = not ai_inimigo_direita
                self.movimento(ai_inimigo_esquerda, ai_inimigo_direita, mundo)
                self.atualizar_acao(1)
                self.movimento_counter += 1

                self.visao.center = (self.rect.centerx + 75 * self.direcao, self.rect.centery)

                if self.movimento_counter > TERRA_TAMANHO:  # jogador sem sair da cena
                    self.direcao *= -1
                    self.movimento_counter *= -1

                else:
                    self.ocioso_counter -= 1
                    if self.ocioso_counter <= 0:
                        self.ocioso = False

    def atualizar_animacao(self):
        ANIMACAO_FRESH = 100
     

        self.image = self.animacao_lista[self.acao][self.frame_index]

        if pygame.time.get_ticks() - self.atualizar_tempo > ANIMACAO_FRESH:
            self.atualizar_tempo = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animacao_lista[self.acao]):
            if self.acao == 3:
                self.frame_index = len(self.animacao_lista[self.acao]) - 1
            else:
                self.frame_index = 0

    def atualizar_acao(self, new_action):
        if new_action != self.acao:
            self.acao = new_action
            self.frame_index = 0
            self.atualizar_tempo = pygame.time.get_ticks()

    def checar_a_vida(self):
        if self.saude_vida <= 0:
            self.saude_vida = 0
            self.velocidade = 0
            self.vivo = False
            self.atualizar_acao(3)  # Defina a ação como "morto" quando a saúde do jogador chegar a zero

    def desenho(self):
        tela.blit(pygame.transform.flip(self.image, self.virar, False), self.rect)
