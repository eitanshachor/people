import lxml.html


class Page:
    def __init__(self, input_val):
        """
        a Page can be instantiated with a url & options (TBD) needed to fetch it
        """
        self.input = input_val
        # TODO: special case, maybe __url__ or something?
        if hasattr(input_val, "url"):
            self.url = input_val.url

    def set_raw_data(self, raw_data):
        """ callback to handle raw data returned by grabbing the URL """
        self.raw_data = raw_data

    def get_data(self):
        """ return data extracted from this page and this page alone """
        raise NotImplementedError()


class HtmlPage(Page):
    def set_raw_data(self, raw_data):
        super().set_raw_data(raw_data)
        self.root = lxml.html.fromstring(raw_data)
        if hasattr(self.source, "url"):
            self.root.make_links_absolute(self.source.url)


class ListPage(Page):
    class SkipItem(Exception):
        pass

    def skip(self):
        raise self.SkipItem()


# TODO
# class CSVListPage(ListPage):
#     def get_data(self):
#         print(self.raw_data)
#         for item in items:
#             try:
#                 item = self.process_item(item)
#             except self.SkipItem:
#                 continue
#             yield item

#     def process_item(self, item):
#         return item


class HtmlListPage(ListPage, HtmlPage):
    """
    Simplification for HTML pages that get a list of items and process them.

    When overriding the class, instead of providing get_data, one must only provide
    a selector and a process_item function.
    """

    selector = None

    # common for a list page to only work on one URL, in which case it is more clear
    # to set it as a property
    def __init__(self, url=None):
        """
        a Page can be instantiated with a url & options (TBD) needed to fetch it
        """
        if url is not None:
            self.url = url

    def get_data(self):
        if not self.selector:
            raise NotImplementedError("must either provide selector or override scrape")
        items = self.selector.match(self.root)
        for item in items:
            try:
                item = self.process_item(item)
            except self.SkipItem:
                continue
            yield item

    def process_item(self, item):
        return item
