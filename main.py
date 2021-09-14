import sys
import csv
import random
import pygame

from settings import Settings
from utils import isloweralnum

class TypingGame:
    def __init__(self):
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.font = pygame.font.Font(self.settings.font_path, self.settings.fontsize)
        self.screen.fill(self.settings.bg_color)

        with open(self.settings.csv_file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            self.text_list = [row for row in reader]
        #print(self.text_list)

        self.__init_exam()

    def __init_exam(self):
        index = random.randrange(1, len(self.text_list))
        self.ans = self.text_list[index][0]
        self.text = self.text_list[index][1]
        #self.ans = "pneumonoultramicroscopicsilicovolcanoconiosis"
        self.n_word = 0
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
            #print(keyname) # check
            if (len(self.ans) > self.n_word) and (self.ans[self.n_word] == keyname):
                self.strbuf += keyname
                self.n_word += 1
            if (len(self.ans) <= self.n_word):
                self.__init_exam()

    def __update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.__draw_font(self.text, (self.settings.screen_width/2, self.settings.screen_height/2-150))
        self.__draw_font(self.ans[self.n_word:], (self.settings.screen_width/2, self.settings.screen_height/2-75))
        self.__draw_font(self.strbuf, (self.settings.screen_width/2, self.settings.screen_height/2))
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