# YahooMall
CrawelYahooMallData_byScrapy

1. 在YahooMall/yahoo_spider/yahoo_spider/路徑下的四個.py檔是設定檔
2. 爬蟲主程式為yahoo_spider/yahoo_spider/spiders/mall.py
3. 載好所有套包程式後在cmd下「scrapy crawl mall -o mall.csv」指令，就可以於本機端產生相對應的mall.csv檔
4. yahoo_spider/yahoo_spider/spiders/BestSellItemAnalysis.py檔則是用來分析mall.csv檔中的主要字詞，最後會輸出BestSellItem.csv檔在對應路徑中
