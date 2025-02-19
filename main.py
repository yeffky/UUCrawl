'''
Author: yeffky
Date: 2025-02-17 12:34:40
LastEditTime: 2025-02-19 16:15:12
'''
from crawler import ip_crawler, data_crawler
from analysis import data_analysis
from pic_generate import pic_generate, html_generate
from post import xiaohongshu_post
import file_handler

if __name__ == '__main__':
    url = 'D:/Project/UUCrawl/Code/pic_generate/pic.html'
    file_handler.start_observer()

    # 获取IP
    # ip = ip_crawler.crawl_ip()
    # 获取数据
    data = data_crawler.crawl_data()
    
    # 数据分析
    data_analysis.analysis_data()
    
    # 生成html
    html_generate.generate_html()
    # 生成图片
    pic_generate.generate_pic(url)

    # 发布小红书
    xiaohongshu_post.post_article()


    