# -*- coding: utf-8 -*-
# @Author : Ezreal
# @File : main.py
# @Project: OnlineCourseKiller
# @CreateTime : 2025/6/13 下午22:51:12
# @Version：1.0
import time
import json
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def login(driver):
    driver.get("https://lms.cctv.cn/auth/loginIndex.do")
    # cookies = driver.get_cookies()
    driver.implicitly_wait(10)

    login_name = input("请输入账号：")
    driver.find_element(by=By.NAME, value="loginName").send_keys(login_name)


    password = input("请输入密码：")
    driver.find_element(by=By.NAME, value="password").send_keys(password)

    captcha_button = driver.find_element(by=By.ID, value="yzmBtn")
    captcha_button.click()

    driver.implicitly_wait(10)

    # 创建动作链对象
    actions = ActionChains(driver)

    # 点击坐标 (0, 0)，也就是页面左上角
    actions.move_by_offset(0, 0).click().perform()

    # 手动输入验证码
    captcha = input("请输入验证码: ")
    captcha_input = driver.find_element(by=By.ID, value="msgCode")
    captcha_input.send_keys(captcha)

    login_button = driver.find_element(by=By.ID, value="loginButton")
    login_button.click()

    # message = driver.find_element(by=By.ID, value="message")
    # text = message.text

    # driver.implicitly_wait(10)
    print("login successfully!")

    time.sleep(5)

    # # 保存 cookies 到文件
    # cookies = driver.get_cookies()
    # with open("cookies.json", "w") as f:
    #     json.dump(cookies, f)

def select_courses(driver):
    # # 先访问网站以设置 domain
    # driver.get("https://lms.cctv.cn/auth/loginIndex.do")
    #
    # # 从文件加载 cookies
    # with open("cookies.json", "r") as f:
    #     cookies = json.load(f)
    #
    # # 添加 cookies
    # for cookie in cookies:
    #     driver.add_cookie(cookie)
    #
    # # 刷新页面使 cookies 生效
    # driver.refresh()
    #
    # driver.implicitly_wait(10)

    # close_button = driver.find_element(by=By.ID, value="fancybox-close")
    # if (close_button):
    #     close_button.click()

    # courses_list = driver.find_elements(by=By.ID, value="all_online_course")
    # courses_list.click()

    driver.get("https://lms.cctv.cn/curriculum/index.do")
    driver.implicitly_wait(10)

    courses_list_pages = driver.find_elements(by=By.CLASS_NAME, value="ui-list-page")
    page = []
    for course_page in courses_list_pages:
        page.append(int(course_page.text))
    # print(max(page))

    for i in range(1, max(page) - 37):
        print("正在选第", i, "页的课")
        courses_list = driver.find_elements(by=By.CLASS_NAME, value="over-text")
        for course in courses_list:
            # print(course.text)
            course.click()
            driver.implicitly_wait(10)
            try:
                driver.find_element(by=By.ID, value="bt").click()
                print("选课成功!")
            except:
                print("这门课选过了,已跳过！")
                pass
            driver.back()
            time.sleep(5)
        next_page = driver.find_element(by=By.CLASS_NAME, value="ui-icon-next")
        next_page.click()
        time.sleep(5)

def auto_complete_courses(driver):
    driver.get("https://lms.cctv.cn/learning/courseIndex.do")

    while True:
        driver.implicitly_wait(10)
        try:
            driver.find_element(by=By.CLASS_NAME, value="p1").click()
            while True:
                try:
                    driver.find_element(by=By.LINK_TEXT, value="继续学习").click()
                    time.sleep(20)
                    driver.find_element(by=By.CLASS_NAME, value="layui-layer-close1").click()
                    driver.refresh()
                except:
                    try:
                        driver.find_element(by=By.LINK_TEXT, value="开始学习").click()
                        time.sleep(20)
                        driver.find_element(by=By.CLASS_NAME, value="layui-layer-close1").click()
                    except:
                        driver.back()
                        break
        except:
            print("在读课程已全部完成！")
            break


if __name__ == '__main__':
    # url = 'https://lms.cctv.cn/auth/loginIndex.do'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)  # 防止浏览器自动关闭
    options.headless = True
    driver = webdriver.Chrome(options=options)

    login(driver)
    # select_courses(driver)
    auto_complete_courses(driver)
