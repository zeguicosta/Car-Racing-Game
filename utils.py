import pygame


# Função para definir o novo tamanho da imagem após ser multiplicada por um fator
def scale_image(img, factor):
    # Usa-se round() para que não haja números decimais
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size) # Função do pygame que redefine o tamanho da imagem

# Função que rotaciona a imagem inicialmente pelo top left e depois reajusta para que seja pelo centro
def blit_rotate_center(window, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle) # Função do pygame que rotaciona a imagem
    # Remove o offset, rotacionando a imagem sem modificar as posições x e y
    new_rectangle = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    window.blit(rotated_image, new_rectangle.topleft) # Exibe a imagem rotacionada