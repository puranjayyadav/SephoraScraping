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

            product_details = response.xpath("(//div[@class='css-foh208'])[2]")

            print(product_details)