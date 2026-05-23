from django.core.paginator import Paginator


def paginate(queryset, per_page, request):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get('page'))
