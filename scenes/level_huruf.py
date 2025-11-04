"""
Level Huruf Scene - Puzzle menyusun kata sederhana
"""

import pygame
import cairo
import random
from game_engine import Scene
from components.button import Button
from components.draggable import DraggableObject

class LevelHurufScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.draggables = []
        self.targets = []
        self.back_button = None
        self.current_word = ""
        self.score = 0
        self.max_score = 3
        self.celebration_timer = 0
        
        # Daftar kata sederhana untuk anak TK
        self.words = ["BOLA", "KUCING", "MAMA", "PAPA", "APEL"]
    
    def enter(self):
        """Setup level saat scene dimulai"""
        self.draggables = []
        self.targets = []
        self.score = 0
        self.celebration_timer = 0
        
        # Create back button
        self.back_button = Button(50, 50, 150, 60, "← Kembali", (100, 200, 100))
        self.back_button.on_click = lambda: self.engine.change_scene("menu")
        
        # Generate puzzle
        self._generate_puzzle()
    
    def _generate_puzzle(self):
        """Generate puzzle kata baru"""
        # Pilih kata random
        self.current_word = random.choice(self.words)
        letters = list(self.current_word)
        random.shuffle(letters)
        
        # Create draggable letters
        start_y = 500
        spacing = 120
        offset_x = (self.engine.width - len(letters) * spacing) / 2
        
        for i, letter in enumerate(letters):
            draggable = DraggableObject(
                offset_x + i * spacing, start_y, 90, 90, letter,
                color=(random.randint(150, 255), random.randint(100, 200), random.randint(150, 255))
            )
            self.draggables.append(draggable)
        
        # Create target positions
        target_y = 280
        target_offset_x = (self.engine.width - len(self.current_word) * spacing) / 2
        
        for i, expected_letter in enumerate(self.current_word):
            target = {
                'x': target_offset_x + i * spacing,
                'y': target_y,
                'expected': expected_letter,
                'filled': False,
                'index': i
            }
            self.targets.append(target)
            
            # Set snap targets untuk draggables
            for draggable in self.draggables:
                if draggable.content == expected_letter:
                    draggable.set_snap_target(target['x'], target['y'], tolerance=60)
    
    def handle_event(self, event):
        """Handle events"""
        self.back_button.handle_event(event)
        
        # Handle draggables
        for draggable in self.draggables:
            if draggable.handle_event(event):
                self._check_answer(draggable)
    
    def update(self, dt):
        """Update logic"""
        self.back_button.update(dt)
        
        for draggable in self.draggables:
            draggable.update(dt)
        
        # Update celebration timer
        if self.celebration_timer > 0:
            self.celebration_timer -= dt
            if self.celebration_timer <= 0:
                # Update game state and return to menu or next round
                if self.score >= self.max_score:
                    self.engine.game_state["stars_huruf"] += 1
                    self.engine.change_scene("menu")
                else:
                    self.enter()
    
    def render(self, ctx):
        """Render level"""
        # Background gradient
        gradient = cairo.LinearGradient(0, 0, 0, self.engine.height)
        gradient.add_color_stop_rgb(0, 0.6, 0.8, 0.9)
        gradient.add_color_stop_rgb(1, 0.9, 0.6, 0.8)
        ctx.rectangle(0, 0, self.engine.width, self.engine.height)
        ctx.set_source(gradient)
        ctx.fill()
        
        # Draw title
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(48)
        title = f"Susun Kata: {self.current_word}"
        text_extents = ctx.text_extents(title)
        title_x = (self.engine.width - text_extents.width) / 2
        
        ctx.set_source_rgba(0, 0, 0, 0.5)
        ctx.move_to(title_x + 3, 153)
        ctx.show_text(title)
        
        ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(title_x, 150)
        ctx.show_text(title)
        
        # Draw instruction
        ctx.set_font_size(28)
        instruction = "Tarik huruf ke kotak yang tepat!"
        text_extents = ctx.text_extents(instruction)
        instr_x = (self.engine.width - text_extents.width) / 2
        
        ctx.set_source_rgb(0.2, 0.2, 0.2)
        ctx.move_to(instr_x, 200)
        ctx.show_text(instruction)
        
        # Draw target boxes
        for target in self.targets:
            self._draw_target(ctx, target)
        
        # Draw draggables
        for draggable in self.draggables:
            draggable.render(ctx)
        
        # Draw score
        self._draw_score(ctx)
        
        # Draw back button
        self.back_button.render(ctx)
        
        # Draw celebration if completed
        if self.celebration_timer > 0:
            self._draw_celebration(ctx)
    
    def _draw_target(self, ctx, target):
        """Draw target box"""
        x, y = target['x'], target['y']
        size = 90
        
        # Draw dashed box
        ctx.save()
        ctx.set_line_width(4)
        ctx.set_dash([10, 5])
        
        if target['filled']:
            ctx.set_source_rgba(0, 1, 0, 0.6)
        else:
            ctx.set_source_rgba(1, 1, 1, 0.6)
        
        ctx.rectangle(x, y, size, size)
        ctx.stroke()
        
        # Draw index number below
        ctx.set_dash([])
        ctx.set_font_size(20)
        text = str(target['index'] + 1)
        text_extents = ctx.text_extents(text)
        text_x = x + (size - text_extents.width) / 2
        
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.move_to(text_x, y + size + 25)
        ctx.show_text(text)
        
        ctx.restore()
    
    def _draw_score(self, ctx):
        """Draw current score"""
        ctx.set_font_size(32)
        score_text = f"Kata Selesai: {self.score}/{self.max_score}"
        
        ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(self.engine.width - 300, 100)
        ctx.show_text(score_text)
    
    def _draw_celebration(self, ctx):
        """Draw celebration overlay"""
        # Semi-transparent overlay
        ctx.set_source_rgba(0, 0, 0, 0.7)
        ctx.rectangle(0, 0, self.engine.width, self.engine.height)
        ctx.fill()
        
        # Celebration text
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(72)
        
        text = "Pintar Sekali! 🌟"
        text_extents = ctx.text_extents(text)
        text_x = (self.engine.width - text_extents.width) / 2
        text_y = self.engine.height / 2
        
        # Pulsating effect
        import math
        scale = 1.0 + 0.1 * math.sin(self.celebration_timer * 10)
        
        ctx.save()
        ctx.translate(self.engine.width/2, self.engine.height/2)
        ctx.scale(scale, scale)
        ctx.translate(-self.engine.width/2, -self.engine.height/2)
        
        # Rainbow gradient text
        gradient = cairo.LinearGradient(text_x, text_y - 50, text_x, text_y + 50)
        gradient.add_color_stop_rgb(0, 1, 0.5, 0.5)
        gradient.add_color_stop_rgb(0.5, 0.5, 1, 0.5)
        gradient.add_color_stop_rgb(1, 0.5, 0.5, 1)
        
        ctx.set_source(gradient)
        ctx.move_to(text_x, text_y)
        ctx.show_text(text)
        
        ctx.restore()
    
    def _check_answer(self, draggable):
        """Check if draggable is in correct position"""
        if draggable.snapped:
            # Find which target it snapped to
            for target in self.targets:
                dx = abs(draggable.x - target['x'])
                dy = abs(draggable.y - target['y'])
                
                if dx < 10 and dy < 10:  # Close enough
                    if target['expected'] == draggable.content and not target['filled']:
                        # Correct!
                        target['filled'] = True
                        
                        # Check if whole word is completed
                        if all(t['filled'] for t in self.targets):
                            self.score += 1
                            if self.score >= self.max_score:
                                self.celebration_timer = 2.5
                            else:
                                # Reset untuk kata baru
                                self.celebration_timer = 1.5
                        break