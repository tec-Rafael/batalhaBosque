import pygame
import sys
import random
from animacao import Cavaleiro, Minotauro, AtaqueBoss, desenhar_barra_vida

# Inicialização do Pygame
pygame.init()

# Configuração da tela
largura_tela = 1425
altura_tela = 800
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Batalha No Bosque")

# Variáveis de debug
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
debug_mode = False

# Fundo da tela
background = pygame.image.load("images/background/Battleground3.png")
fundo = pygame.transform.scale(background, (largura_tela, altura_tela))

# Animações do cavaleiro
animacoes_cavaleiro = {
    "walk": {"imagem_animacao": pygame.image.load("images/Knight_2/Walk.png").convert_alpha(), "qtd_animacao": 8, "velocidade_animacao": 0.12},
    "idle": {"imagem_animacao": pygame.image.load("images/Knight_2/Idle.png").convert_alpha(), "qtd_animacao": 4, "velocidade_animacao": 0.3},
    "attack1": {"imagem_animacao": pygame.image.load("images/Knight_2/Attack1.png").convert_alpha(), "qtd_animacao": 5, "velocidade_animacao": 0.07},
    "protect": {"imagem_animacao": pygame.image.load("images/Knight_2/Protect.png").convert_alpha(), "qtd_animacao": 1, "velocidade_animacao": 0.8},
    "run": {"imagem_animacao": pygame.image.load("images/Knight_2/Run.png").convert_alpha(), "qtd_animacao": 7, "velocidade_animacao": 0.15},
    "runAttack": {"imagem_animacao": pygame.image.load("images/Knight_2/Run+Attack.png").convert_alpha(), "qtd_animacao": 6, "velocidade_animacao": 0.08},
    "jump": {"imagem_animacao": pygame.image.load("images/Knight_2/Jump.png").convert_alpha(), "qtd_animacao": 6, "velocidade_animacao": 0.13},
    "Dead": {"imagem_animacao": pygame.image.load("images/Knight_2/Dead.png").convert_alpha(), "qtd_animacao": 6, "velocidade_animacao": 0.25}
}

# Animações do minotauro
animacoes_minotauro = {
    "idle":
        {"imagem_animacao": pygame.image.load("images/Minotaur_1/Idle.png").convert_alpha(),
         "qtd_animacao": 6, 
         "velocidade_animacao": 0.13},
    "attack":
        {"imagem_animacao": pygame.image.load("images/Minotaur_1/Attack.png").convert_alpha(),
         "qtd_animacao": 5,
         "velocidade_animacao": 0.1},
    "Dead":
        {"imagem_animacao": pygame.image.load("images/Minotaur_1/Dead.png").convert_alpha(),
         "qtd_animacao": 5,
         "velocidade_animacao": 0.5
         },
}

# Criação dos personagens
personagem = Cavaleiro(
    x=100,
    y=200, 
    velocidade=200, 
    animacao=animacoes_cavaleiro,
    largura_frame=128, 
    altura_frame=128, 
    escala_personagem=3,
    vida_maxima=150,
    margem_hitbox_x=0.5, 
    margem_hitbox_y=0.1
    )

boss = Minotauro(
    x=1000,
    y=100,
    velocidade=200,
    animacao=animacoes_minotauro,
    largura_frame=128, 
    altura_frame=128,
    escala_personagem=4,
    vida_maxima=300,
    margem_hitbox_x=0.55,
    margem_hitbox_y=0.15
    )

# Ataques possíveis do boss
ataques_boss = [
    AtaqueBoss("rapido", 0.25, 0.07, 1.0, 10),
    AtaqueBoss("normal", 0.25, 0.1, 2.0, 15),
    AtaqueBoss("carregado", 0.5, 0.15, 3.5, 25)
]

ult_ataque_boss = 0
intervalo_ataque = 4
relogio = pygame.time.Clock()

