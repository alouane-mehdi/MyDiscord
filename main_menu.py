import pygame
import sys
import subprocess

class MainMenu:
    def __init__(self):
        pygame.init()

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)

        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600

        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('Main Menu')

        self.font = pygame.font.Font(None, 36)

    def draw_button(self, text, x, y, width, height, color, command=None):
        pygame.draw.rect(self.window, color, (x, y, width, height))
        text_surface = self.font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        self.window.blit(text_surface, text_rect)
        if command:
            pygame.draw.rect(self.window, self.BLACK, (x, y, width, height), 2)
            button_rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(self.window, self.BLACK, button_rect, 2)
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    command()

    def show_main_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.window.fill(self.WHITE)

            button_width = 200
            button_height = 50
            button_margin = 20
            button_x = button_margin
            button_y = (self.WINDOW_HEIGHT - (button_height * 3 + button_margin * 2)) / 2
            
            self.draw_button("Salon 1", button_x, button_y, button_width, button_height, self.GRAY)
            self.draw_button("Salon 2", button_x, button_y + button_height + button_margin, button_width, button_height, self.GRAY)
            self.draw_button("Salon 3", button_x, button_y + 2 * (button_height + button_margin), button_width, button_height, self.GRAY, command=self.open_chat_interface)

            pygame.display.update()

    def open_chat_interface(self):
        subprocess.Popen(["python", "chat.py"])
        pygame.quit()  # Arrête l'exécution de la boucle pygame

if __name__ == "__main__":
    MainMenu().show_main_menu()
