def parse_2013_2015(self, response):

    # define selector that contains all items
    all_people = response.css("section>aside")

    # iterate through items
    for person in all_people:
        raw = person.css("div>div>p:nth-child(3)>a::text").extract()[0]
        info = raw.split(' – ')
        # Different types of - have been used
        if len(info) == 1:
            info = raw.split(' - ')
        name, title = info
        # Clean up typo on webpage
        if ';' in title:
            title = title.replace(';', '')

        # find the year from the crawled URL
        url = response.request.url
        date_info = url.split("/")[4]
        year = date_info[:4]

        # Return item
        yield self.create_board(name, title, year)