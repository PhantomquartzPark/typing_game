class Settings:
    def __init__(self):
        self.csv_file_path = "./textdata/sample.csv"
        self.font_path = "./font/ipaexg00401/ipaexg.ttf"

        scale = 150*2
        self.screen_width  = 4*scale
        self.screen_height = 3*scale

        self.bg_color = (10, 10, 20)
        self.ft_color = (200, 200, 200)

        self.fontsize = 60
        self.maxwordlen = 45