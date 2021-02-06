import os
import sys

import pygame
import requests
api_server = "http://static-maps.yandex.ru/1.x/"
lon = str(float(input()))
lat = str(float(input()))
delta = str(float(input()))


def delta_lon_lat(delta, lon, lat):
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": "map"
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
    screen = pygame.display.set_mode((600, 450))
    delta_lon_lat(delta, lon, lat)
    while running:
        for event in pygame.event.get():  # обработка нажатий
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    delta = str(float(delta) * 1.5)
                if event.key == pygame.K_PAGEDOWN:
                    delta = str(float(delta) / 1.5)
                if float(delta) > 90:
                    delta = '90'
                if float(delta) < 1:
                    delta = '1'
                print(delta)
                delta_lon_lat(delta, lon, lat)
        screen.blit(pygame.image.load("map.png"), (0, 0))
        pygame.display.flip()
        clock.tick(30)
    os.remove("map.png")
    pygame.quit()
"""2.28133742069
2.28133742069
6"""