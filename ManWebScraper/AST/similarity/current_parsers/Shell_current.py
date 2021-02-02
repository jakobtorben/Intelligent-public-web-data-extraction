def parse_current(self, response):
    # define selector that contains all items
    all_people = response.css("div.component.component--fat.promo-list.promo-list--tiles.promo-list--4-or-more-items.promo-list--palette-0").css("div.promo-list__text")

    # iterate through items
    for person in all_people:
        # manually parse name
        name = person.css("h3>a>span::text").get()

        # manually parse title
        title = person.css("p::text").get()

        now = datetime.datetime.now()
        year = now.year

        # Return item
        yield self.create_board(name, title, year)