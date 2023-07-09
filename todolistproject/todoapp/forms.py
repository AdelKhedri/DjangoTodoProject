from django import forms

class ToDoItemForm(forms.Form):
    title = forms.CharField(max_length=100,
                           help_text="this filed is required",
                           required=True,
                           label='title',
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'id': 'title',
                                   'placeholder': 'title',
                               }
                           ))
    description = forms.CharField(max_length=400,
                                 help_text="description",
                                 required=False,
                                 label='description',
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'id': 'description',
                                         'placeholder': 'description',
                                     }
                                 ))


class ToDoListForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="name", widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                        'id': 'name',
                                                                                        'placeholder': 'name'}))