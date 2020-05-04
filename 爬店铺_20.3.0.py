#coding:utf-8
import requests,json
import uiautomator2 as u2
from time import sleep
import ast
'''
python -m weditor
一个关键词爬完后不重启, 点击搜索框搜索并爬取下一个关键词
(运行大约一天会触发安全监测(不过检测无法搜索关键词):滑块/按要求找图)
'''
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.

# 上传店铺名称
def post_shop(shop_name):
    url = "http://112.124.127.143:8049/api/ShopCollect/PostShop"
    payload = '[{"shop_name":"%s","shop_id":""}]'%(shop_name)
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload.encode())
    html = json.loads(response.text)
    print(payload+html['msg'])

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

# 手机上获取商家名称
def get_shop_names():
    arr=[]
    shop_names = d(resourceId="com.xunmeng.pinduoduo:id/lh")
    for i in shop_names:
        arr.append(i.get_text())
    return arr
# sleep(99)


# 主函数>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# d = u2.connect("0123456789ABCDEF")
# d = u2.connect("http://127.0.0.0")
d = u2.connect("127.0.0.1:5555")
d.implicitly_wait(1)  # 隐式等待9s

# sleep(999)
Keyword,id = get_Keyword()
d.app_start("com.xunmeng.pinduoduo")
sleep(2)
# 循环>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
while True:
    shop_names =  get_shop_names()
    for shop_name in shop_names:
        post_shop(shop_name)

    sleep(1)
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












