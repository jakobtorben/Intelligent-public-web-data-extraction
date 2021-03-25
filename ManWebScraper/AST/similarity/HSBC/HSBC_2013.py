

# parse the board from 2013-2014
def parse_2013_2014(self, response):
    # define selector that contains all items
    all_people = response.css("div.profile-col1")

    # iterate through items
    for person in all_people:
        # manually parse name
        name = person.css("div>a.title-profile.text-red::text").get()
        # manually parse title
        title = person.css("div>p.profile-info.profile-desg.bold::text").get()

        # find the year from the crawled URL
        url = response.request.url
        date_info = url.split("/")[4]
        year = date_info[:4]

        # Return item
        yield self.create_board(name,title,year)

