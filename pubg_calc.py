import pygame
import sys
import os
from ui_manager import UIManager
from damage_logic import DamageCalculator

def main():
    pygame.init()
    
    # 1. ПРОВЕРЯЕМ, РАБОТАЕМ ЛИ МЫ НА СМАРТФОНЕ (ANDROID)
    is_android = 'ANDROID_ARGUMENT' in os.environ or ('ANDROID_BOOTLOGO' in os.environ)
    
    if is_android:
        # НА АНДРОИДЕ: забираем реальное максимальное разрешение телефона и включаем FULLSCREEN
        info = pygame.display.Info()
        SCREEN_WIDTH = info.current_w
        SCREEN_HEIGHT = info.current_h
        
        if SCREEN_WIDTH <= 0 or SCREEN_HEIGHT <= 0:
            SCREEN_WIDTH = 500
            SCREEN_HEIGHT = 800
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        # НА ПК: жестко ограничиваем размеры до эталонного мобильного разрешения (пропорции 9:16)
        # Интерфейс не сожмется в пиксели, но и не растянется на весь твой 24-дюймовый монитор
        SCREEN_WIDTH = 450
        SCREEN_HEIGHT = 800
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
    pygame.display.set_caption("PUBG Calc v1.0")
    clock = pygame.time.Clock()

    # Инициализация логики и интерфейса (теперь они получают правильные адаптивные размеры)
    calc = DamageCalculator()
    ui = UIManager(SCREEN_WIDTH, SCREEN_HEIGHT)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    ui.handle_click(event.pos, calc)

        # Отрисовка текущего состояния
        ui.draw(screen, calc, mouse_pos)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
