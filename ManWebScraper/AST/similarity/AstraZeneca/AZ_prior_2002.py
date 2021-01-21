def parse_prior_2002(self, response):
    url = response.request.url
    tables = response.css('table')
    cells = tables[17].css('td')
    for i, cell in enumerate(cells):
        if i != 0:
            if i % 2 == 1:
                item = Board()
                name = cell.css('b::text').get()
                try:
                    name = [item.strip(' ') for item in name.split('\n')]
                    name = ' '.join(name)
                except Exception as e:
                    name = 0
            else:
                title = cell.css('font::text').get()
                try:
                    title = [item.strip(' ') for item in title.split('\n')]
                    title = ' '.join(title)
                except Exception as e:
                    title = 0
                year = self.find_year(url)
                yield self.create_board(name,title,year)