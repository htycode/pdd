#coding:utf-8
import random
import requests,json
import uiautomator2 as u2
from time import sleep
import ast
'''
python -m weditor
两次关键词爬取间隔时间60-70s
添加重启: 一个关键词爬完后重启pdd, 点击搜索框搜索并爬取下一个关键词
'''
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.

# 重启拼多多_搜索相关店铺
def restart_pdd_search(text):
    bj=True
    while bj:
        try:
            d.app_stop("com.xunmeng.pinduoduo")
            sleep(2)
            d.app_start("com.xunmeng.pinduoduo")
            sleep(5)
            # 点击搜索框
            d(resourceId="com.xunmeng.pinduoduo:id/ad4").click(timeout=5)
            sleep(1)
            d(text="搜索店铺").click(timeout=2)
            sleep(1)
            d(text="搜索你要的店铺").set_text(text)
            sleep(2)
            d(text="搜索").click()
            bj = False
        except:
            print('重启')
            pass

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
# d = u2.connect("http://0.0.0.0")
d = u2.connect("127.0.0.1:5555")
d.implicitly_wait(1)  # 隐式等待9s

Keyword,id = get_Keyword()
d.app_start("com.xunmeng.pinduoduo")
sleep(60)
# 循环>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
while True:

    # 获取商铺名节点
    shop_names =  get_shop_names()
    for shop_name in shop_names:
        # 上传商铺名
        post_shop(shop_name)
    # 滑动
    d.swipe(521, 1900, 521, 50, 0.5);sleep(0.5)
    if (d(text="已显示完所有搜索结果").exists()):
        post_Keyword(id)
        sleep(1)
        Keyword,id = get_Keyword()
        # 延时一段时间
        d.app_stop("com.xunmeng.pinduoduo")
        sleep(random.randint(60, 70))
        # 重启拼多多
        restart_pdd_search(Keyword)
        sleep(2)















