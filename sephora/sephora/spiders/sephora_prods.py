import scrapy
from ..utils import URL
from ..items import SephoraItem
import pandas as pd
from scrapy import Selector

class SephoraProdsSpider(scrapy.Spider):
    name = "sephora_prods"
    allowed_domains = ["www.sephora.com"]
    start_urls = [URL]
    data_list=[]
    FINAL_LIST=[]

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
                # Append the data to the data_list
                self.data_list.append(product_detailed_link)
            # df = pd.DataFrame(self.data_list)
            # Save the DataFrame to an Excel file
            # df.to_excel('sephora_data.xlsx', index=False)
            # yield response.follow("https://www.sephora.com" + product_detailed_link,callback=self.parse_product_page)
            #Use for debugging purposes
            # print(product_detailed_link)

# Read the excel file to access individual links one by one
    def start_requests(self):
        # Read links from Excel file (modify the file path)
        df = pd.read_excel('sephora_data.xlsx', header=None, names=['links'])

        for index, row in df.iterrows():
            yield scrapy.Request(url="https://www.sephora.com" + str(row['links']), callback=self.parse_product_page)

    def parse_product_page(self,response):
        seph_item= SephoraItem()
        # Extract data from the product page
        seph_item['product_likes'] = response.xpath("//span[@class='css-jk94q9']/text()").get()
        seph_item['product_name'] = response.xpath("//a[contains(@class, 'css-11cofee') and contains(@class, 'eanm77i0')]/text()").get()
        # seph_item['product_category'] = response.xpath("//a[contains(@class, 'css-sdfa4l') and contains(@class, 'eanm77i0')").get()
        # seph_item['product_size'] = response.xpath("//span[@class='css-7b7t20']/descendant-or-self::text()").get().strip()
        seph_item['product_price'] = response.xpath("//b[@class='css-0']/text()").get()
        seph_item['product_reviewCount'] = response.xpath("//span[@class='css-1j53ife']/text()").get()
        # seph_item['product_rating'] = response.xpath("//div[@class='css-12ke8jn eanm77i0']//span[@class='css-1ac1x0l eanm77i0']").get()
        seph_item['product_brand']= response.xpath("//h1/text()").get()

        # Append the data to the data_list
        self.FINAL_LIST.append({
            'product_likes': seph_item['product_likes'],
            'product_name': seph_item['product_name'],
            # 'product_category': seph_item['product_category'],
            # 'product_size': seph_item['product_size'],
            'product_price': seph_item['product_price'],
            'product_reviewCount': seph_item['product_reviewCount'],
            # 'product_rating': seph_item['product_rating'],
            'product_brand': seph_item['product_brand']
        })
        df = pd.DataFrame(self.FINAL_LIST)
        df.to_excel('sephora_data_FINAL.xlsx', index=False)

        # yield seph_item
    # def closed(self, reason):
    #     # Create a DataFrame from the data_list
    #     df = pd.DataFrame(self.data_list)
    #
    #     # Save the DataFrame to an Excel file
    #     df.to_excel('sephora_data.xlsx', index=False)