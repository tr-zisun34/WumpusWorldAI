import pygame
import random
from dataclasses import dataclass
from typing import List, Tuple
import pygame.gfxdraw
import sys
from Map import *
from Agent import *
from Graphic import *
from Algorithms import *

# Enhanced color palette for consistent styling
@dataclass
class GameColors:
    PRIMARY = (48, 25, 52)
    SECONDARY = (101, 67, 133)
    ACCENT = (255, 195, 0)
    BACKGROUND = (24, 12, 26)
    TEXT_PRIMARY = (255, 255, 255)
    TEXT_SECONDARY = (180, 180, 180)
    BUTTON_HOVER = (143, 95, 188)
    BUTTON_ACTIVE = (81, 54, 107)
    TRANSPARENT = (0, 0, 0, 0)

class ParticleSystem:
    def __init__(self):
        self.particles: List[dict] = []
        
    def create_particle(self, x: int, y: int, color: Tuple[int, int, int]):
        self.particles.append({
            'x': x,
            'y': y,
            'dx': random.uniform(-1, 1),
            'dy': random.uniform(-1, 1),
            'lifetime': random.uniform(0.5, 2.0),
            'color': color,
            'size': random.uniform(2, 4)
        })
    
    def update(self, dt: float):
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['lifetime'] -= dt
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        for particle in self.particles:
            alpha = int(255 * (particle['lifetime'] / 2.0))
            color = (*particle['color'], alpha)
            pygame.gfxdraw.filled_circle(
                screen,
                int(particle['x']),
                int(particle['y']),
                int(particle['size']),
                color
            )

class AnimatedButton:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.font.Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hover = False
        self.scale = 1.0
        self.target_scale = 1.0
        
    def update(self, mouse_pos: Tuple[int, int], dt: float):
        self.hover = self.rect.collidepoint(mouse_pos)
        self.target_scale = 1.1 if self.hover else 1.0
        self.scale += (self.target_scale - self.scale) * dt * 10
        
    def draw(self, screen: pygame.Surface):
        scaled_rect = self.rect.copy()
        scaled_rect.width *= self.scale
        scaled_rect.height *= self.scale
        scaled_rect.center = self.rect.center
        
        # Draw button background with gradient
        gradient_rect = scaled_rect.copy()
        for i in range(scaled_rect.height):
            progress = i / scaled_rect.height
            if self.hover:
                color = tuple(map(lambda x, y: int(x + (y - x) * progress),
                                GameColors.BUTTON_ACTIVE,
                                GameColors.BUTTON_HOVER))
            else:
                color = tuple(map(lambda x, y: int(x + (y - x) * progress),
                                GameColors.PRIMARY,
                                GameColors.SECONDARY))
            pygame.draw.line(screen, color,
                           (scaled_rect.left, scaled_rect.top + i),
                           (scaled_rect.right, scaled_rect.top + i))
        
        # Draw text
        text_surf = self.font.render(self.text, True, GameColors.TEXT_PRIMARY)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        screen.blit(text_surf, text_rect)
        
        # Draw border
        pygame.draw.rect(screen, GameColors.ACCENT, scaled_rect, 2, border_radius=10)

