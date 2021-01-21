def parse_current(self, response):

    # define selector that contains all items
    all_people = response.css("article")

    # iterate through items
    for person in all_people:
        # manually parse name
        name = person.css("div>h3>a").attrib['title']
        # manually parse title
        title = person.css("div>h3>a::text").get()

        now = datetime.datetime.now()
        year = now.year

        # Return item
        yield self.create_board(name, title, year)