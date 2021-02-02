def parse_2013_2015(self, response):
    # define selector that contains all items
    all_people = response.css("div.directorylist.parbase.basecomponent")

    # iterate through items
    for person in all_people:
        # manually parse name

        name = person.css("div>div>div.text>h3>a::text").get()
        # Remove trailing \n and \t
        name = name.strip("\n\t")

        # manually parse title
        title = person.css("div>div>div.text>p::text").get()
        title = title.strip("\n\t")

        # find the year from the crawled URL
        url = response.request.url
        date_info = url.split("/")[4]
        year = date_info[:4]

        # Return item
        yield self.create_board(name, title, year)