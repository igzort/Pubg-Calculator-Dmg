import pygame
import os

class MainScreenAssets:
    def __init__(self, width, height, icon_size):
        # Загрузка карты хитбоксов
        img_path = os.path.join(os.path.dirname(__file__), "..", "hitbox_map.jpg")
        try:
            raw_img = pygame.image.load(img_path).convert()
        except:
            raw_img = pygame.Surface((300, 500))
            raw_img.fill((0, 0, 0))
            
        self.char_img = pygame.transform.smoothscale(raw_img, (width, int(height * 0.53)))
        
        # Списки для спрайтов
        self.helmet_sprites = {}
        self.armor_sprites = {}
        assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        
        for lvl in range(4):
            if lvl == 0:
                self.helmet_sprites[lvl] = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
                self.armor_sprites[lvl] = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
                continue
                
            # Загрузка шлемов (helmet2 - png, остальные - jpg)
            ext_h = ".png" if lvl == 2 else ".jpg"
            h_path = os.path.join(assets_dir, f"helmet{lvl}{ext_h}")
            if os.path.exists(h_path):
                img = pygame.image.load(h_path)
                img = img.convert_alpha() if ext_h == ".png" else img.convert()
                self.helmet_sprites[lvl] = pygame.transform.smoothscale(img, (icon_size, icon_size))
            else:
                self.helmet_sprites[lvl] = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
                
            # Загрузка брони (Все .jpg)
            a_path = os.path.join(assets_dir, f"armor{lvl}.jpg")
            if os.path.exists(a_path):
                img = pygame.image.load(a_path).convert()
                self.armor_sprites[lvl] = pygame.transform.smoothscale(img, (icon_size, icon_size))
            else:
                self.armor_sprites[lvl] = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)

        # Цвета зон
        self.color_map = {
            "HEAD": (255, 0, 0), "NECK": (255, 128, 0), "UPPER_TORSO": (0, 0, 255),
            "LOWER_TORSO": (0, 255, 255), "SHOULDERS": (255, 255, 0), "UPPER_ARMS": (0, 255, 0),
            "FOREARMS": (255, 0, 128), "THIGHS": (128, 0, 128), "CALVES": (128, 255, 128), "FEET": (255, 255, 255)
        }

    def get_zone(self, x, y, img_y, img_w, img_h):
        rel_x, rel_y = x, y - img_y
        if not (0 <= rel_x < img_w and 0 <= rel_y < img_h): return None
        pixel = self.char_img.get_at((rel_x, rel_y))[:3]
        if pixel[0] < 30 and pixel[1] < 30 and pixel[2] < 30: return None
        
        best_zone, min_diff = None, 999999
        for name, color in self.color_map.items():
            diff = (pixel[0]-color[0])**2 + (pixel[1]-color[1])**2 + (pixel[2]-color[2])**2
            if diff < min_diff: best_zone, min_diff = name, diff
        return best_zone if min_diff < 15000 else None
