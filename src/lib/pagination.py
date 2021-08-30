import math

from flask import Request

from ..utils.utils import limit_int

class Pagination:
    def __init__(self, request: Request, count: int) -> None:
        self.limit = limit_int(int(request.args.get('limit') or 25), 25)
        self.offset = int(request.args.get('o') or 0)
        self.count = count
        self.base = request.args.get('o')
        self.current_page = math.floor(self.offset / self.limit) 
        self.total_pages = math.floor(count / self.limit)
