from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import requests
import urllib
import time
import cv2
import random
from urllib.parse import unquote
import json
option = webdriver.ChromeOptions()
# option.add_experimental_option ( "detach", True)

option.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(executable_path=r'C:\Users\Arthur Wang\Desktop\douyin\simulate\chromedriver.exe', options=option)
bg_img = ''
bg_img_local = 'pics/bg.jpeg'
tp_img = ''
tp_img_local = 'pics/fg.png'
out_img_local = 'pics/test.jpeg'


# 存到本地
def saveToLocal(link, dest):
    urllib.request.urlretrieve(link, dest)

def findx(bg, tp, out):
    bg_img = cv2.imread(bg) # 背景图片
    tp_img = cv2.imread(tp) # 缺口图片
    
    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)
    
    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    
    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 寻找最优匹配
    
    tl = max_loc
    # 绘制方框
    th, tw = tp_pic.shape[:2] 
    tl = max_loc # 左上角点的坐标
    br = (tl[0]+tw,tl[1]+th) # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2) # 绘制矩形
    cv2.imwrite(out, bg_img) # 保存在本地
    
    # 返回缺口的X坐标
    return tl[0] 

def drag_and_drop(browser, offset):
    knob = browser.find_element_by_class_name("gt_slider_knob")
    ActionChains(browser).drag_and_drop_by_offset(knob, offset, 0).perform()

def get_track(distance, t):
    track = []
    current = 0
    mid = distance * t / (t+1)
    # mid = distance/2
    v= 0
    while current<distance:
        if current<mid:
            a=1
        else:
            a=-1
        v0 = v
        v = v0 + a*t
        move = v0*t + a*t*t/2
        print('a = ', a, ', dis= ', move)
        if current + move <distance:
            track.append(round(move))
        else:
            track.append(round(distance - current))
        current += move
    return track
# time.sleep(200)
# distance = findx(bg_img_local, tp_img_local, out_img_local)

# time.sleep(10)
# input("running")

# main start
#========================  00  ========================
# driver.get('https://www.douyin.com/user/MS4wLjABAAAAKzY4DCB_Qgl0ygwvSXe_jwFsUQw6JN9g4YU7B8ksRspsd5Teb8GczwmMBZSnFjET')
driver.get('https://v.douyin.com/St1pdRp/')
title = driver.title
if title == '验证码中间页':
    assert title == '验证码中间页'
    time.sleep(2)
    pic1 = driver.find_element(by=By.ID, value='captcha-verify-image')
    bg_img = pic1.get_attribute('src')
    pic2 = driver.find_element(by=By.CSS_SELECTOR, value='img.captcha_verify_img_slide.react-draggable.sc-VigVT.ggNWOG')
    tp_img = pic2.get_attribute('src')
    #========================  01  ========================
    # time.sleep(1)
    print(bg_img)
    print(tp_img)
    saveToLocal(bg_img, bg_img_local)
    saveToLocal(tp_img, tp_img_local)
    #========================  02  move mouse========================
    # time.sleep(1)
    distance = findx(bg_img_local, tp_img_local, out_img_local)
    print("original move x: ", distance)
    print("actual move x: ", distance*.62)
    # time.sleep(1)

    ActionChains(driver).move_to_element(pic1).perform()
    time.sleep(0.25)
    ActionChains(driver).move_to_element(pic2).perform()
    time.sleep(0.25)
    ActionChains(driver).click_and_hold(on_element=pic2).perform()
    if distance<200:
        time.sleep(1)
    time1 = [3,4,5,6,2.1,2.7,2.8,2.9,3.0,3.1,3.2,3.4,4,5,6]
    t = random.choice(time1)
    track = get_track(distance*0.62, t)
    for x in track:
        # ActionChains(driver).move_by_offset(x, 0).perform()
        ActionChains(driver, duration=10).move_by_offset(x, 0).perform()
    ActionChains(driver).pause(0.7).release(on_element=pic2).perform()
    print("move over")

    time.sleep(6)

neirong = driver.find_element(By.ID, 'RENDER_DATA')
# print(neirong.get_attribute("innerHTML"))
data = unquote(neirong.get_attribute("textContent"),'utf8')
jsdata = json.loads(data)
user = jsdata['40']['user']['user']
print(user['uid'])
print(user['secUid'])
print(user['shortId'])
print(user['nickname'])
print(user['desc'])
print(user['gender'])
print(user['followerCount'])
print(user['totalFavorited'])
print(user['awemeCount'])
print(user['ipLocation'])
# attrs=[]
# for attr in neirong.get_property('attributes'):
#     attrs.append([attr['name'], attr['value']])
# print(attrs)

time.sleep(10)