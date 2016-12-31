import json

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import UserMethods


class IndexView(TemplateView):
    """ Redirects to index. """
    template_name = 'index.html'


def datatable(request):
    """ Sends and receives DATATABLE response. """

    # Matches sort response with django model attr
    col_name_map = {'id': 'id',
                    'correo': 'email',
                    'username': 'username',
                    'first_name': 'first_name',
                    'last_name': 'last_name',
                    'date_joined': 'date_joined'}

    params = request.GET  # POST response is also valid

    sort_col_num = params.get('order[0][column]', 0)  # Header index
    sort_dir = params.get('order[0][dir]', 'asc')  # Header direction

    start_num = int(params.get('start', 0))  # Queryset start index
    num = int(params.get('length', 10))  # Queryset paginate

    sort_col_name = params.get('columns[{0}][data]'.format(sort_col_num))  # Header name
    sort_dir_prefix = (sort_dir == 'desc' and '-' or '')  # If sort_dir not asc

    obj_list = UserMethods.objects.all()  # Model queryset

    # Enables column filtering if field has been declared
    if sort_col_name in col_name_map:
        sort_col = col_name_map[sort_col_name]
        obj_list = obj_list.order_by('{0}{1}'.format(sort_dir_prefix, sort_col))

    search_text = params.get('search[value]', '').lower()  # SEARCH response

    # Filters by email or first name
    if search_text:
        obj_list = obj_list.filter(Q(email__icontains=search_text) | Q(first_name__icontains=search_text))

    # Updates queryset
    filtered_obj_list = obj_list

    # Returns filtered/ordered data as a JSON response
    records = {"recordsTotal": obj_list.count(),
               "recordsFiltered": filtered_obj_list.count(),
               "draw": int(params.get('draw', 1)), # prevents xss attacks
               "data": [obj.as_dict() for obj in filtered_obj_list[start_num:(start_num+num)]]}

    return HttpResponse(json.dumps(records), content_type='application/json')
