import pygame
from .main_screen_assets import MainScreenAssets

class MainScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_small = pygame.font.SysFont(None, int(width * 0.042))
        self.font_big = pygame.font.SysFont(None, int(width * 0.065)) # Чуть уменьшили, чтобы длинная строка "33.5+33.5..." не вылезала за края
        self.font_clean = pygame.font.SysFont(None, int(width * 0.038)) # Шрифт для кнопки сброса
        self.icon_size = int(width * 0.11)
        
        self.assets = MainScreenAssets(width, height, self.icon_size)
        
        self.img_x = 0
        self.img_y = int(height * 0.045)
        self.img_w = width
        self.img_h = int(height * 0.53)
        
        # Кнопки UI
        self.btn_armor_select = pygame.Rect(int(width * 0.1), int(height * 0.005), int(width * 0.8), int(height * 0.035))
        
        # ИСПРАВЛЕНО: Сузили чат до 72% ширины экрана, чтобы освободить место справа
        self.rect_chat = pygame.Rect(int(width * 0.05), int(height * 0.60), int(width * 0.72), int(height * 0.11))
        
        # ИСПРАВЛЕНО: Квадратная кнопка CLEAN справа от чата
        self.btn_clean = pygame.Rect(int(width * 0.80), int(height * 0.60), int(width * 0.15), int(height * 0.11))
        
        self.btn_distance_minus = pygame.Rect(int(width * 0.05), int(height * 0.74), int(width * 0.16), int(height * 0.05))
        self.btn_distance_plus = pygame.Rect(int(width * 0.79), int(height * 0.74), int(width * 0.16), int(height * 0.05))
        self.btn_weapon_select = pygame.Rect(int(width * 0.05), int(height * 0.88), int(width * 0.9), int(height * 0.07))

    def draw(self, screen, calc, mouse_pos):
        # Кнопка верхнего меню
        c_arm = (140, 110, 70) if self.btn_armor_select.collidepoint(mouse_pos) else (100, 80, 50)
        pygame.draw.rect(screen, c_arm, self.btn_armor_select, border_radius=6)
        txt_arm = self.font_small.render("ARMOR SETTINGS", True, (255, 255, 255))
        screen.blit(txt_arm, txt_arm.get_rect(center=self.btn_armor_select.center))

        # Отрисовка растянутого человечка
        screen.blit(self.assets.char_img, (self.img_x, self.img_y))
        
        # Текст и спрайты экипировки (Симметрия)
        text_y = int(self.height * 0.055)
        txt_helm = self.font_small.render(f"HELM: L{calc.helmet_lvl}", True, (200, 200, 200))
        txt_armor = self.font_small.render(f"ARMOR: L{calc.vest_lvl}", True, (200, 200, 200))
        screen.blit(txt_helm, (int(self.width * 0.05), text_y))
        screen.blit(txt_armor, (int(self.width * 0.95) - txt_armor.get_width(), text_y))
        
        icon_y = text_y + txt_helm.get_height() + int(self.height * 0.008)
        screen.blit(self.assets.helmet_sprites[calc.helmet_lvl], (int(self.width * 0.05), icon_y))
        screen.blit(self.assets.armor_sprites[calc.vest_lvl], (int(self.width * 0.95) - self.icon_size, icon_y))

        # Подсветка зоны
        active_zone = self.assets.get_zone(*mouse_pos, self.img_y, self.img_w, self.img_h)
        if active_zone:
            txt_hover = self.font_small.render(f">> {active_zone} <<", True, (0, 255, 150))
            screen.blit(txt_hover, txt_hover.get_rect(center=(self.width // 2, self.img_y + self.img_h + int(self.height * 0.015))))

        # Главный чат урона (выводит "33+33+14+14+78=172")
        pygame.draw.rect(screen, (30, 30, 36), self.rect_chat, border_radius=10)
        pygame.draw.rect(screen, (255, 180, 0), self.rect_chat, width=3, border_radius=10)
        screen.blit(self.font_big.render(calc.last_result, True, (255, 215, 0)), self.font_big.render(calc.last_result, True, (255, 215, 0)).get_rect(center=self.rect_chat.center))

        # ИСПРАВЛЕНО: Кнопка CLEAN (красноватая при наведении, темно-серая обычно)
        c_clean = (130, 60, 60) if self.btn_clean.collidepoint(mouse_pos) else (45, 45, 52)
        pygame.draw.rect(screen, c_clean, self.btn_clean, border_radius=10)
        pygame.draw.rect(screen, (200, 70, 70), self.btn_clean, width=2, border_radius=10)
        txt_cln = self.font_clean.render("CLEAN", True, (255, 200, 200))
        screen.blit(txt_cln, txt_cln.get_rect(center=self.btn_clean.center))

        # Настройки дистанции
        pygame.draw.rect(screen, (50, 50, 60), self.btn_distance_minus, border_radius=8)
        pygame.draw.rect(screen, (50, 50, 60), self.btn_distance_plus, border_radius=8)
        screen.blit(self.font_small.render("-10m", True, (255,255,255)), self.font_small.render("-10m", True, (255,255,255)).get_rect(center=self.btn_distance_minus.center))
        screen.blit(self.font_small.render("+10m", True, (255,255,255)), self.font_small.render("+10m", True, (255,255,255)).get_rect(center=self.btn_distance_plus.center))
        screen.blit(self.font_small.render(f"DISTANCE: {calc.distance} M", True, (180, 180, 180)), self.font_small.render(f"DISTANCE: {calc.distance} M", True, (180, 180, 180)).get_rect(center=(self.width // 2, self.btn_distance_minus.centery)))

        # Оружие и кнопка снизу
        base_dmg = int(calc.weapons[calc.current_weapon]["base"])
        pels = f"x{8 if calc.current_weapon == 'Sawed-Off' else 9}" if (calc.weapons[calc.current_weapon]["class"] == "SG" or calc.current_weapon == "Sawed-Off") else ""
        text_current = f"ACTIVE WEAPON: {calc.current_weapon} ({base_dmg}{pels})"
        screen.blit(self.font_small.render(text_current, True, (255, 255, 255)), (int(self.width * 0.06), int(self.height * 0.83)))

        pygame.draw.rect(screen, (80, 140, 80) if self.btn_weapon_select.collidepoint(mouse_pos) else (60, 100, 60), self.btn_weapon_select, border_radius=12)
        screen.blit(self.font_small.render("WEAPON", True, (255,255,255)), self.font_small.render("WEAPON", True, (255,255,255)).get_rect(center=self.btn_weapon_select.center))

    def handle_click(self, pos, calc):
        if self.btn_distance_minus.collidepoint(pos): calc.distance = max(10, calc.distance - 10)
        elif self.btn_distance_plus.collidepoint(pos): calc.distance = min(800, calc.distance + 10)
        elif self.btn_weapon_select.collidepoint(pos): return "weapon"
        elif self.btn_armor_select.collidepoint(pos): return "armor"
        
        # ИСПРАВЛЕНО: Обработка клика по кнопке CLEAN
        elif self.btn_clean.collidepoint(pos):
            calc.clear_history()
            return None
            
        else:
            zone = self.assets.get_zone(*pos, self.img_y, self.img_w, self.img_h)
            if zone: calc.calculate(zone)
        return None
