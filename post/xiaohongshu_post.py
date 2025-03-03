'''
Author: yeffky
Date: 2025-02-15 20:28:32
LastEditTime: 2025-03-03 15:35:12
'''
import sys
sys.path.append("./")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from utils import line_process
import time
import json
import os
import requests
from datetime import datetime

class XiaohongshuClient:
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        # 获取当前执行文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.token_file = os.path.join(current_dir, "xiaohongshu_token.json")
        self.cookies_file = os.path.join(current_dir, "xiaohongshu_cookies.json")
        self.token = self._load_token()
        self._load_cookies()
        
    def _load_token(self):
        """从文件加载token"""
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as f:
                    token_data = json.load(f)
                    # 检查token是否过期
                    if token_data.get('expire_time', 0) > time.time():
                        return token_data.get('token')
            except:
                pass
        return None
        
    def _save_token(self, token):
        """保存token到文件"""
        token_data = {
            'token': token,
            # token有效期设为30天
            'expire_time': time.time() + 30 * 24 * 3600
        }
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)
    
    def _load_cookies(self):
        """从文件加载cookies"""
        if os.path.exists(self.cookies_file):
            try:
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                    self.driver.get("https://creator.xiaohongshu.com")
                    for cookie in cookies:
                        self.driver.add_cookie(cookie)
            except:
                pass
    
    def _save_cookies(self):
        """保存cookies到文件"""
        cookies = self.driver.get_cookies()
        with open(self.cookies_file, 'w') as f:
            json.dump(cookies, f)
            
    def login(self, phone, country_code="+86"):
        """登录小红书"""
        # 如果token有效则直接返回
        if self.token:
            return
        
        # 尝试加载cookies进行登录
        self.driver.get("https://creator.xiaohongshu.com/login")
        self._load_cookies()
        self.driver.refresh()
        time.sleep(3)
        # 检查是否已经登录
        if self.driver.current_url != "https://creator.xiaohongshu.com/login":
            print("使用cookies登录成功")
            self.token = self._load_token()
            self._save_cookies()
            time.sleep(2)
            return
        else:
            # 清理无效的cookies
            self.driver.delete_all_cookies()
            print("无效的cookies，已清理")
            
        # 如果cookies登录失败，则进行手动登录
        self.driver.get("https://creator.xiaohongshu.com/login")

        # 等待登录页面加载完成
        time.sleep(5)
        # 点击国家区号输入框
        country_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='请选择选项']")))
        country_input.click()
        time.sleep(5)
        
        # 等待区号列表出现并点击+886
        # 等待区号列表出现并点击+86
        try:
            self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/div/div/div[1]/input").click()
            time.sleep(3)
            self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/div/div/div[1]/input").send_keys(country_code)
            time.sleep(3)
            # self.driver.find_element(By.XPATH, "/html/body/div[6]/div/div").click()
            # china_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'css-cqcgee')]//div[contains(text(), '+86')]")))
            time.sleep(5)
        except Exception as e:
            print("无法找到国家区号选项")
            print(e)
        
        # 定位手机号输入框
        phone_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='手机号']")))
        phone_input.clear()
        phone_input.send_keys(phone)
        
        # 点击发送验证码按钮
        try:
            send_code_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-uyobdj")))
            send_code_btn.click()
        except:
            # 尝试其他可能的选择器
            try:
                send_code_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1vfl29"))) 
                send_code_btn.click()
            except:
                try:
                    send_code_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'发送验证码')]")))
                    send_code_btn.click()
                except:
                    print("无法找到发送验证码按钮")
        is_send_code = False
        while not is_send_code:
            # 输入验证码
            verification_code = requests.get("http://xx.xx.xx.xx:5628/captcha").json()['code']
            if verification_code:
                is_send_code = True
            else:
                time.sleep(5)
                continue
        code_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='验证码']")))
        code_input.clear()
        code_input.send_keys(verification_code)
                
        # 点击登录按钮
        login_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".beer-login-btn")))
        login_button.click()
        
        # 等待登录成功,获取token
        time.sleep(3)
        # 保存cookies
        self._save_cookies()

        # 关闭浏览器
        # self.driver.quit()
            
        # print(f"获取到的token: {token}")
        
        # if token:
        #     self._save_token(token)
        #     self.token = token
        # else:
        #     print("未能获取到token")
        
    def post_article(self, title, content, images=None):
        """发布文章
        Args:
            title: 文章标题
            content: 文章内容
            images: 图片路径列表
        """
        # 如果token失效则重新登录
            
        # 设置token
        # self.driver.execute_script(f'localStorage.setItem("token", "{self.token}")')
        time.sleep(3)
        print("点击发布按钮")
        # 点击发布按钮
        publish_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.el-tooltip__trigger.el-tooltip__trigger")))
        publish_btn.click()

        # 如果是发布视频，则不操作这一步
        # 切换到上传图文
        time.sleep(3)
        tabs = self.driver.find_elements(By.CSS_SELECTOR, ".creator-tab")
        if len(tabs) > 1:
            tabs[1].click()
        time.sleep(3)
        # # 输入标题和内容
        # title_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".title-input")))
        # content_input = self.driver.find_element(By.CSS_SELECTOR, ".content-input")
        
        # title_input.send_keys(title)
        # content_input.send_keys(content)
        
        # 上传图片
        if images:
            upload_input = self.driver.find_element(By.CSS_SELECTOR,'input[type="file"]')
            # 将所有图片路径用\n连接成一个字符串一次性上传
            upload_input.send_keys('\n'.join(images))
            time.sleep(1)
        time.sleep(3)
        
        JS_ADD_TEXT_TO_INPUT = """
        var elm = arguments[0], txt = arguments[1];
        elm.value += txt;
        elm.dispatchEvent(new Event('change'));
        """
        
        title_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".d-text")))
        self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, title_input, title)
        # title_input.send_keys(title)
        
        # Start of Selection
        # Start of Selection
        print(content)
        JS_ADD_TEXT_TO_P = """
        var elm = arguments[0], txt = arguments[1];
        elm.textContent = txt;
        """
        content_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ql-editor")))
        p_element = content_input.find_element(By.CSS_SELECTOR, "p")
        print(p_element)
        self.driver.execute_script(JS_ADD_TEXT_TO_P, p_element, content)
        # content_input.send_keys(123)
        # 发布
        time.sleep(600)
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, ".el-button.publishBtn")
        submit_btn.click()
        
    def close(self):
        """关闭浏览器"""
        self.driver.quit()
        
def post_article():
    poster = XiaohongshuClient()
    phone = open('./docs/phone.txt').read()
    poster.login(phone)
    print("登录成功")
    print("开始发布文章")
    print(os.getcwd())
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    title = open(f'./xiaohongshu_drafts/小红书_推广文案_千战系列{today}.txt', 'r', encoding='utf-8').readline()
    article = line_process.get_article(f'./xiaohongshu_drafts/小红书_推广文案_千战系列{today}.txt')
    print(article)
    images = os.listdir('./pictures')
    images = map(lambda x: os.path.join(r"D:\Project\UUCrawl\Code\pictures", x), images)
    poster.post_article(title, article, images)
    poster.close()
