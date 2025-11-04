"""
Menu Scene - Tampilan menu utama
"""

import pygame
import cairo
import math
from game_engine import Scene
from components.button import Button

class MenuScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.buttons = []
        self.particles = []
        self.time = 0
        
    def enter(self):
        """Setup menu saat scene dimulai"""
        self.buttons = []
        
        # Create menu buttons
        button_width = 300
        button_height = 80
        start_x = (self.engine.width - button_width) / 2
        start_y = 300
        spacing = 100
        
        # Button Belajar Angka
        btn_angka = Button(
            start_x, start_y, button_width, button_height,
            "🔢 Belajar Angka", (255, 107, 107)
        )
        btn_angka.on_click = lambda: self.engine.change_scene("level_angka")
        self.buttons.append(btn_angka)
        
        # Button Belajar Huruf
        btn_huruf = Button(
            start_x, start_y + spacing, button_width, button_height,
            "🔤 Belajar Huruf", (78, 205, 196)
        )
        btn_huruf.on_click = lambda: self.engine.change_scene("level_huruf")
        self.buttons.append(btn_huruf)
        
        # Button Keluar
        btn_exit = Button(
            start_x, start_y + spacing * 2, button_width, button_height,
            "🚪 Keluar", (255, 159, 64)
        )
        btn_exit.on_click = lambda: self.engine.quit()
        self.buttons.append(btn_exit)
        
        # Initialize particles untuk background
        self.particles = []
        for i in range(30):
            self.particles.append({
                'x': (i * self.engine.width / 30),
                'y': (i * 50) % self.engine.height,
                'size': 20 + (i % 3) * 10,
                'speed': 20 + (i % 4) * 10,
                'color': self._get_random_color(i)
            })
    
    def handle_event(self, event):
        """Handle events"""
        for button in self.buttons:
            button.handle_event(event)
    
    def update(self, dt):
        """Update animations"""
        self.time += dt
        
        # Update buttons
        for button in self.buttons:
            button.update(dt)
        
        # Update particles
        for particle in self.particles:
            particle['y'] += particle['speed'] * dt
            if particle['y'] > self.engine.height:
                particle['y'] = -particle['size']
    
    def render(self, ctx):
        """Render menu"""
        # Draw gradient background
        gradient = cairo.LinearGradient(0, 0, 0, self.engine.height)
        gradient.add_color_stop_rgb(0, 0.4, 0.6, 0.9)  # Biru muda
        gradient.add_color_stop_rgb(1, 0.8, 0.4, 0.9)  # Ungu muda
        ctx.rectangle(0, 0, self.engine.width, self.engine.height)
        ctx.set_source(gradient)
        ctx.fill()
        
        # Draw animated particles
        for particle in self.particles:
            ctx.save()
            # Pulsating effect
            pulse = 0.8 + 0.2 * math.sin(self.time * 2 + particle['x'])
            
            ctx.arc(particle['x'], particle['y'], particle['size'] * pulse, 0, 2 * math.pi)
            ctx.set_source_rgba(
                particle['color'][0],
                particle['color'][1],
                particle['color'][2],
                0.3
            )
            ctx.fill()
            ctx.restore()
        
        # Draw title with shadow
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(72)
        
        title = "Petualangan Belajar"
        text_extents = ctx.text_extents(title)
        title_x = (self.engine.width - text_extents.width) / 2
        title_y = 150
        
        # Title shadow
        ctx.set_source_rgba(0, 0, 0, 0.5)
        ctx.move_to(title_x + 4, title_y + 4)
        ctx.show_text(title)
        
        # Title text
        ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(title_x, title_y)
        ctx.show_text(title)
        
        # Subtitle
        ctx.set_font_size(32)
        subtitle = "untuk Anak TK"
        text_extents = ctx.text_extents(subtitle)
        subtitle_x = (self.engine.width - text_extents.width) / 2
        
        ctx.set_source_rgba(1, 1, 1, 0.9)
        ctx.move_to(subtitle_x, title_y + 50)
        ctx.show_text(subtitle)
        
        # Draw buttons
        for button in self.buttons:
            button.render(ctx)
        
        # Draw stars info (progress)
        self._draw_progress_info(ctx)
    
    def _draw_progress_info(self, ctx):
        """Draw progress stars"""
        ctx.set_font_size(24)
        
        # Stars angka
        stars_angka = self.engine.game_state.get("stars_angka", 0)
        text = f"⭐ Angka: {stars_angka}"
        ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(50, self.engine.height - 100)
        ctx.show_text(text)
        
        # Stars huruf
        stars_huruf = self.engine.game_state.get("stars_huruf", 0)
        text = f"⭐ Huruf: {stars_huruf}"
        ctx.move_to(50, self.engine.height - 60)
        ctx.show_text(text)
    
    def _get_random_color(self, seed):
        """Generate random pastel color"""
        colors = [
            (1, 0.8, 0.8),  # Pink
            (0.8, 1, 0.8),  # Green
            (0.8, 0.8, 1),  # Blue
            (1, 1, 0.8),    # Yellow
            (1, 0.8, 1),    # Magenta
        ]
        return colors[seed % len(colors)]