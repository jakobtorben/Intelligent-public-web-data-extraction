def parse_2015_current(self, response):
    # define selector that contains all items
    all_people = response.css("section.component.promo-list.promo-list--tiles.promo-list--4-or-more-items.colour--palette-0").css("article.promo-list__item")

    # iterate through items
    for person in all_people:
        # manually parse name
        name = person.css("h3>a>span::text").get()

        # manually parse title
        title = person.css("p::text").get()
        # extract title from text body
        title = title.replace(name+" is ", '')

        # find the year from the crawled URL
        url = response.request.url
        date_info = url.split("/")[4]
        year = date_info[:4]

        # Return item
        yield self.create_board(name, title, year)