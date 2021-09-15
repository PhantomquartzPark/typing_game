import sys
import time
import argparse
import csv
import random
import pygame

from settings import Settings
from utils import isloweralnum

class TypingGame:
    def __init__(self, delay_ans, csv_file_path):
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.font = pygame.font.Font(self.settings.font_path, self.settings.fontsize)
        self.screen.fill(self.settings.bg_color)

        self.delay_ans = delay_ans
        self.n_typo = 0

        with open(csv_file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            self.text_list = [row for row in reader]
        #print(self.text_list)

        self.__init_exam()
        self.start_game = time.perf_counter()

    def __init_exam(self):
        index = random.randrange(1, len(self.text_list))
        #print(index) # check
        self.ans  = str.lower(self.text_list[index][0])
        self.text = self.text_list[index][1] if (len(self.text_list[index]) > 1) else ""
        #self.ans = "pneumonoultramicroscopicsilicovolcanoconiosis"
        self.n_word = 0
        self.strbuf = ""
        self.start_exam = time.perf_counter()

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
            else:
                self.n_typo += 1
            if (len(self.ans) <= self.n_word):
                self.__init_exam()

    def __update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.__draw_font_tl("Time: {:.0f}".format(time.perf_counter()-self.start_game), (0, 0))

        self.__draw_font_tr("Typo: {}".format(self.n_typo), (0, 0))
        self.__draw_font_ct(self.text, (0, -150))
        if (time.perf_counter() - self.start_exam) >= self.delay_ans:
            self.__draw_font_ct(self.ans[self.n_word:], (0, -75))
        self.__draw_font_ct(self.strbuf, (0, 0))

        pygame.display.update()
                        
    def __draw_font(self, strwords, location, color=None):
        if not color:
            color = self.settings.ft_color
        words = self.font.render(strwords, True, color)
        self.screen.blit(words, location)

    # ct; center
    def __draw_font_ct(self, strwords, gap, color=None):
        gap_w, gap_h = gap
        ft_width, ft_height = self.font.size(strwords)
        location = (gap_w+(self.settings.screen_width-ft_width)/2,
                    gap_h+(self.settings.screen_height-ft_height)/2)
        self.__draw_font(strwords, location, color)

    # tl; top-left
    def __draw_font_tl(self, strwords, gap, color=None):
        gap_w, gap_h = gap
        location = (gap_w+0, gap_h+0)
        self.__draw_font(strwords, location, color)

    # tr; top-right
    def __draw_font_tr(self, strwords, gap, color=None):
        gap_w, gap_h = gap
        ft_width, ft_height = self.font.size(strwords)
        location = (gap_w+self.settings.screen_width-ft_width,
                    gap_h+0)
        self.__draw_font(strwords, location, color)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv", default="./csv/sample.csv")
    parser.add_argument("-d", "--delay", type=int, default=0)
    args = parser.parse_args()

    game = TypingGame(args.delay, args.csv)
    game.run()