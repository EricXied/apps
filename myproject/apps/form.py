from django import forms


class SavedFileInDjangoForm(forms.Form):
    save_file = forms.FileField
