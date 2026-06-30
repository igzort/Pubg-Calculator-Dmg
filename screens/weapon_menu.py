import pygame

class WeaponMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_small = pygame.font.SysFont(None, int(width * 0.041)) 
        self.font_big = pygame.font.SysFont(None, int(width * 0.065))
        
        self.selected_category = None
        self.categories = ["AR", "DMR", "SR", "Shotgun", "Pistols", "LMG", "SMG", "Others"]
        
        # Кнопки категорий генерируем ОДИН раз при старте
        self.cat_buttons = {}
        for i, cat in enumerate(self.categories):
            x = int(width * 0.07) + (i % 2) * int(width * 0.45)
            y = int(height * 0.20) + (i // 2) * int(height * 0.12)
            self.cat_buttons[cat] = pygame.Rect(x, y, int(width * 0.40), int(height * 0.09))
            
        self.btn_back = pygame.Rect(int(width * 0.05), int(height * 0.88), int(width * 0.9), int(height * 0.07))
        
        # Хранилище для кнопок оружия выбранной категории (всегда инициализировано)
        self.current_wpn_buttons = {}

    def _rebuild_weapon_buttons(self, calc):
        """Вспомогательный метод: строит кнопки оружия только при смене категории"""
        self.current_wpn_buttons.clear()
        if self.selected_category is None:
            return

        wpn_class_map = {"Shotgun": "SG", "Pistols": "HG"}
        target_class = wpn_class_map.get(self.selected_category, self.selected_category)
        filtered_weapons = [name for name, d in calc.weapons.items() if d["class"] == target_class]
        
        for i, name in enumerate(filtered_weapons):
            x = int(self.width * 0.07) + (i % 2) * int(self.width * 0.45)
            y = int(self.height * 0.18) + (i // 2) * int(self.height * 0.09)
            self.current_wpn_buttons[name] = pygame.Rect(x, y, int(self.width * 0.40), int(self.height * 0.07))

    def draw(self, screen, calc, mouse_pos):
        # --- ЭКРАН 1: ВЫБОР КАТЕГОРИИ ---
        if self.selected_category is None:
            title = self.font_big.render("SELECT CATEGORY:", True, (255, 180, 0))
            screen.blit(title, title.get_rect(center=(self.width // 2, int(self.height * 0.11))))
            
            for cat, rect in self.cat_buttons.items():
                color = (80, 80, 100) if rect.collidepoint(mouse_pos) else (35, 35, 40)
                pygame.draw.rect(screen, color, rect, border_radius=10)
                txt = self.font_small.render(cat.upper(), True, (255, 255, 255))
                screen.blit(txt, txt.get_rect(center=rect.center))
                
            pygame.draw.rect(screen, (80, 50, 50), self.btn_back, border_radius=12)
            screen.blit(self.font_small.render("CLOSE MENU", True, (255,255,255)), self.font_small.render("CLOSE MENU", True, (255,255,255)).get_rect(center=self.btn_back.center))
            return

        # --- ЭКРАН 2: ВЫБОР ОРУЖИЯ ВНУТРИ КАТЕГОРИИ ---
        title = self.font_big.render(f"{self.selected_category.upper()}:", True, (0, 255, 150))
        screen.blit(title, title.get_rect(center=(self.width // 2, int(self.height * 0.11))))
        
        # Теперь draw просто берет уже готовые Rect из словаря без лишних вычислений
        for name, rect in self.current_wpn_buttons.items():
            if rect.collidepoint(mouse_pos): 
                color = (80, 140, 80)
            elif calc.current_weapon == name: 
                color = (50, 50, 70)
            else: 
                color = (35, 35, 40)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            
            base_dmg = calc.weapons[name]["base"]
            wpn_class = calc.weapons[name]["class"]
            
            if wpn_class == "SG" or name == "Sawed-Off":
                pels = 8 if name == "Sawed-Off" else 9
                display_text = f"{name} ({int(base_dmg)}x{pels})"
            else:
                display_text = f"{name} ({int(base_dmg)})"
                
            txt = self.font_small.render(display_text, True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=rect.center))
            
        pygame.draw.rect(screen, (80, 80, 90), self.btn_back, border_radius=12)
        screen.blit(self.font_small.render("BACK TO CATEGORIES", True, (255,255,255)), self.font_small.render("BACK TO CATEGORIES", True, (255,255,255)).get_rect(center=self.btn_back.center))

    def handle_click(self, pos, calc):
        if self.selected_category is None:
            for cat, rect in self.cat_buttons.items():
                if rect.collidepoint(pos):
                    self.selected_category = cat
                    self._rebuild_weapon_buttons(calc) # Перестраиваем кнопки один раз при клике
                    return None
            if self.btn_back.collidepoint(pos):
                return "main"
        else:
            for name, rect in self.current_wpn_buttons.items():
                if rect.collidepoint(pos):
                    calc.current_weapon = name
                    self.selected_category = None
                    calc.last_result = "CLICK TARGET TO RECALC"
                    return "main"
            if self.btn_back.collidepoint(pos):
                self.selected_category = None
                self.current_wpn_buttons.clear() # Очищаем за ненадобностью
        return None
