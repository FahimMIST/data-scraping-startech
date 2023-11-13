import scrapy

class startechscraper(scrapy.Spider):
    name = 'startech'

    def start_requests(self):
        urls = ['https://www.startech.com.bd'] 
        for url in urls:
            yield scrapy.Request(url = url, callback=self.parse_url)


    def parse_url(self, response):
        links = response.css('a.nav-link::attr(href)').extract()
        
        for url in links:
            yield response.follow(url =url, callback = self.parse_2)

    def parse_2(self, response):
        links2 = response.css('ul.pagination>li>a::attr(href)').extract()
        
        for url2 in links2:
            yield response.follow(url =url2, callback = self.parse_3)

    def parse_3(self, response):
        links3 = response.css('div.p-item-img>a::attr(href)').extract()
        
        for url3 in links3:
            yield response.follow(url =url3, callback = self.parse_content)
    
    
    def parse_content(self, response):
        for products in response.css('div.pd-summary'):
            yield {
                'name' : products.css('h1::text').get(),
                'Current_Price': products.css('table.product-info-table>tr>td.product-info-data.product-price::text').get().replace('\u09f3',''),
                'Regular_Price': products.css('table.product-info-table>tr>td.product-info-data.product-regular-price::text').get().replace('\u09f3',''),
                'Product_Status': products.css('table.product-info-table>tr>td.product-info-data.product-status::text').get(),
                'Product_code': products.css('table.product-info-table>tr>td.product-info-data.product-code::text').get(),
                'Brand': products.css('table.product-info-table>tr>td.product-info-data.product-brand::text').get(),
                'Short Description': products.css('div.short-description>ul>li::text').extract()
                    }
