"""
Game Edukatif Anak TK - Petualangan Angka & Huruf
Main Entry Point
"""

import pygame
import sys
from scenes.menu import MenuScene
from scenes.level_angka import LevelAngkaScene
from scenes.level_huruf import LevelHurufScene
from game_engine import GameEngine

def main():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Game configuration
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    FPS = 60
    
    # Create game engine
    engine = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, FPS)
    
    # Register scenes
    engine.register_scene("menu", MenuScene(engine))
    engine.register_scene("level_angka", LevelAngkaScene(engine))
    engine.register_scene("level_huruf", LevelHurufScene(engine))
    
    # Start with menu scene
    engine.change_scene("menu")
    
    # Main game loop
    engine.run()
    
    # Cleanup
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()