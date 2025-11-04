"""
Button Component - Tombol interaktif dengan animasi
"""

import pygame
import cairo
import math

class Button:
    def __init__(self, x, y, width, height, text, color, text_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.text_color = text_color
        
        # Animation states
        self.hover = False
        self.pressed = False
        self.scale = 1.0
        self.target_scale = 1.0
        
        # Callback function
        self.on_click = None
    
    def handle_event(self, event):
        """Handle mouse events"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Check if mouse is over button
        self.hover = (self.x <= mouse_pos[0] <= self.x + self.width and
                      self.y <= mouse_pos[1] <= self.y + self.height)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover:
                self.pressed = True
                self.target_scale = 0.95
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.hover:
                # Trigger click callback
                if self.on_click:
                    self.on_click()
            self.pressed = False
            self.target_scale = 1.1 if self.hover else 1.0
    
    def update(self, dt):
        """Update animations"""
        # Smooth scale animation
        self.scale += (self.target_scale - self.scale) * 10 * dt
        
        # Update target scale based on hover
        if not self.pressed:
            self.target_scale = 1.1 if self.hover else 1.0
    
    def render(self, ctx):
        """Render button dengan Cairo"""
        # Save context
        ctx.save()
        
        # Calculate center for scaling
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        
        # Apply scale transform
        ctx.translate(center_x, center_y)
        ctx.scale(self.scale, self.scale)
        ctx.translate(-center_x, -center_y)
        
        # Draw rounded rectangle with gradient
        radius = 20
        
        # Create gradient
        gradient = cairo.LinearGradient(self.x, self.y, self.x, self.y + self.height)
        gradient.add_color_stop_rgb(0, 
            self.color[0]/255 * 1.2, 
            self.color[1]/255 * 1.2, 
            self.color[2]/255 * 1.2)
        gradient.add_color_stop_rgb(1, 
            self.color[0]/255, 
            self.color[1]/255, 
            self.color[2]/255)
        
        # Draw rounded rectangle
        self._draw_rounded_rect(ctx, self.x, self.y, self.width, self.height, radius)
        ctx.set_source(gradient)
        ctx.fill_preserve()
        
        # Draw border
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(3)
        ctx.stroke()
        
        # Draw shadow if hovered
        if self.hover:
            ctx.save()
            self._draw_rounded_rect(ctx, self.x, self.y, self.width, self.height, radius)
            ctx.set_source_rgba(0, 0, 0, 0.3)
            ctx.set_line_width(8)
            ctx.stroke()
            ctx.restore()
        
        # Draw text
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(28)
        
        # Get text extents for centering
        text_extents = ctx.text_extents(self.text)
        text_x = self.x + (self.width - text_extents.width) / 2 - text_extents.x_bearing
        text_y = self.y + (self.height - text_extents.height) / 2 - text_extents.y_bearing
        
        # Draw text shadow
        ctx.set_source_rgba(0, 0, 0, 0.5)
        ctx.move_to(text_x + 2, text_y + 2)
        ctx.show_text(self.text)
        
        # Draw text
        ctx.set_source_rgb(
            self.text_color[0]/255,
            self.text_color[1]/255,
            self.text_color[2]/255
        )
        ctx.move_to(text_x, text_y)
        ctx.show_text(self.text)
        
        # Restore context
        ctx.restore()
    
    def _draw_rounded_rect(self, ctx, x, y, width, height, radius):
        """Helper untuk menggambar rounded rectangle"""
        ctx.new_sub_path()
        ctx.arc(x + width - radius, y + radius, radius, -math.pi/2, 0)
        ctx.arc(x + width - radius, y + height - radius, radius, 0, math.pi/2)
        ctx.arc(x + radius, y + height - radius, radius, math.pi/2, math.pi)
        ctx.arc(x + radius, y + radius, radius, math.pi, 3*math.pi/2)
        ctx.close_path()