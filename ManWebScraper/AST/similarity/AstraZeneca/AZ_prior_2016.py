def parse_prior_2016(self, response):
    url = response.request.url
    all_people = response.css('dl')
    for person in all_people:
        name = person.css('dt::text').getall()
        title = person.css('dd.description::text').getall()[0]
        year = self.find_year(url)
        yield self.create_board(name,title,year)