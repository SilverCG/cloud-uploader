from django import forms
from filer.fields.file import FilerFileField
from uploader.models import Event, Upload
from django.contrib.admin import widgets      

class UploadFileForm(forms.ModelForm):
    event = forms.ModelChoiceField(queryset=Event.objects.all(), required=False)
    class Meta:
        model = Upload   
#     def save(self, event=None, *args, **kwargs):
#         if event:
#             obj = super(UploadFileForm, self).save(commit=False, *args, **kwargs)
#             obj.event = event
#             return obj.save()
#         return super(UploadFileForm, self).save(*args, **kwargs)

    
class EventForm(forms.ModelForm):
    name = forms.CharField(required=False)
    class Meta:
        model = Event
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminDateWidget()
        self.fields['date'].required = False
