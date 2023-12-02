from django import forms

PROJECT_STATUS = (("active", "active"), ("deactive", "deactive"))


class ProjectsForm(forms.Form):
    name = forms.CharField(max_length=32)
    description = forms.CharField(max_length=256)
    status_select = forms.ChoiceField(choices=PROJECT_STATUS)
    cover_image = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super(ProjectsForm, self).clean()

        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        status_select = cleaned_data.get("status_select")

        if not name or not description or not status_select:
            raise forms.ValidationError("Invalid Required Values")
