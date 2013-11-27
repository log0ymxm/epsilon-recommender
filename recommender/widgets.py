from django.forms.widgets import CheckboxSelectMultiple


class ChoiceFieldRenderer(object):
    """
An object used by RadioSelect to enable customization of radio widgets.
"""

    choice_input_class = None

    def __init__(self, name, value, attrs, choices):
        self.name = name
        self.value = value
        self.attrs = attrs
        self.choices = choices

    def __getitem__(self, idx):
        choice = self.choices[idx] # Let the IndexError propagate
        return self.choice_input_class(self.name, self.value, self.attrs.copy(), choice, idx)

    def __str__(self):
        return self.render()



class CustomChoiceFieldRenderer(object):

    columns = 3
    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).
        """
        id_ = self.attrs.get('id', None)
        start_tag = format_html('<div id="{0}">', id_) if id_ else '<div>'
        output = [start_tag]
        for i, choice in enumerate(self.choices):
            if i%self.columns == 0:
                format_html('<ul class="col-md-3">')
            choice_value, choice_label = choice
            if isinstance(choice_label, (tuple, list)):
                attrs_plus = self.attrs.copy()
                if id_:
                    attrs_plus['id'] += '_{0}'.format(i)
                sub_ul_renderer = ChoiceFieldRenderer(name=self.name,
                                                      value=self.value,
                                                      attrs=attrs_plus,
                                                      choices=choice_label)
                sub_ul_renderer.choice_input_class = self.choice_input_class
                output.append(format_html('<li>{0}{1}</li>', choice_value,
                                          sub_ul_renderer.render()))
            else:
                w = self.choice_input_class(self.name, self.value,
                                            self.attrs.copy(), choice, i)
                output.append(format_html('<li>{0}</li>', force_text(w)))
            if i%self.columns == self.columns:
                format_html('</ul>')
        output.append('</div>')

        return mark_safe('\n'.join(output))

class CustomCheckboxFieldRenderer(CustomChoiceFieldRenderer):
    pass

class CustomCheckboxSelectMultiple(CheckboxSelectMultiple):
    renderer = CustomCheckboxFieldRenderer