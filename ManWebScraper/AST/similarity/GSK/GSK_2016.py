def parse_2016_current(self, response):
    # define selector that contains all items
    all_people = response.css("article.listing-item.with-image")

    # iterate through items
    for person in all_people:
        # manually parse name
        name = person.css("h3>a::text").get()
        # manually parse title
        title = person.css("p::text").get()

        # find the year from the crawled URL
        url = response.request.url
        date_info = url.split("/")[4]
        year = date_info[:4]

        # Return item
        yield self.create_board(name,title,year)