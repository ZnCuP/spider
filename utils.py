import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_diver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')  # 不打开浏览器窗口
        options.add_argument('--disable-gpu')
    # 下载符合版本匹配的驱动，充当浏览器和Selenium的桥梁
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def create_dir(path="output_file"):
    if not os.path.exists(path):
        os.makedirs(path)
    return path
