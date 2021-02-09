import os
import sys

import pygame
import requests
api_server = "http://static-maps.yandex.ru/1.x/"
lon = str(float(input()))
lat = str(float(input()))
delta = str(float(input()))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def delta_lon_lat_layers(delta, lon, lat, layer):
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": layer
    }
    response = requests.get(api_server, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


if __name__ == '__main__':
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('Мордобилити')
    running = True
    layer = 'map'
    screen = pygame.display.set_mode((800, 650))
    delta_lon_lat_layers(delta, lon, lat, layer)
    all_sprites = pygame.sprite.Group()
    # создадим спрайт
    sprite = pygame.sprite.Sprite()
    # определим его вид
    sprite.image = load_image("shema.png")
    # и размеры
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = 10
    sprite.rect.y = 460
    # добавим спрайт в группу
    all_sprites.add(sprite)
    while running:
        for event in pygame.event.get():  # обработка нажатий
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 10 < pygame.mouse.get_pos()[0] < 85 and 460 < pygame.mouse.get_pos()[1] < 495 and layer != 'map':
                    layer = 'map'
                    sprite.image = load_image("shema.png")
                elif 87 < pygame.mouse.get_pos()[0] < 162 and 460 < pygame.mouse.get_pos()[1] < 495 and layer != 'sat':
                    layer = 'sat'
                    sprite.image = load_image("spytnik.png")
                elif 164 < pygame.mouse.get_pos()[0] < 240 and 460 < pygame.mouse.get_pos()[1] < 495 and layer != 'skl':
                    layer = 'sat,skl'
                    sprite.image = load_image("gibrid.png")
                delta_lon_lat_layers(delta, lon, lat, layer)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    delta = str(float(delta) * 1.5)
                if event.key == pygame.K_PAGEDOWN:
                    delta = str(float(delta) / 1.5)
                if event.key == pygame.K_RIGHT:
                    lon = str(float(lon) + float(delta) / 2)
                if event.key == pygame.K_LEFT:
                    lon = str(float(lon) - float(delta) / 2)
                if event.key == pygame.K_UP:
                    lat = str(float(lat) + float(delta) / 4)
                if event.key == pygame.K_DOWN:
                    lat = str(float(lat) - float(delta) / 4)
                if float(delta) > 90:
                    delta = '90'
                if float(delta) < 1:
                    delta = '1'
                if float(lon) > 179:
                    lon = str(float(lon) - 359)
                elif float(lon) < -179:
                    lon = str(float(lon) + 359)
                if float(lat) > 85:
                    lat = str(float(lat) - 170)
                elif float(lat) < -85:
                    lat = str(float(lat) + 170)
                delta_lon_lat_layers(delta, lon, lat, layer)
        screen.blit(pygame.image.load("map.png"), (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    os.remove("map.png")
    pygame.quit()
"""2.28133742069
2.28133742069
6"""