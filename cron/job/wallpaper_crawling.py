# 爬取壁纸
from crawling.wallpaper.wallpaper_crawler import craw_wallpaper as cw
from crawling.wallpaper.wallpaper_crawler import craw_random_wallpaper

def craw_wallpaper():
    cw()

def random_wallpaper():
    return craw_random_wallpaper()