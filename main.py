import sys
import pygame

from settings import Settings
from utils import isloweralnum

class TypingGame:
    def __init__(self):
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.font = pygame.font.Font(None, self.settings.fontsize)
        self.screen.fill(self.settings.bg_color)

        self.ind = 0
        self.ans = "pneumonoultramicroscopicsilicovolcanoconiosis"
        self.strbuf = ""

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.__check_keydown_events(event)
            
            self.__update_screen()

    def __check_keydown_events(self, event):
        keyname = pygame.key.name(event.key)
        if (len(self.strbuf) < self.settings.maxwordlen) \
        and (len(keyname) == 1) and isloweralnum(keyname):
            print(keyname) # check
            if (len(self.ans) >= self.ind) and (self.ans[self.ind] == keyname):
                self.strbuf += keyname
                self.ind += 1

    def __update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.__draw_font(self.strbuf, (self.settings.screen_width/2, self.settings.screen_height/2))
        self.__draw_font(self.ans[self.ind:], (self.settings.screen_width/2, self.settings.screen_height/2+50))
        pygame.display.update()

    def __draw_font(self, strwords, location, color=None):
        if not color:
            color = self.settings.ft_color
        
        width, height = location
        words = self.font.render(strwords, True, color)
        ft_width, ft_height = self.font.size(strwords)
        self.screen.blit(words, [width-ft_width/2, height-ft_height/2])

if __name__ == "__main__":
    game = TypingGame()
    game.run()