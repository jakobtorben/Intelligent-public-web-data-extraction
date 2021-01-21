def parse_2015_2020(self, response):

    # define selector that contains all items
    all_people = response.css("article")

    # iterate through items
    for person in all_people:
        # manually parse name
        name = person.css("div>h3>a").attrib['title']
        # manually parse title
        title = person.css("div>h3>a::text").get()

        # find the year from the crawled URL
        url = response.request.url
        date_info = url.split("/")[4]
        year = date_info[:4]

        # Return item
        yield self.create_board(name, title, year)