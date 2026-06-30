import pygame
from screens.main_screen import MainScreen
from screens.weapon_menu import WeaponMenu
from screens.armor_menu import ArmorMenu

class UIManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Текущее состояние приложения: "main", "weapon", "armor"
        self.current_screen = "main"
        
        # Инициализируем изолированные модули экранов
        self.main_screen = MainScreen(width, height)
        self.weapon_menu = WeaponMenu(width, height)
        self.armor_menu = ArmorMenu(width, height)
        
        # Безопасное переопределение кнопки ARMOR строго сверху над головой персонажа
        self.main_screen.btn_armor_select = pygame.Rect(
            int(width * 0.1),            # Отступ слева
            int(height * 0.005),         # Почти у самого верха экрана
            int(width * 0.8),            # Длинная плашка во всю ширину
            int(height * 0.035)          # Аккуратная тонкая кнопка
        )
        
        # ИСПРАВЛЕНО: Безопасно пересоздаем Rect для кнопки WEAPON на всю ширину
        self.main_screen.btn_weapon_select = pygame.Rect(
            int(width * 0.05), 
            int(height * 0.88), 
            int(width * 0.9), 
            int(height * 0.07)
        )

    def draw(self, screen, calc, mouse_pos):
        screen.fill((20, 20, 24)) # Базовый фон для всех окон
        
        # Роутинг (распределение) отрисовки в зависимости от активного экрана
        if self.current_screen == "main":
            self.main_screen.draw(screen, calc, mouse_pos)
            
            # Дополнительно рисуем кнопку ARMOR сверху над персонажем
            c_arm = (140, 110, 70) if self.main_screen.btn_armor_select.collidepoint(mouse_pos) else (100, 80, 50)
            pygame.draw.rect(screen, c_arm, self.main_screen.btn_armor_select, border_radius=6)
            
            txt_arm = self.main_screen.font_small.render("ARMOR SETTINGS", True, (255, 255, 255))
            screen.blit(txt_arm, txt_arm.get_rect(center=self.main_screen.btn_armor_select.center))
            
        elif self.current_screen == "weapon":
            self.weapon_menu.draw(screen, calc, mouse_pos)
            
        elif self.current_screen == "armor":
            self.armor_menu.draw(screen, calc, mouse_pos)

    def handle_click(self, pos, calc):
        # Перенаправляем клики в зависимости от того, какое окно сейчас открыто
        if self.current_screen == "main":
            # Проверяем клик по верхней кнопке брони напрямую
            if self.main_screen.btn_armor_select.collidepoint(pos):
                self.current_screen = "armor"
                return
                
            # Все остальные клики обрабатывает главный экран
            next_screen = self.main_screen.handle_click(pos, calc)
            if next_screen:
                self.current_screen = next_screen
                
        elif self.current_screen == "weapon":
            next_screen = self.weapon_menu.handle_click(pos, calc)
            if next_screen:
                self.current_screen = next_screen
                
        elif self.current_screen == "armor":
            next_screen = self.armor_menu.handle_click(pos, calc)
            if next_screen:
                self.current_screen = next_screen
