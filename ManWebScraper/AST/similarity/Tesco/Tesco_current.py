def parse_current(self, response):

    url = response.request.url

    all_people = response.css('div.people-profile__label')

    for person in all_people:
        name = person.css('strong::text').getall()[0]
        title = person.css('span::text').getall()[0]
        year = self.find_year(url)
        yield self.create_board(name,title,year)