import csv
import os
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from utils import create_diver, create_dir

# 初始化浏览器
driver = create_diver()

OUTPUT_DIR = create_dir()
FILE_NAME = os.path.join(OUTPUT_DIR, "bilibili.csv")

# 打开B站首页
driver.get("https://www.bilibili.com/")

# 等待页面加载
time.sleep(5)

# 模拟页面滚动，加载内容
for _ in range(10):  # 滚动10次
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# 获取视频元素
videos = driver.find_elements(By.CSS_SELECTOR, ".bili-video-card")

print(f"共找到{len(videos)}个视频")

# 打开CSV文件准备写入
with open(FILE_NAME, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["标题", "封面图链接", "链接地址"])  # 标题名

    for i, video in enumerate(videos[:100]):
        try:
            # 标题
            try:
                title = video.find_element(By.CSS_SELECTOR, "img").get_attribute("alt").strip()
            except NoSuchElementException:
                title = "未知标题"

            # 封面图
            try:
                img = video.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
            except NoSuchElementException:
                img = "未获取到图片"

            # 链接
            try:
                address = video.find_element(By.CSS_SELECTOR, "a[href*='bilibili']").get_attribute("href")
            except NoSuchElementException:
                address = "未获取到链接"

            print(f"{i + 1}. {title} - {img} - {address}")
            writer.writerow([title, img, address])

        except Exception as e:
            print(f"跳过第 {i + 1} 个元素，原因：{e}")

# 关闭浏览器
driver.quit()

print("程序执行完毕")