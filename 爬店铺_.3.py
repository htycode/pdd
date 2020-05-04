#coding:utf-8
import requests
import uiautomator2 as u2
import urllib.request
from time import sleep
import ast
'''
python -m weditor
'''
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.


def post_shop(shop_name):
    url = "http://112.124.127.143:8049/api/ShopCollect/PostShop"
    payload = '[{"shop_name":"%s","shop_id":""}]'%(shop_name)
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload.encode())
    print(payload+response.text)
    # print(response.text.encode('utf8'))

# 获取关键词
def get_Keyword():
    url = "http://112.124.127.143:8049/api/ShopCollect/GetKeyword"
    html = requests.get(url)
    print(html.text)
    html = ast.literal_eval(html.text)
    Keyword=html['data']["keyword"]
    id=html['data']["id"]
    return Keyword,id

# 上传更新关键词
def post_Keyword(id):
    url = "http://112.124.127.143:8049/api/ShopCollect/PutKeyword?keyword_id="+str(id)
    html = requests.post(url)
    print(html.text)

# sleep(99)


# 主函数>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
d = u2.connect("127.0.0.1:5555")
d.implicitly_wait(1)  # 隐式等待9s
# sleep(999)
id = 25
d.app_start("com.xunmeng.pinduoduo")
while True:
    for i in range(0,6):
        try:
            shop_name = d(resourceId="com.xunmeng.pinduoduo:id/lh")[i].get_text()
            if last_name == shop_name:
                pass
            else:
                post_shop(shop_name)
        except:  #触发: 找不到商铺名
            sleep(1)
            last_name = shop_name
            print("12412")
            if (d(text="已显示完所有搜索结果").exists()):
                post_Keyword(id)
                sleep(1)
                Keyword,id = get_Keyword()
                # 点击搜索框店铺名
                d(resourceId="com.xunmeng.pinduoduo:id/n").click()
                sleep(2)
                d(text="搜索你要的店铺").set_text(Keyword)
                sleep(2)
                d(text="搜索").click()
                sleep(5)

    d.swipe(521, 1833, 521, 218, 1)
    sleep(1)












