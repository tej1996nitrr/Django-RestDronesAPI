from rest_framework.pagination import LimitOffsetPagination

class LimitUpperBound(LimitOffsetPagination):
    max_limit=8
