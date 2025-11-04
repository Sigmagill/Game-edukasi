"""
Game Engine - Mengelola scenes, events, dan rendering
"""

import pygame
import cairo
import numpy as np

class GameEngine:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        
        # Pygame setup
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Petualangan Angka & Huruf")
        self.clock = pygame.time.Clock()
        
        # Cairo surface setup untuk rendering smooth
        self.cairo_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.cairo_context = cairo.Context(self.cairo_surface)
        
        # Scene management
        self.scenes = {}
        self.current_scene = None
        self.running = True
        
        # Game state untuk menyimpan progress
        self.game_state = {
            "stars_angka": 0,
            "stars_huruf": 0,
            "level_unlocked": 1
        }
    
    def register_scene(self, name, scene):
        """Register scene baru"""
        self.scenes[name] = scene
    
    def change_scene(self, name):
        """Pindah ke scene lain"""
        if name in self.scenes:
            if self.current_scene:
                self.current_scene.exit()
            self.current_scene = self.scenes[name]
            self.current_scene.enter()
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0  # Delta time in seconds
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Pass events to current scene
                if self.current_scene:
                    self.current_scene.handle_event(event)
            
            # Update current scene
            if self.current_scene:
                self.current_scene.update(dt)
            
            # Clear Cairo surface
            self.cairo_context.set_source_rgb(1, 1, 1)
            self.cairo_context.paint()
            
            # Render current scene
            if self.current_scene:
                self.current_scene.render(self.cairo_context)
            
            # Convert Cairo surface to Pygame surface
            buf = self.cairo_surface.get_data()
            image = pygame.image.frombuffer(buf, (self.width, self.height), 'ARGB')
            self.screen.blit(image, (0, 0))
            
            # Update display
            pygame.display.flip()
    
    def quit(self):
        """Stop game loop"""
        self.running = False

class Scene:
    """Base class untuk semua scene"""
    def __init__(self, engine):
        self.engine = engine
    
    def enter(self):
        """Dipanggil saat scene dimulai"""
        pass
    
    def exit(self):
        """Dipanggil saat scene berakhir"""
        pass
    
    def handle_event(self, event):
        """Handle pygame events"""
        pass
    
    def update(self, dt):
        """Update logic"""
        pass
    
    def render(self, ctx):
        """Render dengan Cairo context"""
        pass