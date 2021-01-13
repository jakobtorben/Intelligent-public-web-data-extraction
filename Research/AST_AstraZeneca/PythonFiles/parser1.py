def parse_current(self, response):
    url = response.request.url  # this saves the url

    all_people = response.css('h2.bio__header')

    for person in all_people:
        name, title = person.css('span::text').getall()
        item = Board()
        item['company'] = 'AstraZeneca'
        item['name'] = name
        # strip necessary to remove white space and new line chars
        item['title'] = title[1:-1].strip(' ').strip('\n')
        item['year'] = self.find_year(url)
        print(name, title)
        yield item