def parse_intermediate(self, response):
    url = response.request.url
    paragraphs = response.css('p')

    for p in paragraphs:
        name = p.css('font::text') if not p.css('strong::text').get() else p.css('strong::text')
        if name.get():
            item = Board()
            item['name'] = name.get()
            item['company'] = 'AstraZeneca'

            title = p
            print(title)
            item['title'] = title
            item['year'] = self.find_year(url)
            yield item