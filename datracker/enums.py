

class ChoiceEnum(object):
    choices = ()

    @classmethod
    def keys(cls):
        return [key for key, value in cls.choices]

    @classmethod
    def labels(cls):
        return [value for key, value in cls.choices]


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


class IssueCategories(ChoiceEnum):
    DEVELOPMENT = 1
    PERSONAL = 2
    DOCUMENTATION = 3
    RELIGIOUS = 4
    POLITICAL = 5

    choices = (
        (DEVELOPMENT, 'Development'),
        (PERSONAL, 'Personal'),
        (DOCUMENTATION, 'Documentation'),
        (RELIGIOUS, 'Religious'),
        (POLITICAL, 'Political'),
    )