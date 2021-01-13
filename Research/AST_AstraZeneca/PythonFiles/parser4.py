def parse_prior_2002(self, response):
    url = response.request.url
    tables = response.css('table')
    cells = tables[17].css('td')
    for i, cell in enumerate(cells):
        if i != 0:
            if i % 2 == 1:
                item = Board()
                item['company'] = 'AstraZeneca'
                name = cell.css('b::text').get()
                try:
                    name = [item.strip(' ') for item in name.split('\n')]
                    name = ' '.join(name)
                    item['name'] = name
                except Exception as e:
                    print(e)
                    item['name'] = 0
            else:
                title = cell.css('font::text').get()
                try:
                    title = [item.strip(' ') for item in title.split('\n')]
                    title = ' '.join(title)
                    item['title'] = title
                except Exception as e:
                    print(e)
                    item['title'] = 0
                item['year'] = self.find_year(url)

                yield item