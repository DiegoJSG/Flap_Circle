import random
import pygame
from pygame import gfxdraw

pygame.init()

# Cores
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)

# Tamanho da tela
largura = 450
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Flappy Circle")

clock = pygame.time.Clock()

# Variáveis para o jogador Editar
pos_x = 50
pos_y = altura // 2
gravidade = 1  # Ajuste o valor para tornar o pulo mais suave
impulso = -10  # Ajuste o valor para controlar a altura do pulo

# Variáveis dos obstáculos
largura_obstaculo = 70
altura_obstaculo = random.randint(100, 400)
espaco_obstaculo = 150
pos_x_obstaculo = largura + 20
pos_y_obstaculo = 0
velocidade_obstaculo = 3  # Ajuste o valor para controlar a velocidade dos obstáculos
aumento_velocidade = 0.2  # Aumento de velocidade para cada obstáculo

pontos = 0
pontuacao_anterior = 0
fonte_pontos = pygame.font.SysFont(None, 50)
fonte_pontuacao_anterior = pygame.font.SysFont(None, 30)

fonte_game_over = pygame.font.SysFont(None, 80)
fonte_continue = pygame.font.SysFont(None, 40)
fonte_obrigado = pygame.font.SysFont(None, 60)
fonte_aperte = pygame.font.SysFont(None, 30)
fonte_titulo = pygame.font.SysFont(None, 60)
fonte_instrucoes = pygame.font.SysFont(None, 30)

def jogador():
    pygame.draw.circle(tela, AMARELO, (pos_x, pos_y), 20)

def obstaculos(pos_x, altura, espaco):
    pygame.gfxdraw.box(tela, (pos_x, 0, largura_obstaculo, altura), VERDE)
    pygame.gfxdraw.box(tela, (pos_x, altura + espaco, largura_obstaculo, altura), VERDE)

def mostrar_pontos(pontos):
    texto = fonte_pontos.render("Pontuação: " + str(pontos), True, BRANCO)
    tela.blit(texto, (largura // 2 - texto.get_width() // 2, 50))

def mostrar_pontuacao_anterior(pontuacao):
    texto = fonte_pontuacao_anterior.render("Pontuação anterior: " + str(pontuacao), True, BRANCO)
    tela.blit(texto, (largura - texto.get_width() - 10, 10))

def verificador_de_colisao(pos_x, pos_y, pos_x_obstaculo, pos_y_obstaculo, altura_obstaculo, espaco_obstaculo):
    if pos_x + 20 > pos_x_obstaculo and pos_x - 20 < pos_x_obstaculo + largura_obstaculo:
        if pos_y - 20 < altura_obstaculo or pos_y + 20 > altura_obstaculo + espaco_obstaculo:
            return True
    return False

def mostrar_game_over(pontos):
    tela.fill(PRETO)
    texto_game_over = fonte_game_over.render("GAME OVER", True, BRANCO)
    texto_pontos = fonte_pontos.render("Pontuação: " + str(pontos), True, BRANCO)
    tela.blit(texto_game_over, (largura // 2 - texto_game_over.get_width() // 2, altura // 2 - 50))
    tela.blit(texto_pontos, (largura // 2 - texto_pontos.get_width() // 2, altura // 2 + 50))
    pygame.display.update()
    pygame.time.wait(2000)

def mostrar_continue(contagem):
    tela.fill(PRETO)
    if contagem > 0:
        texto_continue = fonte_continue.render("Tentar Denovo? " + str(contagem), True, BRANCO)
    else:
        texto_continue = fonte_continue.render("Game Over!", True, BRANCO)
    texto_aperte = fonte_aperte.render("Aperte espaço para continuar", True, BRANCO)
    tela.blit(texto_continue, (largura // 2 - texto_continue.get_width() // 2, altura // 2))
    tela.blit(texto_aperte, (largura // 2 - texto_aperte.get_width() // 2, altura // 2 + 50))
    pygame.display.update()

def mostrar_obrigado(pontos):
    tela.fill(PRETO)
    texto_obrigado = fonte_obrigado.render("Obrigado por Jogar!", True, BRANCO)
    texto_pontos = fonte_pontos.render("Pontuação: " + str(pontos), True, BRANCO)
    tela.blit(texto_obrigado, (largura // 2 - texto_obrigado.get_width() // 2, altura // 2 - 50))
    tela.blit(texto_pontos, (largura // 2 - texto_pontos.get_width() // 2, altura // 2 + 50))
    pygame.display.update()
    pygame.time.wait(2000)

def mostrar_menu_inicial():
    tela.fill(PRETO)
    texto_titulo = fonte_titulo.render("Flappy Circle", True, BRANCO)
    texto_instrucoes = fonte_instrucoes.render("Aperte espaço para começar !", True, BRANCO)
    tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, altura // 2 - 50))
    tela.blit(texto_instrucoes, (largura // 2 - texto_instrucoes.get_width() // 2, altura // 2 + 50))
    pygame.display.update()

# Loop principal do jogo
jogo_ativo = True
menu_ativo = True
game_over = False
continue_active = False
contagem = 5
obrigado_por_jogar = False
while jogo_ativo:
    while menu_ativo:
        mostrar_menu_inicial()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogo_ativo = False
                menu_ativo = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_ativo = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo_ativo = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not continue_active:
                pos_y += impulso
            elif event.key == pygame.K_SPACE and game_over and continue_active:
                # Reiniciar o jogo
                pos_x = 50
                pos_y = altura // 2
                altura_obstaculo = random.randint(100, 400)
                pos_x_obstaculo = largura + 20
                pontos = 0
                game_over = False
                continue_active = False
                contagem = 5

    if not game_over and not continue_active and not obrigado_por_jogar:
        pos_y += gravidade

        # Limpar a tela
        tela.fill(PRETO)

        # Desenhando o jogador
        jogador()

        # Desenhando os obstáculos
        obstaculos(pos_x_obstaculo, altura_obstaculo, espaco_obstaculo)

        # Verificando colisão
        if verificador_de_colisao(pos_x, pos_y, pos_x_obstaculo, pos_y_obstaculo, altura_obstaculo, espaco_obstaculo):
            game_over = True
            pontuacao_anterior = pontos

        # Atualizar a posição do obstáculo
        pos_x_obstaculo -= (velocidade_obstaculo + pontos * aumento_velocidade)

        # Verificar se o obstáculo saiu da tela
        if pos_x_obstaculo < -largura_obstaculo:
            pos_x_obstaculo = largura
            altura_obstaculo = random.randint(100, 400)
            pontos += 1
        
        mostrar_pontuacao_anterior(pontuacao_anterior)

        mostrar_pontos(pontos)

        pygame.display.update() # Atualizar a tela


        # Limitar a taxa de quadros por segundo
        clock.tick(30)  # Altere para 60 quadros por segundo para maior fluidez caso queira
    elif game_over and not continue_active and not obrigado_por_jogar:
        mostrar_game_over(pontos)
        continue_active = True
    elif continue_active:
        mostrar_continue(contagem)
        pygame.time.wait(1000)
        contagem -= 1
        if contagem < 0:
            continue_active = False
            game_over = False
            contagem = 0
            obrigado_por_jogar = True
    elif obrigado_por_jogar:
        mostrar_obrigado(pontuacao_anterior)
        jogo_ativo = False

# Encerrar o Pygame
pygame.quit()
