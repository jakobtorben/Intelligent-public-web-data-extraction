def parse_prior_2016(self, response):
    url = response.request.url
    all_people = response.css('dl')
    for person in all_people:
        name = person.css('dt::text').getall()
        title = person.css('dd.description::text').getall()[0]

        item = Board()
        item['company'] = 'AstraZeneca'
        item['name'] = name
        item['title'] = title
        item['year'] = self.find_year(url)
        yield item