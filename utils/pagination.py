import math
from django.core.paginator import Paginator


def make_pagination_range(
        page_range,
        qty_pages,
        current_page
):
    middle_page = math.ceil(qty_pages / 2)
    start_range = current_page - middle_page
    stop_range = current_page + middle_page
    total_pages = len(page_range)

    start_range_offset = abs(start_range)

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range -= abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_page,
        'last_page_out_of_range': stop_range < total_pages,
    }


def make_pagination(queryset, per_page, request, qty_pages=4):
    paginator = Paginator(queryset, per_page)
    current_page = request.GET.get('page', 1)
    page_obj = paginator.get_page(current_page)

    pagination = make_pagination_range(
        paginator.page_range,
        qty_pages,
        int(current_page)
    )

    return page_obj, pagination
