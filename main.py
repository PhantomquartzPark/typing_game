import sys
import pygame

from settings import Settings

class TypingGame:
    def __init__(self):
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.font = pygame.font.Font(None, self.settings.fontsize)
        self.screen.fill(self.settings.bg_color)

    def run(self):
        strbuf = ""
        while True:
            for event in pygame.event.get():
                # press x button (top right of the screen)
                if event.type == pygame.QUIT:
                    sys.exit()
                # press some key
                elif event.type == pygame.KEYDOWN:
                    keyname = pygame.key.name(event.key)
                    # can type a to z (lowercase only)
                    if (len(strbuf) <= 20) and (len(keyname) == 1) \
                    and (ord("a") <= ord(keyname)) \
                    and (ord(keyname) <= ord("z")):
                        print(keyname)
                        strbuf += keyname

            # update
            self.screen.fill(self.settings.bg_color)
            words = self.font.render(strbuf, True, self.settings.ft_color)
            ft_width, ft_height = self.font.size(strbuf)
            self.screen.blit(words, [(self.settings.screen_width-ft_width)/2, (self.settings.screen_height-ft_height)/2])

            pygame.display.update()

if __name__ == "__main__":
    game = TypingGame()
    game.run()