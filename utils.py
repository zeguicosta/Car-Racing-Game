import pygame


# ARQUIVO PARA FUNÇÕES UTILITÁRIAS


# Função para definir o novo tamanho da imagem após ser multiplicada por um fator
def scale_image(img, factor):
    # Usa-se round() para que não haja números decimais
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)