def parse_current(self, response):
    # define selector that contains all items
    all_people = response.css("li.directors-index__item")

    # iterate through items
    for person in all_people:
        # manually parse name
        name = person.css("a>div>div>h3.contact-large-image-teaser__header::text").get()
        # manually parse title
        title = person.css("a>div>div>p>span::text").get()

        now = datetime.datetime.now()
        year = now.year

        # Return item
        yield self.create_board(name,title,year)