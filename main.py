import sys
import time
import argparse
import csv
import random
import pygame

from settings import Settings
from utils import isavailable

class TypingGame:
    def __init__(self, args):
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.main_font = pygame.font.Font(self.settings.font_path, self.settings.main_fontsize)
        self.sub_font = pygame.font.Font(self.settings.font_path, self.settings.sub_fontsize)
        self.screen.fill(self.settings.bg_color)

        self.delay_ans = abs(args.delay)
        self.delay_opt = 1 if (args.delay < 0) else 0
        self.trans = args.trans
        self.replace_space = args.replace_space
        self.mode = args.mode
        self.n_typo = 0

        with open(args.csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            self.text_list = [row for row in reader]
        #print(self.text_list)

        self.exam_indicies = []
        self.start_game = time.perf_counter()

    def __init_exam(self):
        if self.mode == "s": # s; sample
            if len(self.exam_indicies) == 0:
                self.exam_indicies = random.sample(range(1, len(self.text_list)), len(self.text_list)-1)
            index = self.exam_indicies.pop(0)
        elif self.mode == "c": # c; choices (random.choices() cannot use in python3.5)
            index = random.randrange(1, len(self.text_list))
        
        self.ans = self.text_list[index][0]
        if self.trans == "u":
            self.ans  = str.upper(self.ans)
        elif self.trans == "l":
            self.ans  = str.lower(self.ans)
        self.ans = self.ans.replace(" ", self.replace_space)
        self.ans = "".join([c if isavailable(c) else "" for c in self.ans])

        self.text    = "" if (len(self.text_list[index]) <= 1) else self.text_list[index][1]
        self.subtext = "" if (len(self.text_list[index]) <= 2) else self.text_list[index][2]
        self.n_word = 0
        self.strbuf = ""
        self.start_exam = time.perf_counter()

    def run(self):
        self.__init_exam()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.__check_keydown_events(event)
            
            self.__update_screen()

    def __check_keydown_events(self, event):
        keycode = event.unicode
        keycode = self.replace_space if (keycode == " ") else keycode
        if (len(keycode) == 1) and isavailable(keycode):
            if keycode == self.ans[self.n_word]:
                self.strbuf += keycode
                self.n_word += 1
            else:
                self.n_typo += 1
            
            if (len(self.ans) <= self.n_word):
                self.__init_exam()

    def __update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.__draw_font_tl(self.main_font, "Time: {:.0f}".format(time.perf_counter()-self.start_game), (0, 0))
        self.__draw_font_tr(self.main_font, "Typo: {}".format(self.n_typo), (0, 0))

        offset = 25
        sec_per_char = 0.1
        
        self.__draw_font_ct(self.sub_font, self.subtext, (0, -225+offset))
        self.__draw_font_ct(self.sub_font, self.text, (0, -150+offset))
        if (time.perf_counter() - self.start_exam) >= (self.delay_opt*sec_per_char*len(self.ans) + self.delay_ans):
            self.__draw_font_ct(self.main_font, self.ans[self.n_word:], (0, -75+offset))
        self.__draw_font_ct(self.main_font, self.strbuf, (0, 0+offset))

        pygame.display.update()
                        
    def __draw_font(self, font, strwords, location, color=None):
        if not color:
            color = self.settings.ft_color
        words = font.render(strwords, True, color)
        self.screen.blit(words, location)

    # ct; center
    def __draw_font_ct(self, font, strwords, gap, color=None):
        gap_w, gap_h = gap
        ft_width, ft_height = font.size(strwords)
        location = (gap_w+(self.settings.screen_width-ft_width)/2,
                    gap_h+(self.settings.screen_height-ft_height)/2)
        self.__draw_font(font, strwords, location, color)

    # tl; top-left
    def __draw_font_tl(self, font, strwords, gap, color=None):
        gap_w, gap_h = gap
        location = (gap_w+0, gap_h+0)
        self.__draw_font(font, strwords, location, color)

    # tr; top-right
    def __draw_font_tr(self, font, strwords, gap, color=None):
        gap_w, gap_h = gap
        ft_width, ft_height = font.size(strwords)
        location = (gap_w+self.settings.screen_width-ft_width,
                    gap_h+0)
        self.__draw_font(font, strwords, location, color)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv", default="./csv/sample.csv")
    parser.add_argument("-d", "--delay", type=int, default=0)
    parser.add_argument("-r", "--replace_space", choices=[" ", "_"], default=" ")
    parser.add_argument("-t", "--trans", choices=["l", "u"])
    parser.add_argument("-m", "--mode", choices=["s", "c"], default="s")
    args = parser.parse_args()

    game = TypingGame(args)
    game.run()