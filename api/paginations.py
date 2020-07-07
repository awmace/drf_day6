from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination


# 基础分页器
class NpfPageNumberPagination(PageNumberPagination):
    # 指定每页数据的数量
    page_size = 4
    # 可以通过此参数指定分页最大数量
    max_page_size = 6
    # 让前端具有修改每页数量的功能   url?page_size=每页数量
    page_size_query_param = "page_size"
    # 获取第几页的数据   url?page=页数
    page_query_param = "page"


# 偏移分页器
class NpfLimitPagination(LimitOffsetPagination):
    # 默认获取的每页数量
    default_limit = 3
    # 指定前端修改每页的数量  url?limit=数量
    limit_query_param = "limit"
    # 前端指定相对于第一条数据的偏移的数量  url?offset=偏移量
    offset_query_param = "offset"
    # 每页获取的最大数量，默认为Null
    # max_limit = 6


# 游标分页器 (加密:路径)  依赖于排序，不排序无法使用
class NpfCoursePagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 6
    ordering = "price"
