import math

from flask import Request

from ..utils.utils import limit_int, parse_int

class Pagination:
    def __init__(self, request: Request) -> None:
        self.limit = limit_int(int(request.args.get('limit') or 25), 25)
        self.offset = parse_int(request.args.get('o'), 0)
        self.base = request.args.to_dict()
        self.current_page = math.floor(self.offset / self.limit) or 1 
        self.count = None
        self.total_pages = None

        self.base.pop('o', None)
    
    def add_count(self, count: int):
        self.count = count
        self.total_pages = math.floor(self.count / self.limit) or 1
