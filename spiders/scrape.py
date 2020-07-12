import scrapy

import os.path
import requests


class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ["https://www.us-cert.gov/ncas/analysis-reports"]
    base_url = "https://www.us-cert.gov"
    page_url = "https://www.us-cert.gov/ncas/analysis-reports"

    def parse(self, response):
        print(response.url)
        # debugging

        selectors = response.xpath("//a")
        # Get all the <a>'s and loop through them
        for selector in selectors:
            link = selector.xpath("@href").extract_first()
            text = selector.xpath("text()").extract_first()
            # Getting the link and link text from the tags

            if link is not None and text is not None and text.startswith("MIFR"):
                # For the links corresponding with MIFR, run the parse_page method
                print("link")
                print(link)
                print("text")
                print(text)
                yield scrapy.Request(self.base_url + link, callback=self.parse_page)

        next_page_partial_url = response.xpath(
            '//li[@class="pager__item pager__item--next"]/a/@href'
        ).extract_first()
        # Get the next page url from the next button's link
        if next_page_partial_url is not None:
            next_page_url = self.page_url + next_page_partial_url
            yield scrapy.Request(next_page_url, callback=self.parse)
            # Rerun the method on the next page
        else:
            print("done")
            yield None

    ##This is the archived, link-based parse method. It is more comprehensive since it selects all of the relevant URLs rather than
    ##going by the name (since a lot of the files don't start with MIFR)
    # def parse(self, response):
    #     selectors = response.xpath("//a")
    #     for selector in selectors:
    #         link = selector.xpath("@href").extract_first()
    #         exts = ['ar20', 'ar19', 'AR19', 'AR18']
    #         if link is not None and any(ext in link for ext in exts):
    #             yield scrapy.Request(self.base_url+link, callback=self.parse_page)
    #     next_page_partial_url = response.xpath('//li[@class="pager__item pager__item--next"]/a/@href').extract_first()
    #     if next_page_partial_url is not None:
    #         next_page_url = self.page_url + next_page_partial_url
    #         yield scrapy.Request(next_page_url, callback=self.parse)
    #     else:
    #         yield None

    def parse_page(self, response):

        selectors = response.xpath("//a")
        # Get all the <a>'s and loop through them
        for selector in selectors:

            link = selector.xpath("@href").extract_first()
            exts = ["stix"]
            if link is not None and any(ext in link for ext in exts):
                # Get the links to stix files

                if not link.startswith("http"):
                    link = self.base_url + link

                name = link.split("publications/")[1]
                # Getting the name from the URL rather than passing it in so that both parse methods can be interchanged

                print("done")
                print(link)
                print(name)

                file_name = "../reports/" + name

                if not os.path.isfile(file_name):
                    # Write to file if it doesn't already exist
                    response = requests.get(link)
                    with open(file_name, "xb") as output:
                        output.write(response.content)
                else:
                    print("file already downloaded")
