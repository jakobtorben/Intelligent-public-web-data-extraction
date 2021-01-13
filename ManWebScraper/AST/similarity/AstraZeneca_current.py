def parse_current(self, response):

    url = response.request.url # this saves the url

    all_people = response.css('h2.bio__header')

    for person in all_people:
        name, title = person.css('span::text').getall()
        # strip necessary to remove white space and new line chars
        title = title[1:-1].strip(' ').strip('\n')
        year = self.find_year(url)
        yield self.create_board(name,title,year)