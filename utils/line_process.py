'''
Author: yeffky
Date: 2025-02-16 16:10:36
LastEditTime: 2025-02-16 16:42:54
'''
import linecache

# 放入缓存防止内存过载
def get_line_count(filename):
    count = 0
    with open(filename, 'r', encoding='utf-8') as f:
        while True:
            buffer = f.read(1024 * 1)
            if not buffer:
                break
            count += buffer.count('\n')
    return count


def get_article(file_path):
    # 清除linecache模块的缓存
    linecache.clearcache()
    # 获取文件的总行数
    line_count = get_line_count(file_path)
    # 打印文件的总行数
    print('num: ', line_count)
    # 从第二行开始获取
    start_line = 1
    # 循环n次，每次获取文件中的一行
    article_content = ""
    for i in range(line_count):
        last_content = linecache.getline(file_path, start_line)
        article_content += last_content + '\n'
        start_line += 1
    return article_content
        