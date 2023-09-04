import requests
from lxml import etree
import random
import time
import json



from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)



def get_html(url):
    #构建代理池
    ua_list = [
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) '
        'AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    ]

    headers = {
        "User-Agent": random.choice(ua_list)
    }
    cookies = {
        'cookie':'Cc2838679FS=5bzGREbqAMY_3YFzJmAqqGnYl610jl66AgWpdEOE7YNREUWAO2jmZoOpVSszKyY51FxahQnCaZBZB0Yi7HnAFLa;'
                 ' _lxsdk_cuid=180941706f9c8-07f61ddf955f4-50684054-144000-180941706fac8; uuid_n_v=v1; '
                 'uuid=E1A5BA00051911EEB5DB33031B0079F35D45D917A0804399B2B474D0FE9D8F5B;'
                 ' _lxsdk=E1A5BA00051911EEB5DB33031B0079F35D45D917A0804399B2B474D0FE9D8F5B;'
                 ' _csrf=acbcb67b270ca382f6c942e039cc7501496bfbba1f47917371cbd1a20c653166; '
                 'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1686131922,1686191225,1686192243;'
                 ' Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1686192243; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=250912697.1652272938794.1686192172103.1686192243412.109; _lxsdk_s=18898d439d1-986-ec9-070%7C%7C23'
    }
    try:
        resp = requests.get(url,headers=headers,cookies=cookies)
        if '猫眼验证中心' in resp.text:
            print("请重新获取当前时效下的Cookie，修改代码中的Cookie值后再尝试运行！")
        else:
            if resp.status_code == 200:
                return resp.text
    except requests.ConnectionError as e:
        print('Error', e.args)

def get_paim():
    chart = {}
    arry = []
    url = 'https://piaofang.maoyan.com/box-office?ver=normal'
    html = get_html(url)
    html = etree.HTML(html)
    trs = html.xpath('//*[@id="app"]/div/div[2]/div/div[2]/table/tbody/tr')
    # print(len(trs))
    ths = html.xpath('//*[@id="app"]/div/div[2]/div/div[2]/table/thead/tr/th')
    d=[]
    for th in ths:
        title = th.xpath('text()')[0]
        d.append(title)
    print(d)

    for i in range(len(trs)):
        dict = {}
        tr = trs[i]
        name = tr.xpath('./td[1]/div/p[1]/text()')[0]
        num = tr.xpath('./td[2]/div/text()')[0]
        zonghebi = tr.xpath('./td[3]/div/text()')[0]
        paipbi = tr.xpath('./td[4]/div/text()')[0]
        paizuobi = tr.xpath('./td[5]/div/text()')[0]
        sump = tr.xpath('./td[1]/div/p[2]/span')
        dict['name'] = name
        dict['num'] = num
        dict['zonghebi'] = zonghebi
        dict['paipbi'] = paipbi
        dict['paizuobi'] = paizuobi
        arry.append(dict)
    # print(arry)
    chart['chartData'] = arry
    chart['title'] = d
    # print(chart)
    return chart

        # print(name,num,sumbi,paipbi,paizuobi)

def bingzhuan():
    array = []
    chart = {}
    url = 'https://piaofang.maoyan.com/session'
    html = get_html(url)
    html = etree.HTML(html)
    trs = html.xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div[2]/div/table/tbody/tr')
    for i in range(len(trs)):
        dict = {}
        tr = trs[i]
        name = tr.xpath('./td[1]/div/div/span/text()')[0]
        sessionbi = tr.xpath('./td[2]/div/text()')[0]
        session = tr.xpath('./td[3]/div/text()')[0]
        # print(name,sessionbi,session)
        dict['name'] = name
        # dict['sessionbi'] = sessionbi
        dict['value'] = session
        array.append(dict)
    chart['chartData'] = array
    print(chart)
    return chart

def zong_pm():
    url = 'https://piaofang.maoyan.com/mdb/rank'
    html = get_html(url)
    html = etree.HTML(html)
    fin_data = []
    pf_data = {}
    # ths = html.xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div/table/thead/tr/th')
    # for i in ths:
    #     th = i.xpath('./div/span/text()')
    #     print(th)
    trs = html.xpath('//*[@id="app"]/div/div[2]/div/div[2]/div[2]/div/table/tbody/tr')
    for i in range(len(trs)):
        data = {}
        name = trs[i].xpath('./td[1]/div/div/div[1]/span/text()')[0]
        pf = trs[i].xpath('./td[2]/div/text()')[0]
        time = trs[i].xpath('./td[1]/div/div/div[2]/text()')[0]
        price = trs[i].xpath('./td[3]/div/text()')[0]
        people = trs[i].xpath('./td[4]/div/text()')[0]
        data['name'] = name
        data['pf'] = pf
        data['time'] = time
        data['price'] = price
        data['people'] = people
        fin_data.append(data)
    pf_data['pfdata'] = fin_data
    print(pf_data)
    return pf_data



@app.route('/one/data')#这个是对函数的注解
def onedata():
    return get_paim()

@app.route('/two/data')#这个是对函数的注解
def twodata():
    return bingzhuan()
@app.route('/pf/data')#这个是对函数的注解
def pfdata():
    return zong_pm()

@app.route('/map/data')#这个是对函数的注解
def mapdata():
    with open("D:\html\\vue\serve\mock\china.json", encoding="utf-8") as file:
        file_json = json.loads(file.readline())
    return file_json



if __name__ == '__main__':
    # zong_pm()
    app.run(port='8888')
    # get_paim()
#   zong_pm()
    # while(True):
    #     get_paim()
    #     time.sleep(1.5)

    # bingzhuan()
