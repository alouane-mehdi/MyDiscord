import pygame
import sys
from chat_window import ChatWindow  # Importe la classe ChatWindow
from db import Database

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

    def draw_button(self, text, x, y, width, height, color):
        pygame.draw.rect(self.window, color, (x, y, width, height))
        text_surface = self.font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        self.window.blit(text_surface, text_rect)

    def open_chat_window(self, server, username, password, database):
        db = Database(server, username, password, database)
        db_connection = db.get_connection()

        if db_connection is not None:
            chat_window = ChatWindow(db_connection)
            chat_window.show()
        else:
            print("Échec de la connexion à la base de données.")

    def show_main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 20 <= mouse_x <= 220 and 100 <= mouse_y <= 150:
                        self.open_chat_window('ahmed-aouad.students-laplateforme.io', 'ahmed-aouad', 'ouarda2017', 'ahmed-aouad_mydiscord')

            self.window.fill(self.WHITE)

            button_width = 200
            button_height = 50
            button_margin = 20
            button_x = button_margin
            button_y = (self.WINDOW_HEIGHT - (button_height * 3 + button_margin * 2)) / 2
            
            self.draw_button("Salon 1", button_x, button_y, button_width, button_height, self.GRAY)
            self.draw_button("Salon 2", button_x, button_y + button_height + button_margin, button_width, button_height, self.GRAY)
            self.draw_button("Salon 3", button_x, button_y + 2 * (button_height + button_margin), button_width, button_height, self.GRAY)

            pygame.display.update()

if __name__ == "__main__":
    MainMenu().show_main_menu()
