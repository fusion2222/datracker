class ChoiceEnum(object):
    choices = ()


class Pages(ChoiceEnum):
    ABOUT = 1
    DASHBOARD = 2
    FAQ = 3
    ISSUES = 4

    choices = (
        (ABOUT, 'About'),
        (DASHBOARD, 'Dashboard'),
        (FAQ, 'FAQ'),
        (ISSUES, 'Issues')
    )