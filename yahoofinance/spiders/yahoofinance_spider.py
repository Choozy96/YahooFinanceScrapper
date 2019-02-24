import scrapy
import time
#Scraps data from yahoo's finance historical data page. Parses the data into a csv file.

class YahooFinanceSpider(scrapy.Spider):
    name = "yahoofinance"
    DOWNLOAD_DELAY = 1

    def start_requests(self):
        input_ticker = input("Insert tickers to scrape, include '.SI' for SG tickers, ',' for ticker seperators")
        ticker_list = input_ticker.split(',')
        urls = []
        period2= int(time.time())
        for ticker in ticker_list:
            urls.append("https://sg.finance.yahoo.com/quote/%s/history?period1=0&period2=%s0&interval=1d&filter=history&frequency=1d" %(ticker,period2))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ticker = response.url.split('/')[4]
        filename = '%s.csv' % ticker
        #scraps to csv file in repo root
        table = response.xpath('//*[@data-test="historical-prices"]')
        rows = table.xpath('//tr')
        with open(filename,'w') as f:
            table_headers = rows[0].xpath('th//text()').extract()
            for header in table_headers:
                f.write(header)
                f.write(',')
            f.write('\n')
            for row in rows[1:-1]:
                hist_data_list = row.xpath('td//text()').extract()
                for data in hist_data_list:
                    while data.find(',')!=-1:
                        data = data.replace(',','')
                    f.write(data)
                    f.write(',')
                f.write('\n')
        self.log('saved file %s' % filename)