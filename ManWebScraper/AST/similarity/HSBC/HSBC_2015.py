def parse_2015_2018(self, response):
    # define selector that contains all items
    all_people = response.css("li.profile-col1")

    # iterate through items
    for person in all_people:
        # manually parse name
        name = person.css("div>h3>a.title-profile.text-red::text").get()
        # manually parse title
        title = person.css("div>p.profile-info::text").get()

        # find the year from the crawled URL
        url = response.request.url
        date_info = url.split("/")[4]
        year = date_info[:4]

        # Return item
        yield self.create_board(name,title,year)