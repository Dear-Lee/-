from bs4 import BeautifulSoup
import requests
import csv


def getlocation(name):  # 调用百度API查询位置，输入地名，获取该地名对应的经纬度
    bdurl = 'http://api.map.baidu.com/geocoder/v2/?address='
    output = 'json'
    ak = 'Iz0njXfVvxFjT8bBWG7rB92qIsGwkri6'  # 百度地图API申请的密匙
    callback = 'showLocation'
    uri = bdurl + name + '&output=t' + output + '&ak=' + ak + '&callback=' + callback
    res = requests.get(uri)
    s = BeautifulSoup(res.text)
    lng = s.find('lng')
    lat = s.find('lat')
    if lng:
        return lng.get_text() + ',' + lat.get_text()


url = 'http://esf.cq.fang.com/house/i3'
heade = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}  # 请求头，模拟浏览器登陆
page = list(range(1, 101, 1))  # 代表从1到100，间隔1(不包含101)
p = []
hi = []
Adr = []
for i in page:  # 循环访问房天下的网页
    response = requests.get(url + str(i))#获取list中的网页
    soup = BeautifulSoup(response.text)#使用beautifulsoup库获取网页里的信息
    # 提取价格
    prices = soup.find_all('span', class_='price')
    for price in prices:
        p.append(price.get_text())
        # print(price.get_text())
    # 提取房源信息
    hs = soup.find_all('p', class_='title')
    for h in hs:
        hi.append(h.get_text())
        # print(h.get_text())
    # 提取房源详细地址
    Adress = soup.find_all('span', class_='iconAdress ml10 gray9')
    for ad in Adress:
        Adr.append("重庆" + ad.get_text())#不同地方有可能有相同的地名，加上“重庆”限定了查找区域
    # print(ad.get_text())
    print(i)


n = 0
num = len(p)
file = open('data.csv', 'w', newline='', encoding='utf-8')
headers = ['name', 'Adress', 'loc', 'price']
writers = csv.DictWriter(file, headers)
writers.writeheader()
while n < num:  # 循环将信息存放进列表
    hi0 = hi[n].split('|')
    name = hi0[0]
    ad0 = Adr[n].split('|')
    Adress = ad0[0]
    loc = getlocation(Adress)
    price = p[n]
    Ad = Adr[n]
    house = {'name': name, 'Adress': Ad, 'loc': loc, 'price': price}
    # 将房子的信息放进一个dict中
    writers.writerow(house)  # 将dict写入到csv文件中
    n += 1
    #print(n)
file.close()

reader = csv.reader(open('data.csv', encoding='utf-8'))
for row in reader:
    loc = row[2]
    sloc = loc.split(',')
    lng = ''
    lat = ''
    if len(sloc) == 2:
        lng = sloc[0]
        lat = sloc[1]
        count = '50'
        out = '{\"lng\":' + lng + ',\"lat\":' + lat + ',\"count\":' + count + '},'
        print(out)
