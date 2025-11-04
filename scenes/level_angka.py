"""
Level Angka Scene - Puzzle drag & drop angka
"""

import pygame
import cairo
import random
from game_engine import Scene
from components.button import Button
from components.draggable import DraggableObject

class LevelAngkaScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.draggables = []
        self.targets = []
        self.back_button = None
        self.current_puzzle = None
        self.score = 0
        self.max_score = 3
        self.celebration_timer = 0
    
    def enter(self):
        """Setup level saat scene dimulai"""
        self.draggables = []
        self.targets = []
        self.score = 0
        self.celebration_timer = 0
        
        # Create back button
        self.back_button = Button(50, 50, 150, 60, "← Kembali", (200, 100, 100))
        self.back_button.on_click = lambda: self.engine.change_scene("menu")
        
        # Generate puzzle
        self._generate_puzzle()
    
    def _generate_puzzle(self):
        """Generate puzzle baru"""
        # Tipe puzzle: mengurutkan angka 1-5
        numbers = [1, 2, 3, 4, 5]
        random.shuffle(numbers)
        
        # Create draggable numbers
        start_y = 500
        spacing = 130
        
        for i, num in enumerate(numbers):
            draggable = DraggableObject(
                50 + i * spacing, start_y, 100, 100, num,
                color=(random.randint(100, 255), random.randint(100, 255), random.randint(150, 255))
            )
            self.draggables.append(draggable)
        
        # Create target positions (1-5 urut)
        target_y = 300
        for i in range(1, 6):
            target = {
                'x': 150 + i * 150,
                'y': target_y,
                'expected': i,
                'filled': False
            }
            self.targets.append(target)
            
            # Set snap targets untuk draggables
            for draggable in self.draggables:
                if draggable.content == i:
                    draggable.set_snap_target(target['x'], target['y'], tolerance=60)
    
    def handle_event(self, event):
        """Handle events"""
        self.back_button.handle_event(event)
        
        # Handle draggables
        for draggable in self.draggables:
            if draggable.handle_event(event):
                # Check if correct
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
                # Next puzzle or back to menu
                if self.score >= self.max_score:
                    # Update game state
                    self.engine.game_state["stars_angka"] += 1
                    self.engine.change_scene("menu")
                else:
                    # Reset for next round
                    self.enter()
    
    def render(self, ctx):
        """Render level"""
        # Background gradient
        gradient = cairo.LinearGradient(0, 0, 0, self.engine.height)
        gradient.add_color_stop_rgb(0, 0.9, 0.7, 0.5)
        gradient.add_color_stop_rgb(1, 0.8, 0.9, 0.6)
        ctx.rectangle(0, 0, self.engine.width, self.engine.height)
        ctx.set_source(gradient)
        ctx.fill()
        
        # Draw title
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(48)
        title = "Urutkan Angka 1-5!"
        text_extents = ctx.text_extents(title)
        title_x = (self.engine.width - text_extents.width) / 2
        
        ctx.set_source_rgba(0, 0, 0, 0.5)
        ctx.move_to(title_x + 3, 153)
        ctx.show_text(title)
        
        ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(title_x, 150)
        ctx.show_text(title)
        
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
        size = 100
        
        # Draw dashed box
        ctx.save()
        ctx.set_line_width(3)
        ctx.set_dash([10, 5])
        
        if target['filled']:
            ctx.set_source_rgba(0, 1, 0, 0.5)
        else:
            ctx.set_source_rgba(1, 1, 1, 0.5)
        
        ctx.rectangle(x, y, size, size)
        ctx.stroke()
        
        # Draw number label below
        ctx.set_dash([])
        ctx.set_font_size(24)
        text = str(target['expected'])
        text_extents = ctx.text_extents(text)
        text_x = x + (size - text_extents.width) / 2
        
        ctx.set_source_rgb(0.3, 0.3, 0.3)
        ctx.move_to(text_x, y + size + 30)
        ctx.show_text(text)
        
        ctx.restore()
    
    def _draw_score(self, ctx):
        """Draw current score"""
        ctx.set_font_size(32)
        score_text = f"Skor: {self.score}/{self.max_score}"
        
        ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(self.engine.width - 200, 100)
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
        
        text = "Hebat! 🎉"
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
        
        # Draw text
        ctx.set_source_rgb(1, 0.8, 0)
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
                    if target['expected'] == draggable.content:
                        # Correct!
                        target['filled'] = True
                        self.score += 1
                        
                        # Check if all completed
                        if self.score >= self.max_score:
                            self.celebration_timer = 2.0
                        break