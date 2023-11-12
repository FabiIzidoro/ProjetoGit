import pygame
from __init__ import varibles
from constants import TELA_LARGURA, GRAVIDADE, TERRA_TAMANHO

# Definindo a classe Bala
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        super().__init__()  # Inicialização da classe base Sprite
        self.velocidade = 10
        self.image = varibles["bala_img"]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Definindo a posição inicial da bala
        self.direcao = direcao

    def update(self, jogador, mundo):
        # Movendo a bala
        self.rect.x += (self.direcao * self.velocidade)
        
        # Removendo a bala se sair da tela
        if self.rect.right < 0 or self.rect.left > TELA_LARGURA:
            self.kill()

        # Checando colisões com obstáculos
        for terra in mundo.obstaculo_list:
            if terra[1].colliderect(self.rect):
                self.kill()

        # Checando colisões com o jogador
        if pygame.sprite.spritecollide(jogador, varibles["bala_grupo"], False) and jogador.vivo:
            jogador.saude_vida -= 5
            self.kill()

        # Checando colisões com inimigos
        if pygame.sprite.groupcollide(varibles["inimigo_grupo"], varibles["bala_grupo"], False, True):
            for inimigo in varibles["inimigo_grupo"]:
                if inimigo.vivo:
                    inimigo.saude_vida -= 25
                    self.kill()

# Definindo a classe Granada
class Granada(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.tempo = 100
        self.vel_y = -10
        self.velocidade = 7
        self.image = varibles["granada_img"]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direcao = direcao


    def update(self, jogador, mundo):
        self.vel_y += GRAVIDADE
        dx = self.direcao * self.velocidade
        dy = self.vel_y


        # Colisão vertical
        colisao_vertical = False
        for terra in mundo.obstaculo_list:
            if terra[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                colisao_vertical = True
                break

        if colisao_vertical:
            dy = 0
            self.vel_y = 0
            self.velocidade = 0  # A granada deve parar de se mover na direção horizontal também.    

        # Checando colisões com obstáculos
        for terra in mundo.obstaculo_list:
            if terra[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direcao *= -1
                dx = -self.direcao * self.velocidade

            if terra[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = 0
                self.vel_y = 0




        # Invertendo direção se a granada atingir as bordas da tela
        if self.rect.left + dx < 0 or self.rect.right + dx > TELA_LARGURA:
            self.direcao *= -1
            dx = -self.direcao * self.velocidade

        # Movendo a granada
        self.rect.x += dx
        self.rect.y += dy

        
        # Reduzindo o tempo
        self.tempo -= 1

        # Explodindo a granada após o tempo esgotar
        if self.tempo <= 0:
            self.kill()
            explode = Explode(self.rect.x, self.rect.y, 0.5)
            varibles["explode_grupo"].add(explode)

            # Verificando danos ao jogador e inimigos na explosão
            if abs(self.rect.centerx - jogador.rect.centerx) < TERRA_TAMANHO * 2 and \
                    abs(self.rect.centery - jogador.rect.centery) < TERRA_TAMANHO * 2:
                jogador.saude_vida -= 50

            for inimigo in varibles["inimigo_grupo"]:
                if abs(self.rect.centerx - inimigo.rect.centerx) < TERRA_TAMANHO * 2 and \
                        abs(self.rect.centery - inimigo.rect.centery) < TERRA_TAMANHO * 2:
                    inimigo.saude_vida -= 50

# Definindo a classe de Explosão
class Explode(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()  # Inicialização da classe base Sprite
        # Carregando imagens da animação de explosão
        self.images = [pygame.transform.scale(pygame.image.load(f'img/explode/exp{num}.png').convert_alpha(),
                                             (int(pygame.image.load(f'img/explode/exp{num}.png').get_width() * scale), 
                                              int(pygame.image.load(f'img/explode/exp{num}.png').get_height() * scale))) for num in range(1, 6)]
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        EXPLODE_VELOCIDADE = 4
        self.counter += 1

        # Animando a explosão
        if self.counter >= EXPLODE_VELOCIDADE:
            self.counter = 0
            self.frame_index += 1

        # Removendo a explosão após o último frame
        if self.frame_index >= len(self.images):
            self.kill()
        else:
            self.image = self.images[self.frame_index]
