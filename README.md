# YahooMall
CrawelYahooMallData_byScrapy

1. 在YahooMall/yahoo_spider/yahoo_spider/路徑下的四個.py檔是設定檔
2. 爬蟲主程式為yahoo_spider/yahoo_spider/spiders/mall.py
3. 載好所有套包程式後在cmd下「scrapy crawl mall -o mall.csv」指令，就可以於本機端產生相對應的mall.csv檔
4. BestSellItemAnalysis.py檔則是用來分析mall.csv檔中的主要字詞，最後會輸出BestSellItem.csv檔在對應路徑中
5. 接著再用BestSellItem.csv做一些人工判別分析，找出可能的熱銷商品組合

# query需求
在做爬蟲時，有同步將資料存到朋友的mandoDB下，所以如果需要query資料時，可以用以下指令找想要的資料
from pymongo import MongoClient
from bson.objectid import ObjectId #這東西再透過ObjectID去尋找的時候會用到

/# connection /

conn = MongoClient("mongodb://sklee:295122@shiaukuan.asuscomm.com:27017") 

db = conn['yahoo']

collection = db['mall']

/# test if connection success /

for i in collection.find({'enqueue_date':'2018-09-02'}):
    print (i)
    break