class EnhancedGraphic(Graphic):
    def __init__(self):
        super().__init__()
        self.particles = ParticleSystem()
        self.buttons = []
        self.score_animation = {'current': 0, 'target': 0}
        self.setup_buttons()
        
    def setup_buttons(self):
        button_width = 500
        button_height = 50
        start_y = 120
        spacing = 80
        
        for i, text in enumerate(["MAP 1", "MAP 2", "MAP 3", "MAP 4", "MAP 5", "EXIT"]):
            self.buttons.append(
                AnimatedButton(
                    (SCREEN_WIDTH - button_width) // 2,
                    start_y + i * spacing,
                    button_width,
                    button_height,
                    text,
                    self.font
                )
            )
    
    def home_draw(self):
        # Create atmospheric background
        self.screen.fill(GameColors.BACKGROUND)
        
        # Draw animated particles
        self.particles.update(1/60)
        for _ in range(2):
            self.particles.create_particle(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                GameColors.ACCENT
            )
        self.particles.draw(self.screen)
        
        # Draw title
        title = self.victory.render("WUMPUS WORLD", True, GameColors.ACCENT)
        title_rect = title.get_rect(centerx=SCREEN_WIDTH//2, top=20)
        self.screen.blit(title, title_rect)
        
        # Draw animated buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos, 1/60)
            button.draw(self.screen)
    
    def running_draw(self):
        self.screen.fill(GameColors.BACKGROUND)
        self.map.draw(self.screen)
        
        # Animate score
        score = self.agent.get_score()
        self.score_animation['target'] = score
        self.score_animation['current'] += (self.score_animation['target'] - 
                                          self.score_animation['current']) * 0.1
        
        # Draw modern HUD
        self._draw_hud()
        
    def _draw_hud(self):
        # Score panel at the top right
        panel_rect = pygame.Rect(SCREEN_WIDTH - 250, 10, 240, 80)
        pygame.draw.rect(self.screen, GameColors.PRIMARY, panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, GameColors.ACCENT, panel_rect, 2, border_radius=10)
        
        score_text = f"SCORE: {int(self.score_animation['current']):,}"
        score_surf = self.font.render(score_text, True, GameColors.TEXT_PRIMARY)
        score_rect = score_surf.get_rect(center=panel_rect.center)
        self.screen.blit(score_surf, score_rect)
        
        # Status indicators
        self._draw_status_indicators()
        
    def _draw_status_indicators(self):
        # Position directly below the score panel
        indicators_rect = pygame.Rect(SCREEN_WIDTH - 250, 100, 240, 80)
        pygame.draw.rect(self.screen, GameColors.PRIMARY, indicators_rect, border_radius=10)
        pygame.draw.rect(self.screen, GameColors.ACCENT, indicators_rect, 2, border_radius=10)
        
        # Adjust text position within the indicator rectangle
        status_text = self.noti.render("STATUS: Active", True, GameColors.TEXT_SECONDARY)
        text_pos = (indicators_rect.x + 10, indicators_rect.y + 20)
        self.screen.blit(status_text, text_pos)
    
    def win_draw(self):
        self.screen.fill(GameColors.BACKGROUND)
        
        # Create victory/defeat effects
        for _ in range(5):
            self.particles.create_particle(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                GameColors.ACCENT
            )
        self.particles.update(1/60)
        self.particles.draw(self.screen)
        
        # Draw victory/defeat message
        if self.state == WIN:
            message = 'VICTORY!!!'
            color = GameColors.ACCENT
        else:
            message = 'TRY BEST!!!'
            color = GameColors.TEXT_SECONDARY
            
        text = self.victory.render(message, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        
        # Add glow effect
        glow_surf = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        glow_color = (*color, 100)
        glow_text = self.victory.render(message, True, glow_color)
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow_surf.blit(glow_text, offset)
        self.screen.blit(glow_surf, text_rect)
        self.screen.blit(text, text_rect)
        
        # Draw animated score
        score = self.agent.get_score()
        score_text = self.victory.render(f'Score: {score}', True, GameColors.TEXT_PRIMARY)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(score_text, score_rect)
        
        # Add return to menu button
        return_button = AnimatedButton(
            SCREEN_WIDTH//4, 
            3*SCREEN_HEIGHT//4,
            SCREEN_WIDTH//2,
            50,
            "Return to Menu",
            self.font
        )
        return_button.update(pygame.mouse.get_pos(), 1/60)
        return_button.draw(self.screen)

# Update the original game's display_action method with visual feedback
def display_action(self, action: Algorithms.Action):
    # Add visual feedback particles for actions
    i, j = self.agent.get_pos()
    # screen_x = j * CELL_SIZE + CELL_SIZE//2
    # screen_y = i * CELL_SIZE + CELL_SIZE//2
    screen_x = j * 2 + 2
    screen_y = i * 2 + 2
    
    if action in [Algorithms.Action.MOVE_FORWARD, Algorithms.Action.GRAB_GOLD]:
        for _ in range(10):
            self.particles.create_particle(screen_x, screen_y, GameColors.ACCENT)
            
    # Call original display_action logic
    super().display_action(action)


# import pygame
# import random
# from dataclasses import dataclass
# from typing import List, Tuple
# import pygame.gfxdraw
# import sys
# from Map import *
# from Agent import *
# from Graphic import *
# from Algorithms import *

# # Updated color palette for sky blue and cream theme
# @dataclass
# class GameColors:
#     PRIMARY = (135, 206, 235)  # Sky blue for main UI elements
#     SECONDARY = (173, 216, 230)  # Lighter sky blue for gradients
#     ACCENT = (255, 245, 220)  # Cream for highlights
#     BACKGROUND = (240, 248, 255)  # Very light blue (almost white) for background
#     TEXT_PRIMARY = (255, 255, 255)  # White for primary text
#     TEXT_SECONDARY = (70, 130, 180)  # Steel blue for secondary text
#     BUTTON_HOVER = (100, 180, 220)  # Darker sky blue for button hover
#     BUTTON_ACTIVE = (70, 150, 190)  # Even darker sky blue for button active
#     TRANSPARENT = (0, 0, 0, 0)  # Transparent for effects

# class ParticleSystem:
#     def __init__(self):
#         self.particles: List[dict] = []
        
#     def create_particle(self, x: int, y: int, color: Tuple[int, int, int]):
#         self.particles.append({
#             'x': x,
#             'y': y,
#             'dx': random.uniform(-2, 2),
#             'dy': random.uniform(-2, 2),
#             'lifetime': random.uniform(0.3, 1.5),
#             'color': color,
#             'size': random.uniform(2, 5)
#         })
    
#     def update(self, dt: float):
#         for particle in self.particles[:]:
#             particle['x'] += particle['dx'] * dt * 60
#             particle['y'] += particle['dy'] * dt * 60
#             particle['lifetime'] -= dt
#             if particle['lifetime'] <= 0:
#                 self.particles.remove(particle)
    
#     def draw(self, screen: pygame.Surface):
#         for particle in self.particles:
#             alpha = int(255 * (particle['lifetime'] / 1.5))
#             color = (*particle['color'][:3], alpha)
#             pygame.gfxdraw.filled_circle(
#                 screen,
#                 int(particle['x']),
#                 int(particle['y']),
#                 int(particle['size']),
#                 color
#             )

# class AnimatedButton:
#     def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pygame.font.Font):
#         self.rect = pygame.Rect(x, y, width, height)
#         self.text = text
#         self.font = font
#         self.hover = False
#         self.scale = 1.0
#         self.target_scale = 1.0
        
#     def update(self, mouse_pos: Tuple[int, int], dt: float):
#         self.hover = self.rect.collidepoint(mouse_pos)
#         self.target_scale = 1.15 if self.hover else 1.0
#         self.scale += (self.target_scale - self.scale) * dt * 8
        
#     def draw(self, screen: pygame.Surface):
#         scaled_rect = self.rect.copy()
#         scaled_rect.width = int(scaled_rect.width * self.scale)
#         scaled_rect.height = int(scaled_rect.height * self.scale)
#         scaled_rect.center = self.rect.center
        
#         # Draw button background with gradient
#         gradient_surf = pygame.Surface(scaled_rect.size, pygame.SRCALPHA)
#         for i in range(scaled_rect.height):
#             progress = i / scaled_rect.height
#             if self.hover:
#                 color = tuple(int(x + (y - x) * progress) for x, y in zip(GameColors.BUTTON_ACTIVE, GameColors.BUTTON_HOVER))
#             else:
#                 color = tuple(int(x + (y - x) * progress) for x, y in zip(GameColors.PRIMARY, GameColors.SECONDARY))
#             pygame.draw.line(gradient_surf, color, (0, i), (scaled_rect.width, i))
#         screen.blit(gradient_surf, scaled_rect)
        
#         # Draw text
#         text_surf = self.font.render(self.text, True, GameColors.TEXT_SECONDARY)
#         text_rect = text_surf.get_rect(center=scaled_rect.center)
#         screen.blit(text_surf, text_rect)
        
#         # Draw border with rounded corners
#         pygame.draw.rect(screen, GameColors.ACCENT, scaled_rect, 2, border_radius=15)

# class EnhancedGraphic(Graphic):
#     def __init__(self):
#         super().__init__()
#         self.particles = ParticleSystem()
#         self.buttons = []
#         self.score_animation = {'current': 0, 'target': 0}
#         self.title_font = pygame.font.Font(FONT_MRSMONSTER, 80)
#         self.setup_buttons()
        
#     def setup_buttons(self):
#         button_width = 400
#         button_height = 60
#         # Dynamically calculate start_y and spacing based on screen height
#         start_y = 150  # Start below title (assuming title height ~100)
#         spacing = (SCREEN_HEIGHT - start_y - 100) // 6  # Evenly space 6 buttons
#         if spacing < 60:  # Minimum spacing to avoid overlap
#             spacing = 60
            
#         for i, text in enumerate(["MAP 1", "MAP 2", "MAP 3", "MAP 4", "MAP 5", "EXIT"]):
#             self.buttons.append(
#                 AnimatedButton(
#                     (SCREEN_WIDTH - button_width) // 2,
#                     start_y + i * spacing,
#                     button_width,
#                     button_height,
#                     text,
#                     self.font
#                 )
#             )
    
#     def home_draw(self):
#         # Draw background with subtle gradient
#         gradient_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
#         for i in range(SCREEN_HEIGHT):
#             progress = i / SCREEN_HEIGHT
#             color = tuple(int(x + (y - x) * progress) for x, y in zip(GameColors.BACKGROUND, GameColors.PRIMARY))
#             pygame.draw.line(gradient_surf, color, (0, i), (SCREEN_WIDTH, i))
#         self.screen.blit(gradient_surf, (0, 0))
        
#         # Draw animated particles
#         self.particles.update(1/60)
#         for _ in range(3):
#             self.particles.create_particle(
#                 random.randint(0, SCREEN_WIDTH),
#                 random.randint(0, SCREEN_HEIGHT),
#                 GameColors.ACCENT
#             )
#         self.particles.draw(self.screen)
        
#         # Draw title with glow effect
#         title = self.title_font.render("WUMPUS WORLD", True, GameColors.ACCENT)
#         title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
#         glow_surf = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
#         glow_color = (*GameColors.ACCENT[:3], 100)
#         glow_text = self.title_font.render("WUMPUS WORLD", True, glow_color)
#         for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
#             glow_surf.blit(glow_text, (10 + offset[0], 10 + offset[1]))
#         self.screen.blit(glow_surf, (title_rect.x - 10, title_rect.y - 10))
#         self.screen.blit(title, title_rect)
        
#         # Draw animated buttons
#         mouse_pos = pygame.mouse.get_pos()
#         for button in self.buttons:
#             button.update(mouse_pos, 1/60)
#             button.draw(self.screen)
    
#     def running_draw(self):
#         self.screen.fill(GameColors.BACKGROUND)
#         self.map.draw(self.screen)
#         self.all_sprites.draw(self.screen)
        
#         # Animate score
#         score = self.agent.get_score()
#         self.score_animation['target'] = score
#         self.score_animation['current'] += (self.score_animation['target'] - 
#                                          self.score_animation['current']) * 0.15
        
#         # Draw HUD with adjusted position to avoid map overlap
#         self._draw_hud()
        
#         # Draw particles
#         self.particles.update(1/60)
#         self.particles.draw(self.screen)
        
#     def _draw_hud(self):
#         # Semi-transparent HUD panel, shifted right and with top margin
#         panel_rect = pygame.Rect(SCREEN_WIDTH - 300, 40, 260, 140)  # Moved right by 20, top by 20
#         panel_surf = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
#         panel_surf.fill((*GameColors.PRIMARY[:3], 180))
#         self.screen.blit(panel_surf, panel_rect)
#         pygame.draw.rect(self.screen, GameColors.ACCENT, panel_rect, 2, border_radius=12)
        
#         # Score display
#         score_text = f"SCORE: {int(self.score_animation['current']):,}"
#         score_surf = self.font.render(score_text, True, GameColors.TEXT_PRIMARY)
#         score_rect = score_surf.get_rect(topleft=(panel_rect.x + 20, panel_rect.y + 20))
#         self.screen.blit(score_surf, score_rect)
        
#         # Status indicators
#         status_text = self.noti.render("STATUS: Active", True, GameColors.TEXT_SECONDARY)
#         status_rect = status_text.get_rect(topleft=(panel_rect.x + 20, panel_rect.y + 60))
#         self.screen.blit(status_text, status_rect)
        
#         # Additional game info
#         pos_text = self.noti.render(f"POS: {self.agent.get_pos()}", True, GameColors.TEXT_SECONDARY)
#         pos_rect = pos_text.get_rect(topleft=(panel_rect.x + 20, panel_rect.y + 80))
#         self.screen.blit(pos_text, pos_rect)
    
#     def win_draw(self):
#         # Draw background gradient
#         gradient_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
#         for i in range(SCREEN_HEIGHT):
#             progress = i / SCREEN_HEIGHT
#             color = tuple(int(x + (y - x) * progress) for x, y in zip(GameColors.BACKGROUND, GameColors.PRIMARY))
#             pygame.draw.line(gradient_surf, color, (0, i), (SCREEN_WIDTH, i))
#         self.screen.blit(gradient_surf, (0, 0))
        
#         # Draw victory/defeat effects
#         self.particles.update(1/60)
#         for _ in range(5):
#             self.particles.create_particle(
#                 random.randint(0, SCREEN_WIDTH),
#                 random.randint(0, SCREEN_HEIGHT),
#                 GameColors.ACCENT
#             )
#         self.particles.draw(self.screen)
        
#         # Draw victory/defeat message
#         message = 'VICTORY!!!' if self.state == WIN else 'TRY AGAIN!!!'
#         color = GameColors.ACCENT if self.state == WIN else GameColors.TEXT_SECONDARY
#         text = self.victory.render(message, True, color)
#         text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        
#         # Add glow effect
#         glow_surf = pygame.Surface((text_rect.width + 20, text_rect.height + 20), pygame.SRCALPHA)
#         glow_color = (*color[:3], 120)
#         glow_text = self.victory.render(message, True, glow_color)
#         for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3)]:
#             glow_surf.blit(glow_text, (10 + offset[0], 10 + offset[1]))
#         self.screen.blit(glow_surf, (text_rect.x - 10, text_rect.y - 10))
#         self.screen.blit(text, text_rect)
        
#         # Draw score
#         score_text = self.victory.render(f'Score: {self.agent.get_score():,}', True, GameColors.TEXT_PRIMARY)
#         score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
#         self.screen.blit(score_text, score_rect)
        
#         # Draw return button
#         return_button = AnimatedButton(
#             SCREEN_WIDTH//4, 
#             3*SCREEN_HEIGHT//4,
#             SCREEN_WIDTH//2,
#             60,
#             "Return to Menu",
#             self.font
#         )
#         return_button.update(pygame.mouse.get_pos(), 1/60)
#         return_button.draw(self.screen)

#     def display_action(self, action: Algorithms.Action):
#         i, j = self.agent.get_pos()
#         screen_x = 40 + j * 70
#         screen_y = 40 + i * 70
        
#         # Add particle effects for key actions
#         if action in [Algorithms.Action.MOVE_FORWARD, Algorithms.Action.GRAB_GOLD, Algorithms.Action.SHOOT]:
#             for _ in range(15):
#                 self.particles.create_particle(screen_x, screen_y, GameColors.ACCENT)
#         elif action in [Algorithms.Action.KILL_WUMPUS]:
#             for _ in range(20):
#                 self.particles.create_particle(screen_x, screen_y, GameColors.SECONDARY)
#             self.wumpus.wumpus_kill(self.screen, self.font)  # Corrected to original args
#             pygame.time.delay(500)
        
#         super().display_action(action)