import os

import yaml
from bs4 import BeautifulSoup

from utils import create_diver, create_dir

# 初始化浏览器
driver = create_diver()

OUTPUT_DIR = create_dir()
FILE_NAME = os.path.join(OUTPUT_DIR, "www.douyin.com.yml")

# 打开抖音，最多等待5秒
driver.get("https://www.douyin.com/")
driver.implicitly_wait(5)

# 获取HTML结构
html = driver.page_source
driver.quit()

# 解析html代码
soup = BeautifulSoup(html, "html.parser")


def element_to_dict(element):
    if not hasattr(element, "name") or element.name is None:
        return None

    # 定义父节点
    node = {"tag": element.name}

    # 提取属性
    if element.attrs:
        node["attrs"] = element.attrs

    # 提取文本内容
    text = element.get_text(strip=True)
    if text and text != element.name:
        node["text"] = text

    # 提取子元素
    children = []
    for child in element.children:
        child_dict = element_to_dict(child)
        if child_dict:
            children.append(child_dict)

    # 填充子节点
    if children:
        node["children"] = children

    return node


# 从html中提取结构
structure = element_to_dict(soup.html)

# 保存文件
with open(FILE_NAME, "w", encoding="utf-8") as f:
    yaml.dump(element_to_dict(soup.html), f, allow_unicode=True, sort_keys=False)

print("程序执行完毕")