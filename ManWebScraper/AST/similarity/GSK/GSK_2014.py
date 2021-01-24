def parse_2014_2016(self, response):
    # define selector that contains all items
    all_people = response.css("a.titleLink.textDecorateNone")

    # iterate through items
    for person in all_people:
        # manually parse name
        name = person.css("h2>span.textDecorateNone::text").getall()[0]
        print(name)
        # manually parse title
        title = person.css("h2>span.textDecorateNone::text").getall()[1]

        # find the year from the crawled URL
        url = response.request.url
        date_info = url.split("/")[4]
        year = date_info[:4]

        # Return item
        yield self.create_board(name,title,year)