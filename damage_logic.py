class DamageCalculator:
    def __init__(self):
        # Актуальная база оружия PUBG ПК
        self.weapons = {
            # --- Штурмовые винтовки (AR) ---
            "M416":       {"base": 41.0, "class": "AR", "drop_start": 60},
            "Beryl M762": {"base": 46.0, "class": "AR", "drop_start": 60},
            "AKM":        {"base": 47.0, "class": "AR", "drop_start": 60},
            "SCAR-L":     {"base": 42.0, "class": "AR", "drop_start": 60},
            "AUG":        {"base": 41.0, "class": "AR", "drop_start": 60},
            "QBZ":        {"base": 42.0, "class": "AR", "drop_start": 60},
            "ACE32":      {"base": 43.0, "class": "AR", "drop_start": 60},
            "FAMAS":      {"base": 39.0, "class": "AR", "drop_start": 50}, 
            "Groza":      {"base": 47.0, "class": "AR", "drop_start": 60}, 
            "G36C":       {"base": 41.0, "class": "AR", "drop_start": 60},
            "K2":         {"base": 41.0, "class": "AR", "drop_start": 60},
            "M16A4":      {"base": 43.0, "class": "AR", "drop_start": 60},
            "Mk47 Mutant":{"base": 49.0, "class": "AR", "drop_start": 60},
            
            # --- Марксманские винтовки (DMR) ---
            "SKS":        {"base": 53.0, "class": "DMR", "drop_start": 100},
            "SLR":        {"base": 58.0, "class": "DMR", "drop_start": 100},
            "Mini14":     {"base": 46.0, "class": "DMR", "drop_start": 100},
            "Mk12":       {"base": 51.0, "class": "DMR", "drop_start": 100},
            "QBU":        {"base": 48.0, "class": "DMR", "drop_start": 100},
            "VSS":        {"base": 35.0, "class": "DMR", "drop_start": 45}, 
            "Mk14 EBR":   {"base": 61.0, "class": "DMR", "drop_start": 120},
            
            # --- Снайперские винтовки (SR) ---
            "Kar98k":     {"base": 79.0,  "class": "SR",  "drop_start": 100},
            "M24":        {"base": 75.0,  "class": "SR",  "drop_start": 120},
            "AWM":        {"base": 105.0, "class": "SR",  "drop_start": 150},
            "Win94":      {"base": 66.0,  "class": "SR",  "drop_start": 100},
            "Lynx AMR":   {"base": 118.0, "class": "SR",  "drop_start": 200},

            # --- Пистолеты-пулеметы (SMG) ---
            "Vector":     {"base": 31.0, "class": "SMG", "drop_start": 30},
            "Micro UZI":  {"base": 26.0, "class": "SMG", "drop_start": 30},
            "UMP45":      {"base": 41.0, "class": "SMG", "drop_start": 45},
            "MP5K":       {"base": 33.0, "class": "SMG", "drop_start": 35},
            "Tommy Gun":  {"base": 40.0, "class": "SMG", "drop_start": 35},
            "PP-19 Bizon":{"base": 36.0, "class": "SMG", "drop_start": 40},
            "P90":        {"base": 35.0, "class": "SMG", "drop_start": 50},
            "JS9":        {"base": 34.0, "class": "SMG", "drop_start": 40},
            "MP9":        {"base": 31.0, "class": "SMG", "drop_start": 35},

            # --- Дробовики (SG) ---
            "S1897":      {"base": 26.0, "class": "SG",  "drop_start": 10},
            "S686":       {"base": 26.0, "class": "SG",  "drop_start": 10},
            "S12K":       {"base": 24.0, "class": "SG",  "drop_start": 8},
            "DBS":        {"base": 26.0, "class": "SG",  "drop_start": 12},
            
            # --- Пистолеты (HG) ---
            "P92":        {"base": 35.0, "class": "HG",  "drop_start": 15},
            "P1911":      {"base": 41.0, "class": "HG",  "drop_start": 15},
            "P18C":       {"base": 23.0, "class": "HG",  "drop_start": 10},
            "Skorpion":   {"base": 22.0, "class": "HG",  "drop_start": 10},
            "R1895":      {"base": 64.0, "class": "HG",  "drop_start": 20},
            "R45":        {"base": 65.0, "class": "HG",  "drop_start": 20},
            "Deagle":     {"base": 62.0, "class": "HG",  "drop_start": 20},
            "Sawed-Off":  {"base": 22.0, "class": "HG",  "drop_start": 5},
            
            # --- Пулеметы (LMG) ---
            "M249":       {"base": 40.0, "class": "LMG", "drop_start": 60},
            "DP-28":      {"base": 51.0, "class": "LMG", "drop_start": 60},
            "MG3":        {"base": 42.0, "class": "LMG", "drop_start": 60},
            
            # --- Особое (Others) ---
            "Crossbow":   {"base": 105.0,"class": "Others","drop_start": 10},
            "Panzerfaust":{"base": 150.0,"class": "Others","drop_start": 15},
            "Mortar":     {"base": 200.0,"class": "Others","drop_start": 300}
        }
        
        # Исправленная и проверенная таблица множителей
        self.multipliers = {
            "HEAD":        {"AR": 2.35, "DMR": 2.35, "SR": 2.50, "SMG": 2.10, "LMG": 2.35, "SG": 1.50, "HG": 2.00, "base": 2.00},
            "NECK":        {"AR": 1.00, "DMR": 1.05, "SR": 1.30, "SMG": 1.00, "LMG": 1.00, "SG": 1.00, "HG": 1.00, "base": 1.00},
            "UPPER_TORSO": {"AR": 1.10, "DMR": 1.15, "SR": 1.15, "SMG": 1.05, "LMG": 1.10, "SG": 1.00, "HG": 1.00, "base": 1.00},
            "LOWER_TORSO": {"AR": 1.00, "DMR": 1.05, "SR": 1.10, "SMG": 1.05, "LMG": 1.10, "SG": 1.00, "HG": 1.00, "base": 1.00},
            "SHOULDERS":   {"AR": 0.90, "DMR": 0.95, "SR": 1.05, "SMG": 1.30, "LMG": 0.90, "SG": 1.00, "HG": 0.90, "base": 0.90},
            "UPPER_ARMS":  {"AR": 0.60, "DMR": 0.65, "SR": 0.70, "SMG": 1.30, "LMG": 0.60, "SG": 1.00, "HG": 0.60, "base": 0.60},
            "FOREARMS":    {"AR": 0.50, "DMR": 0.50, "SR": 0.50, "SMG": 1.30, "LMG": 0.50, "SG": 1.00, "HG": 0.50, "base": 0.50},
            "THIGHS":      {"AR": 0.60, "DMR": 0.65, "SR": 0.70, "SMG": 1.30, "LMG": 0.60, "SG": 1.00, "HG": 0.60, "base": 0.60},
            "CALVES":      {"AR": 0.50, "DMR": 0.50, "SR": 0.50, "SMG": 1.30, "LMG": 0.50, "SG": 1.00, "HG": 0.50, "base": 0.50},
            "FEET":        {"AR": 0.30, "DMR": 0.30, "SR": 0.30, "SMG": 1.30, "LMG": 0.30, "SG": 1.00, "HG": 0.30, "base": 0.30}
        }
        
        self.armor_mods = [1.0, 0.70, 0.60, 0.45]
        self.current_weapon = "M416"
        self.distance = 50
        self.helmet_lvl = 2
        self.vest_lvl = 2  # Отвечает за уровень ARMOR в калькуляторе
        
        # Хранилище истории выстрелов
        self.shots_history = []
        self.last_result = "CLICK TARGET TO START"

    def clear_history(self):
        """Метод для полной очистки истории выстрелов по кнопке CLEAN"""
        self.shots_history.clear()
        self.last_result = "CLEARED"

    def _get_distance_modifier(self, wpn_class, dist, drop_start):
        """Реалистичный расчет падения урона PUBG в зависимости от класса оружия"""
        if dist <= drop_start:
            return 1.0
            
        extra_dist = dist - drop_start
        
        if wpn_class == "SMG":
            return max(0.25, 1.0 - (extra_dist * 0.0035))  
        elif wpn_class == "AR":
            return max(0.40, 1.0 - (extra_dist * 0.0012))  
        elif wpn_class == "DMR":
            return max(0.50, 1.0 - (extra_dist * 0.0006))  
        elif wpn_class == "SR":
            return max(0.60, 1.0 - (extra_dist * 0.0002))  
        elif wpn_class in ["SG", "HG"]:
            return max(0.05, 1.0 - (extra_dist * 0.0200))  
            
        return max(0.40, 1.0 - (extra_dist * 0.0015))

    def calculate(self, body_part):
        wpn = self.weapons[self.current_weapon]
        
        # 1. Расчет баллистического падения урона
        dist_mod = self._get_distance_modifier(wpn["class"], self.distance, wpn["drop_start"])
        real_base = wpn["base"] * dist_mod
        
        # 2. Множитель конкретной части тела
        mult = self.multipliers[body_part].get(wpn["class"], self.multipliers[body_part]["base"])
        
        # 3. Модификатор брони
        armor_mod = 1.0
        if body_part == "HEAD": 
            armor_mod = self.armor_mods[self.helmet_lvl]
        elif body_part == "NECK": 
            armor_mod = 1.0 - ((1.0 - self.armor_mods[self.helmet_lvl]) * 0.75)
        elif body_part in ["UPPER_TORSO", "LOWER_TORSO", "SHOULDERS"]: 
            armor_mod = self.armor_mods[self.vest_lvl]
            
        final_damage = real_base * mult * armor_mod
        
        # Округляем одиночный выстрел до 1 знака
        shot_dmg = round(final_damage, 1)
        
        # Если оружие — дробовик, то считаем урон за весь полный залп дробинок
        if wpn["class"] == "SG" or self.current_weapon == "Sawed-Off":
            pellets = 8 if self.current_weapon == "Sawed-Off" else 9
            shot_dmg = round(shot_dmg * pellets, 1)

        # 4. Добавление в историю (храним строго 5 последних попаданий)
        self.shots_history.append(shot_dmg)
        if len(self.shots_history) > 5:
            self.shots_history.pop(0)

        # 5. Сборка итоговой строки: "33.5+33.5+14.0=81.0"
        shots_str = "+".join(str(dmg) for dmg in self.shots_history)
        total_sum = round(sum(self.shots_history), 1)
        
        self.last_result = f"{shots_str}={total_sum}"
        return final_damage
