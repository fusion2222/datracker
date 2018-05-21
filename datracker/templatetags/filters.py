from django import template

register = template.Library()


@register.filter(name='add_field_textfield_classes')
def add_field_textfield_classes(field, class_name=None):
    """
    Adds specified className to single form field.
    """

    if not class_name:
        class_name = 'textfield'

    new_field_class = field.field.widget.attrs.get('class', '').split(' ')
    new_field_class.append(class_name)

    field.field.widget.attrs['class'] = ' '.join(new_field_class)
    return field


@register.filter(name='add_form_textfield_classes')
def add_form_textfield_classes(form, class_name=None):
    """
    Adds specified className to all fields in form. Situable for simple forms.
    """

    for field in form:
        add_field_textfield_classes(field=field, class_name=class_name)

    return form
