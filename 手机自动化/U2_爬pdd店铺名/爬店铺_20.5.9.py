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
            d(text="首页").click(timeout=5)
            # 点击搜索框
            d.click(522, 134)
            sleep(1)
            d(text="搜索店铺").click(timeout=4)
            sleep(1)
            d(text="搜索你要的店铺").set_text(text)
            sleep(2)
            d(text="搜索").click()
            sleep(2)
            bj = False
        except:
            print('重启拼多多')
            pass

# 上传店铺信息
def post_shop(shop_name,shop_sale):
    url = "http://112.124.127.143:8049/api/ShopCollect/PostShop"
    payload = '[{"shop_name":"%s","shop_id":"","sales":"%s"}]'%(shop_name,shop_sale)
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data = payload.encode())
    html = json.loads(response.text)
    # print(html['msg']+":"+shop_name+"/"+shop_sale)
    d.toast.show(html['msg']+":"+shop_name+"/"+shop_sale,11)

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

# 手机上获取商家名称/销量
def get_shop_infos():
    arr=[]
    for i in range(1, 6):
        try:
            shop_names = d.xpath('//*[@resource-id="com.xunmeng.pinduoduo:id/hj"]/android.view.View[{}]/android.widget.TextView[1]'.format(i))
            shop_sales = d.xpath('//*[@resource-id="com.xunmeng.pinduoduo:id/hj"]/android.view.View[{}]/android.widget.TextView[2]'.format(i))
            name = shop_names.get_text()
            sale = shop_sales.get_text()
            if name != "" and sale != "":
                # print(name, sale)
                dp_dic = {"name":name,"sale":sale}
                arr.append(dp_dic)
        except:
            pass
    return arr
# sleep(99)


# 主函数>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# d = u2.connect("0123456789ABCDEF")
d = u2.connect("http://0.0.0.0")
# d = u2.connect("127.0.0.1:5555")
d.implicitly_wait(3)  # 隐式等待9s

# id=
# Keyword,id = get_Keyword()
# d.app_start("com.xunmeng.pinduoduo")
# sleep(60)
# 循环>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
while True:
    # 获取商铺信息
    shop_infos = get_shop_infos()
    for shop_info in shop_infos:
        # 上传商铺信息
        post_shop(shop_info["name"],shop_info["sale"])
    # 滑动
    d.swipe(521, 1900, 521, 50, 1.5)
    sleep(random.randint(1, 5))
    if (d(text="已显示完所有搜索结果").exists()):
        post_Keyword(id);sleep(1)
        Keyword, id = get_Keyword()
        # 延时一段时间
        d.app_stop("com.xunmeng.pinduoduo")
        sleep(random.randint(60, 70))
        # 重启拼多多
        restart_pdd_search(Keyword)


