# llama_processor/forms.py
from django import forms

class TextFileUploadForm(forms.Form):
    text_file = forms.FileField(label='Select a text file')