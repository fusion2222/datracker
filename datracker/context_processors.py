from datracker.models import Page

def navbar_menu(request):

    pages = Page.objects.all().order_by('pk')

    output = [{'label': page.label, 'url': '#get_absolute_link'} for page in pages]

    return {'navbar_links': output}
