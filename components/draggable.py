"""
Draggable Component - Object yang bisa di-drag & drop
"""

import pygame
import cairo
import math

class DraggableObject:
    def __init__(self, x, y, width, height, content, color=(100, 150, 255)):
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.width = width
        self.height = height
        self.content = content  # Bisa berupa angka, huruf, atau gambar
        self.color = color
        
        # Drag state
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        
        # Animation
        self.scale = 1.0
        self.target_scale = 1.0
        self.rotation = 0
        
        # Snap target (untuk puzzle)
        self.snap_target = None
        self.snapped = False
    
    def handle_event(self, event):
        """Handle mouse events untuk dragging"""
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if click is inside object
            if self.is_point_inside(mouse_pos[0], mouse_pos[1]):
                self.dragging = True
                self.offset_x = mouse_pos[0] - self.x
                self.offset_y = mouse_pos[1] - self.y
                self.target_scale = 1.2
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                self.target_scale = 1.0
                
                # Check if snapped to target
                if self.snap_target:
                    if self._check_snap():
                        self.snapped = True
                        self.x = self.snap_target['x']
                        self.y = self.snap_target['y']
                        return True  # Berhasil snap
                    else:
                        # Kembali ke posisi awal
                        self.x = self.original_x
                        self.y = self.original_y
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.x = mouse_pos[0] - self.offset_x
                self.y = mouse_pos[1] - self.offset_y
        
        return False
    
    def update(self, dt):
        """Update animations"""
        # Smooth scale animation
        self.scale += (self.target_scale - self.scale) * 10 * dt
        
        # Gentle rotation when dragging
        if self.dragging:
            self.rotation += dt * 2
        else:
            self.rotation *= 0.9
    
    def render(self, ctx):
        """Render draggable object"""
        ctx.save()
        
        # Calculate center
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        
        # Apply transformations
        ctx.translate(center_x, center_y)
        ctx.rotate(self.rotation)
        ctx.scale(self.scale, self.scale)
        ctx.translate(-center_x, -center_y)
        
        # Draw shadow if dragging
        if self.dragging:
            radius = 15
            self._draw_rounded_rect(ctx, self.x + 5, self.y + 5, 
                                   self.width, self.height, radius)
            ctx.set_source_rgba(0, 0, 0, 0.3)
            ctx.fill()
        
        # Draw main shape (rounded rectangle)
        radius = 15
        self._draw_rounded_rect(ctx, self.x, self.y, self.width, self.height, radius)
        
        # Gradient fill
        gradient = cairo.LinearGradient(self.x, self.y, self.x, self.y + self.height)
        gradient.add_color_stop_rgb(0, 
            self.color[0]/255 * 1.2, 
            self.color[1]/255 * 1.2, 
            self.color[2]/255 * 1.2)
        gradient.add_color_stop_rgb(1, 
            self.color[0]/255, 
            self.color[1]/255, 
            self.color[2]/255)
        
        ctx.set_source(gradient)
        ctx.fill_preserve()
        
        # Border
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(3)
        ctx.stroke()
        
        # Draw content (text)
        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(48)
        
        text = str(self.content)
        text_extents = ctx.text_extents(text)
        text_x = self.x + (self.width - text_extents.width) / 2 - text_extents.x_bearing
        text_y = self.y + (self.height - text_extents.height) / 2 - text_extents.y_bearing
        
        # Text shadow
        ctx.set_source_rgba(0, 0, 0, 0.5)
        ctx.move_to(text_x + 2, text_y + 2)
        ctx.show_text(text)
        
        # Text
        ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(text_x, text_y)
        ctx.show_text(text)
        
        ctx.restore()
    
    def is_point_inside(self, px, py):
        """Check if point is inside object"""
        return (self.x <= px <= self.x + self.width and
                self.y <= py <= self.y + self.height)
    
    def set_snap_target(self, x, y, tolerance=50):
        """Set target untuk snapping"""
        self.snap_target = {
            'x': x,
            'y': y,
            'tolerance': tolerance
        }
    
    def _check_snap(self):
        """Check if object is close enough to snap target"""
        if not self.snap_target:
            return False
        
        dx = self.x - self.snap_target['x']
        dy = self.y - self.snap_target['y']
        distance = math.sqrt(dx*dx + dy*dy)
        
        return distance < self.snap_target['tolerance']
    
    def _draw_rounded_rect(self, ctx, x, y, width, height, radius):
        """Helper untuk menggambar rounded rectangle"""
        ctx.new_sub_path()
        ctx.arc(x + width - radius, y + radius, radius, -math.pi/2, 0)
        ctx.arc(x + width - radius, y + height - radius, radius, 0, math.pi/2)
        ctx.arc(x + radius, y + height - radius, radius, math.pi/2, math.pi)
        ctx.arc(x + radius, y + radius, radius, math.pi, 3*math.pi/2)
        ctx.close_path()
    
    def reset_position(self):
        """Reset ke posisi awal"""
        self.x = self.original_x
        self.y = self.original_y
        self.snapped = False