import pygame

class personagem():
    def __init__(self, x, y, velocidade, animacao, largura_frame, altura_frame, escala_personagem=1, margem_hitbox_x=0.2, margem_hitbox_y=0.2, vida_maxima=100):
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.animacao = animacao
        self.largura_frame = largura_frame
        self.altura_frame = altura_frame
        self.escala = escala_personagem
        self.atacando = False
        self.vida_maxima = vida_maxima
        self.vida_atual = vida_maxima
        self.margem_hitbox_x = margem_hitbox_x
        self.margem_hitbox_y = margem_hitbox_y

        self.animacao_atual = list(animacao.keys())[0]
        self.spritesheet = self.animacao[self.animacao_atual]["imagem_animacao"]
        self.frame_qtd = self.animacao[self.animacao_atual]["qtd_animacao"]
        self.velocidade_animacao = self.animacao[self.animacao_atual]["velocidade_animacao"]

        self.frame_atual = 0
        self.tempo_animacao = 0

    def mudar_animacao(self, nome):
        if self.morto and self.animacao_atual == "Dead":

          return
        elif nome in self.animacao and nome != self.animacao_atual:
            self.animacao_atual = nome
            self.frame_qtd = self.animacao[nome]["qtd_animacao"]
            self.spritesheet = self.animacao[nome]["imagem_animacao"]
            self.velocidade_animacao = self.animacao[nome]["velocidade_animacao"]
            self.frame_atual = 0
            self.tempo_animacao = 0
            self.atacando = nome.startswith("attack")




    def atualizar_animacao(self, dt):
     self.tempo_animacao += dt
     if self.tempo_animacao >= self.velocidade_animacao:
        self.tempo_animacao = 0
        self.frame_atual += 1

     if self.frame_atual >= self.frame_qtd:
        if self.animacao_atual == "Dead":
            self.frame_atual = self.frame_qtd - 1  # Travar no último frame da morte
        elif self.animacao_atual.startswith("attack"):
            self.mudar_animacao("idle")
        else:
            self.frame_atual = 0


    def desenhar(self, tela):
        frame = self.spritesheet.subsurface(
            (self.frame_atual * self.largura_frame, 0, self.largura_frame, self.altura_frame)
        )
        frame_escalado = pygame.transform.scale(
            frame, (self.largura_frame * self.escala, self.altura_frame * self.escala)
        )
        tela.blit(frame_escalado, (self.x, self.y))

    def get_hitbox(self):
        largura_total = self.largura_frame * self.escala
        altura_total = self.altura_frame * self.escala

        largura_hitbox = largura_total * (1 - self.margem_hitbox_x)
        altura_hitbox = altura_total * (1 - self.margem_hitbox_y)

        
        return pygame.Rect(
            
            self.x,
            self.y ,
            largura_hitbox,
            altura_hitbox
        )
        
    def get_hitbox_Boss(self):
     largura_total = self.largura_frame * self.escala
     altura_total = self.altura_frame * self.escala

     largura_hitbox = largura_total * (1 - self.margem_hitbox_x)
     altura_hitbox = altura_total * (1 - self.margem_hitbox_y)

    # Centralizar a hitbox no sprite renderizado
     x_hitbox = self.x + (largura_total - largura_hitbox) / 2
     y_hitbox = self.y + (altura_total - altura_hitbox) / 2

     return pygame.Rect(
        x_hitbox,
        y_hitbox,
        largura_hitbox,
        altura_hitbox
    )

    def receber_dano(self, dano):
        self.vida_atual -= dano
        if self.vida_atual < 0:
            self.vida_atual = 0

class Cavaleiro(personagem):
    def __init__(self, x, y, velocidade, animacao, largura_frame, altura_frame, escala_personagem=3, margem_hitbox_x=0.3, margem_hitbox_y=0.2, vida_maxima=200):
        super().__init__(x, y, velocidade, animacao, largura_frame, altura_frame, escala_personagem, margem_hitbox_x, margem_hitbox_y, vida_maxima)
        self.morto = False


class Minotauro(personagem):
    def __init__(self, x, y, velocidade, animacao, largura_frame, altura_frame, escala_personagem=4, margem_hitbox_x=0.1, margem_hitbox_y=0.15, vida_maxima=300):
        super().__init__(x, y, velocidade, animacao, largura_frame, altura_frame, escala_personagem, margem_hitbox_x, margem_hitbox_y, vida_maxima)
        self.direcao = "esquerda"
        self.ataque_atual = None
        self.morto = False


    def desenhar(self, tela):
        frame = self.spritesheet.subsurface((self.frame_atual * self.largura_frame, 0, self.largura_frame, self.altura_frame))
        frame_escalado = pygame.transform.scale(frame, (self.largura_frame * self.escala, self.altura_frame * self.escala))
        frame_escalado = pygame.transform.flip(frame_escalado, True, False)
        tela.blit(frame_escalado, (self.x, self.y))

    def verificar_ataque(self, alvo):
     if alvo.morto:  # Não atacar se o alvo já estiver morto
        return
     if self.animacao_atual == "attack" and self.frame_atual == 3:
        if self.get_hitbox().colliderect(alvo.get_hitbox()):
            alvo.receber_dano(20)

class AtaqueBoss:
    def __init__(self, nome, probabilidade, velocidade_animacao, intervalo, dano):
        self.nome = nome
        self.probabilidade = probabilidade
        self.velocidade_animacao = velocidade_animacao
        self.intervalo = intervalo
        self.dano = dano

def desenhar_barra_vida(tela, x, y, largura, altura, vida_atual, vida_maxima, cor_barra):
    proporcao = vida_atual / vida_maxima
    pygame.draw.rect(tela, (50, 50, 50), (x, y, largura, altura))  # Fundo
    pygame.draw.rect(tela, cor_barra, (x, y, largura * proporcao, altura))  # Vida
    pygame.draw.rect(tela, (0, 0, 0), (x, y, largura, altura), 2)  # Borda
