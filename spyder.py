import scrapy


class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.sib.swiss/national-network/groups-and-group-leaders']

    # def parse(self, response):
    #     for link in response.css('a::attr(href)').getall():
    #         if "-group" in link:
    #             replaced_link = link.replace("-", " ")
    #             yield {'link': response.urljoin(link),'group-name': replaced_link}

    def parse(self, response):
        for link in response.css('a::attr(href)').getall():
            if "-group" in link:
                absolute_link = response.urljoin(link)
                request = scrapy.Request(absolute_link, callback=self.parse_group_page)
                request.meta['absolute_link'] = absolute_link
                request.meta['replaced_link'] = absolute_link.replace("-", " ")
                yield request

    def parse_group_page(self, response):
        # Estrae il testo all'interno del div, di p, e di a.
        description_list = response.css(
            'div.person-description::text, div.person-description p::text, div.person-description a::text').getall()
        description_text = " ".join(description_list).strip()  # Concatena tutti i pezzi di testo
        yield {
            'link': response.meta['absolute_link'],
            'replaced_link': response.meta['replaced_link'],
            'description': description_text
        }
