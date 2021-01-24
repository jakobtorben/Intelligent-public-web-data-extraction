def parse_prior_2011(self, response):

    url = response.request.url

    all_people = response.css('div.bod_bio')

    for person in all_people:
        name, title = person.css('span::text').getall()[0].split(',')[:2]
        year = self.find_year(url)
        yield self.create_board(name,title,year)