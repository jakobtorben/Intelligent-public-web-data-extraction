def parse_current(self, response):
    # define selector that contains all items
    all_people = response.css("li.grid-listing__item")
    print(all_people)
    # iterate through items
    for person in all_people:
        # manually parse name
        name = person.css("a>div>h2::text").get()
        # manually parse title
        title = person.css("a>div>p::text").get()

        now = datetime.datetime.now()
        year = now.year

        # Return item
        yield self.create_board(name,title,year)