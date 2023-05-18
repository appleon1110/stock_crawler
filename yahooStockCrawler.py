import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import chardet
import matplotlib.pyplot as plt
import requests
import datetime
import chardet



def catch_stock(url,fileName):
    CsvFilePath="./file/"+fileName+".csv"
    TxtFilePath="./file/"+"test1.txt"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    table_store = soup.find("script", text=lambda x: x and "TableStore" in x).text



    f = open(TxtFilePath, 'w', encoding='utf-8')
    f.writelines(table_store)
    f.close()

    with open(TxtFilePath,encoding='utf-8') as f:
        data = f.read()


    # 使用 splitlines() 方法將多行字串轉換成一個行的列表
    lines = data.splitlines()
    table_store_line = [line for line in lines if "TableStore" in line][0]
    # print(table_store_line)

    arr = "".join(table_store_line)
    arr = table_store_line.split('"list":')

    # 切出"rankTime": 
    rankTime = arr[1].split('rankTime')

    symbol = arr[1].split(',"listMeta')
    symbol=symbol[0]
    outputData = rankTime[1].replace(':', '').replace(',', '').replace('"', '')

    # 將JSON格式的字串轉換為Python的字典物件
    data = json.loads(symbol)


    
    # 創建CSV檔案
    with open(CsvFilePath, 'a', newline='',encoding="UTF-8") as csvfile:
        writer = csv.writer(csvfile)
        # if os.path.isfile(CsvFilePath):
        #     print("有檔案")
        # else:
        #     print("沒有檔案")
        writer.writerow(['股票日期','股名','排名', '股價', '漲跌','買進張數','賣出張數','買超張數','成交張數','外資持股張數','外資持股比率','股票代號'])

        for item in data:
            if isinstance(item, dict):
                writer.writerow([outputData,item['name'], item['rank'], item['previousClose'],item['previousChange'],item['boughtK'],item['soldK'],item['overboughtK'],item['volK'],item['holdK'],item['holdPercent'],item['rowId'] ])
            elif isinstance(item, list):
                writer.writerow([outputData,item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10]])


def plot_csv_file(fileName):
    # 設定中文字體為 Microsoft JhengHei，或其他中文字體
    plt.rcParams['font.family'] = ['Microsoft JhengHei']
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    

    # 讀取 CSV 檔案
    with open("./file/"+fileName+".csv", 'rb') as f:
        result = chardet.detect(f.read())
        
    encoding = result['encoding']

    if encoding == 'utf-8':
        print("編碼為:"+encoding)
        df = pd.read_csv("./file/"+fileName+".csv", encoding=encoding)
    else:
        df = pd.read_csv("./file/"+fileName+".csv", encoding='Big5')
        print("編碼為:"+"Big5")


    # 取得前 50 筆資料
    df_subset = df.iloc[-100:]
    print(df_subset)
    # 設定圖表大小
    fig, axs = plt.subplots(1, 1, figsize=(20,30))

    # 隱藏座標軸
    axs.axis('off')

    # 自動調整圖表大小
    # axs.axis('tight')

    # 設定字體大小為 100
    plt.rcParams['font.size'] = 100

    # 設定表格內容及標題，並設定字體大小
    table = axs.table(cellText=df_subset.values, colLabels=df_subset.columns, bbox = [0.05, 0.05, 0.95, 0.9])
    table.auto_set_font_size(False)  # 取消自動調整字體大小
    table.set_fontsize(10)  # 設定表格字體大小
    table.auto_set_column_width([0,1])

    # 設定標題字體大小
    axs.set_title(fileName, fontsize=20)

    # 儲存圖片
    plt.savefig("./file/jpg/"+today+fileName+'.JPEG')

    # 關閉當前圖表
    plt.close()


def post_to_linenotify(JPGfileName):

    url = "https://notify-api.line.me/api/notify"
    headers = {
    "Authorization": "Bearer a123456789你的金鑰",
}

    image_path = "./file/jpg/"+today+JPGfileName+".JPEG"

    files = {
        "imageFile": open(image_path, "rb"),
    }

    data = {
        "message": "您的貼心小幫手幫你製作"+JPGfileName+"圖",
    }
    try:
        response = requests.post(url, headers=headers, data=data, files=files)
        response.raise_for_status()
        print(response.status_code)
    except Exception as e:
        print("Error:", e)
        print("Response Text:", response.text)  # 顯示伺服器回傳的錯誤訊息

    else:
        print("檔案存在：", image_path)


today = datetime.date.today()
today=today.strftime("%Y%m%d")

url1="https://tw.stock.yahoo.com/rank/foreign-investor-buy/"
csvName1="外資當日買超排行"
url2="https://tw.stock.yahoo.com/rank/foreign-investor-buy?exchange=TAI"
csvName2="上市外資當日買超排行"
url3="https://tw.stock.yahoo.com/rank/foreign-investor-buy?exchange=TWO"
csvName3="上櫃外資當日買超排行"
url4="https://tw.stock.yahoo.com/rank/foreign-investor-sell"
csvName4="外資當日賣超排行"
url5="https://tw.stock.yahoo.com/rank/foreign-investor-sell?exchange=TAI"
csvName5="上市外資當日賣超排行"
url6="https://tw.stock.yahoo.com/rank/foreign-investor-sell?exchange=TWO"
csvName6="上櫃外資當日賣超排行"
# 抓取指定網址，並儲存成CSV
catch_stock(url1,csvName1)
catch_stock(url2,csvName2)
catch_stock(url3,csvName3)
catch_stock(url4,csvName4)
catch_stock(url5,csvName5)
catch_stock(url6,csvName6)

# 依照指定檔名csv 匯出成圖檔
plot_csv_file(csvName1)
plot_csv_file(csvName4)

post_to_linenotify(csvName1)
post_to_linenotify(csvName4)