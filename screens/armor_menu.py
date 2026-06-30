import pygame

class ArmorMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_small = pygame.font.SysFont(None, int(width * 0.05))
        self.font_big = pygame.font.SysFont(None, int(width * 0.06))
        
        # Кнопки выбора шлема
        self.btn_helmets = {}
        start_y_helm = int(height * 0.25)
        btn_w = int(width * 0.18)
        btn_h = int(height * 0.08)
        for lvl in range(4): 
            self.btn_helmets[lvl] = pygame.Rect(int(width * 0.08) + lvl * (btn_w + int(width * 0.04)), start_y_helm, btn_w, btn_h)
            
        # Кнопки выбора жилета
        self.btn_vests = {}
        start_y_vest = int(height * 0.48)
        for lvl in range(4):
            self.btn_vests[lvl] = pygame.Rect(int(width * 0.08) + lvl * (btn_w + int(width * 0.04)), start_y_vest, btn_w, btn_h)
            
        self.btn_back = pygame.Rect(int(width * 0.05), int(height * 0.88), int(width * 0.9), int(height * 0.07))

    def draw(self, screen, calc, mouse_pos):
        # Заголовок шлемов
        txt_h = self.font_big.render("SELECT HELMET LEVEL:", True, (255, 180, 0))
        screen.blit(txt_h, txt_h.get_rect(center=(self.width // 2, int(self.height * 0.18))))
        
        # Отрисовка кнопок шлема
        for lvl, rect in self.btn_helmets.items():
            is_selected = calc.helmet_lvl == lvl
            if rect.collidepoint(mouse_pos): 
                color = (140, 110, 70)
            elif is_selected: 
                color = (110, 90, 60) # Выделенный цвет
            else: 
                color = (35, 35, 40)
                
            pygame.draw.rect(screen, color, rect, border_radius=8)
            
            # Золотая рамка для выбранного шлема, серая для остальных
            border_color = (255, 180, 0) if is_selected else (80, 80, 80)
            border_w = 2 if is_selected else 1
            pygame.draw.rect(screen, border_color, rect, width=border_w, border_radius=8)
            
            txt = self.font_small.render(f"Lvl {lvl}" if lvl > 0 else "None", True, (255, 255, 255) if is_selected else (200, 200, 200))
            screen.blit(txt, txt.get_rect(center=rect.center))
            
        # Заголовок жилетов
        txt_v = self.font_big.render("SELECT VEST LEVEL:", True, (255, 180, 0))
        screen.blit(txt_v, txt_v.get_rect(center=(self.width // 2, int(self.height * 0.41))))
        
        # Отрисовка кнопок жилета
        for lvl, rect in self.btn_vests.items():
            is_selected = calc.vest_lvl == lvl
            if rect.collidepoint(mouse_pos): 
                color = (140, 110, 70)
            elif is_selected: 
                color = (110, 90, 60)
            else: 
                color = (35, 35, 40)
                
            pygame.draw.rect(screen, color, rect, border_radius=8)
            
            # Золотая рамка для выбранного жилета
            border_color = (255, 180, 0) if is_selected else (80, 80, 80)
            border_w = 2 if is_selected else 1
            pygame.draw.rect(screen, border_color, rect, width=border_w, border_radius=8)
            
            txt = self.font_small.render(f"Lvl {lvl}" if lvl > 0 else "None", True, (255, 255, 255) if is_selected else (200, 200, 200))
            screen.blit(txt, txt.get_rect(center=rect.center))
            
        # Кнопка BACK
        color_back = (80, 80, 90) if self.btn_back.collidepoint(mouse_pos) else (50, 50, 60)
        pygame.draw.rect(screen, color_back, self.btn_back, border_radius=12)
        txt_b = self.font_small.render("BACK TO CALC", True, (255,255,255))
        screen.blit(txt_b, txt_b.get_rect(center=self.btn_back.center))

    def handle_click(self, pos, calc):
        # Клик переключает состояние, но НЕ возвращает в главное меню
        for lvl, rect in self.btn_helmets.items():
            if rect.collidepoint(pos):
                calc.helmet_lvl = lvl
                calc.last_result = "CLICK TARGET TO RECALC"
                
        for lvl, rect in self.btn_vests.items():
            if rect.collidepoint(pos):
                calc.vest_lvl = lvl
                calc.last_result = "CLICK TARGET TO RECALC"
                
        # Выход из меню происходит ТОЛЬКО здесь
        if self.btn_back.collidepoint(pos):
            return "main"
            
        return None
