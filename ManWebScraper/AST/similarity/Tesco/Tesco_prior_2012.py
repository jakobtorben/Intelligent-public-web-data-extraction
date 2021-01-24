def parse_prior_2012(self, response):

    url = response.request.url

    all_people = response.css('#management').css('li')
    for person in all_people:
        name = person.css('h3::text').getall()[0]
        title = person.css('h4::text').getall()[0]
        year = self.find_year(url)
        yield self.create_board(name,title,year)