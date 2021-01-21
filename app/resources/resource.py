from config import constants


class Resource:
    def _get_pagination_params(self, request):
        page = request.args.get('page')
        size = request.args.get('size')

        self.page = int(page if page else constants.PAGE_NUMBER)
        self.size = int(size if size else constants.PAGE_SIZE)
        self.offset = (self.page - 1) * self.size
