from datracker.models import Page


def navbar_menu(request):

    pages = Page.objects.all().order_by('pk')

    output = [{'label': page.label, 'url': page.get_absolute_url()} for page in pages]

    if request.user.is_authenticated:
        output.append({'label': 'Logout', 'url': 'admin/logout'})

    return {'navbar_links': output}
