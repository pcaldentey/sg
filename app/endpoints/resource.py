from config import constants


class Resource:
    def _get_pagination_params(self, request):
        page = request.args.get('page')
        size = request.args.get('size')

        self.page = page if page else constants.PAGE_NUMBER
        self.size = size if size else constants.PAGE_SIZE
        self.offset = (int(self.page) - 1) * int(self.size)