# Loop principal
while True:
    dt = relogio.tick(60) / 1000
    move = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not personagem.atacando:
                teclas = pygame.key.get_pressed()
                if teclas[pygame.K_LSHIFT] and (teclas[pygame.K_d] or teclas[pygame.K_a]):
                    personagem.atacando = True
                    personagem.mudar_animacao("runAttack")
                else:
                    personagem.atacando = True
                    personagem.mudar_animacao("attack1")

    teclas = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    # Ações do personagem
    if personagem.atacando:
        personagem.atualizar_animacao(dt)

        # Dano do Cavaleiro no boss
        if personagem.frame_atual == 2:
            if personagem.get_hitbox().colliderect(boss.get_hitbox()):
                if personagem.animacao_atual == "attack1":
                    dano = 10
                elif personagem.animacao_atual == "runAttack":
                    dano = 20
                elif personagem.animacao_atual == "jump":
                    dano = 15
                else:
                    dano = 5
                boss.receber_dano(dano)

    elif teclas[pygame.K_LCTRL]:
        personagem.mudar_animacao("protect")
        move = True
    elif personagem.animacao_atual == "protect":
        personagem.mudar_animacao("idle")
    else:
        if teclas[pygame.K_LSHIFT] and teclas[pygame.K_d] and mouse[0]:
            personagem.x += personagem.velocidade * dt * 1.5
            personagem.mudar_animacao("runAttack")
            move = True
        elif teclas[pygame.K_LSHIFT] and teclas[pygame.K_a] and mouse[0]:
            personagem.x -= personagem.velocidade * dt * 1.5
            personagem.mudar_animacao("runAttack")
            move = True
        elif teclas[pygame.K_SPACE] and teclas[pygame.K_d] and teclas[pygame.K_LSHIFT]:
            personagem.y -= personagem.velocidade * dt
            personagem.x += personagem.velocidade * dt
            personagem.mudar_animacao("jump")
            move = True
            personagem.y += personagem.velocidade * dt
        elif teclas[pygame.K_SPACE] and teclas[pygame.K_a] and teclas[pygame.K_LSHIFT]:
            personagem.y -= personagem.velocidade * dt
            personagem.x -= personagem.velocidade * dt
            personagem.mudar_animacao("jump")
            move = True
            personagem.y += personagem.velocidade * dt
        elif teclas[pygame.K_LSHIFT] and teclas[pygame.K_d]:
            personagem.x += personagem.velocidade * dt * 1.5
            personagem.mudar_animacao("run")
            move = True
        elif teclas[pygame.K_LSHIFT] and teclas[pygame.K_a]:
            personagem.x -= personagem.velocidade * dt * 1.5
            personagem.mudar_animacao("run")
            move = True
        elif teclas[pygame.K_SPACE] and teclas[pygame.K_d]:
            personagem.y -= personagem.velocidade * dt
            personagem.x += personagem.velocidade * dt
            personagem.mudar_animacao("jump")
            move = True
            personagem.y += personagem.velocidade * dt
        elif teclas[pygame.K_SPACE] and teclas[pygame.K_a]:
            personagem.y -= personagem.velocidade * dt
            personagem.x -= personagem.velocidade * dt
            personagem.mudar_animacao("jump")
            move = True
            personagem.y += personagem.velocidade * dt
        elif teclas[pygame.K_d]:
            personagem.x += personagem.velocidade * dt
            personagem.mudar_animacao("walk")
            move = True
        elif teclas[pygame.K_a]:
            personagem.x -= personagem.velocidade * dt
            personagem.mudar_animacao("walk")
            move = True
        elif teclas[pygame.K_SPACE]:
            personagem.y -= personagem.velocidade * dt
            personagem.mudar_animacao("jump")
            move = True
            personagem.y += personagem.velocidade * dt

    # Atualiza animação se não estiver atacando
    if not personagem.atacando:
        if move:
            personagem.atualizar_animacao(dt)
        else:
            personagem.mudar_animacao("idle")
            personagem.atualizar_animacao(dt)

    # Boss ataque automático
    tempo_atual = pygame.time.get_ticks() / 1000
    distancia = abs(personagem.x - boss.x)

    if not boss.morto:
        if distancia <= 150 and not boss.atacando:
         if tempo_atual - ult_ataque_boss >= intervalo_ataque:
            rand = random.random()
            prob_acumulada = 0
            ataque_escolhido = None
            for ataque in ataques_boss:
                prob_acumulada += ataque.probabilidade
                if rand < prob_acumulada:
                    ataque_escolhido = ataque
                    break

            boss.mudar_animacao("attack")
            animacoes_minotauro["attack"]["velocidade_animacao"] = ataque_escolhido.velocidade_animacao
            intervalo_ataque = ataque_escolhido.intervalo
            ult_ataque_boss = tempo_atual
            boss.atacando = True
            boss.ataque_atual = ataque_escolhido

        if boss.atacando and boss.frame_atual == 3:
           if boss.get_hitbox().colliderect(personagem.get_hitbox()):
            if personagem.animacao_atual != "protect":
                print(f"Boss acertou! Dano: {boss.ataque_atual.dano}")
                personagem.receber_dano(boss.ataque_atual.dano)
            else:
                print("Personagem defendeu o ataque!")

        if boss.atacando and boss.frame_atual >= boss.frame_qtd - 1:
          boss.atacando = False
          boss.mudar_animacao("idle")

        if boss.vida_atual == 0 and not boss.morto:
            boss.mudar_animacao("Dead")
            boss.morto = True
            
        if personagem.vida_atual == 0 and not personagem.morto:
            personagem.mudar_animacao("Dead")
            personagem.morto = True
        
        if personagem.morto == True:
            boss.mudar_animacao("idle")
            personagem.move = False
            

    
    boss.atualizar_animacao(dt)

    # Desenho
    tela.blit(fundo, (0, 0))
    personagem.desenhar(tela)
    boss.desenhar(tela)

    desenhar_barra_vida(tela, 50, 20, 300, 25, personagem.vida_atual, personagem.vida_maxima, (0, 200, 0))
    desenhar_barra_vida(tela, largura_tela - 350, 20, 300, 25, boss.vida_atual, boss.vida_maxima, (200, 0, 0))

    if debug_mode:
        pygame.draw.rect(tela, verde, personagem.get_hitbox(), 2)
        pygame.draw.rect(tela, vermelho, boss.get_hitbox_Boss(), 2)

    pygame.display.update()
