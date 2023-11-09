import scrapy
from ..utils import URL
from ..items import SephoraItem
from scrapy import Selector

class SephoraProdsSpider(scrapy.Spider):
    name = "sephora_prods"
    allowed_domains = ["www.sephora.com"]
    start_urls = [URL]


    def parse(self, response):
        seph_item= SephoraItem()
        # Extract the product information as needed
        parent_divs = response.xpath("//div[starts-with(@id, 'brands-')]/div[@class='css-1s8tjtn eanm77i0']")

        for parent_div in parent_divs:
            brands = parent_div.xpath(".//li[@class='css-1evfm0']")
            for brand in brands:
                # Extract the brand information as needed
                seph_item['brand_name'] = brand.xpath(".//text()").get()  # Extract the text content within the div
                seph_item['brand_link'] = brand.xpath(".//@href").get()
                # Do something with the brand information, e.g., print it out
                yield response.follow("https://www.sephora.com" + seph_item['brand_link'],callback=self.parse_brand_page)


    def parse_brand_page(self, response):
            # Extract data from the brand page
            # We are sedning way too many requests to the server. We need to slow down the requests

            product_details = response.xpath("(//div[@class='css-foh208'])")
            for product in product_details:
                product_detailed_link= product.xpath(".//@href").get()
                yield response.follow("https://www.sephora.com" + product_detailed_link,callback=self.parse_product_page)
            #Use for debugging purposes
            #print(product_detailed_link)

    def parse_product_page(self,response):
        # Extract data from the product page
        product_likes = response.xpath("//span[@class='css-jk94q9']/text()").get()
        product_name = response.xpath("//a[contains(@class, 'css-11cofee') and contains(@class, 'eanm77i0')]/text()").get()
        product_category = response.xpath("//a[contains(@class, 'css-sdfa4l') and contains(@class, 'eanm77i0')").get()
        product_size = response.xpath("//span[@class='css-7b7t20']/descendant-or-self::text()").get().strip()
        product_price = response.xpath("//span[@class='css-jk94q9']/text()").get()
        product_reviewCount = response.xpath("//span[@class='css-jk94q9']/text()").get()
        product_rating = response.xpath("//span[@class='css-jk94q9']/text()").get()
        product_brand= response.xpath("//h1/text()").get()
        print(product_likes)
