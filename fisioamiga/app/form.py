from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Agenda , Terapia


class AgendaDiaForm(ModelForm):
    class Meta: 
        model = Agenda 
        fields = "__all__"

class TerapiaForm(ModelForm):
    class Meta: 
        model = Terapia 
        fields = "__all__"
    
    
    

    # def init(self, args, **kwargs):
    #     super(AgendaDiaForm, self).init(args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         if field.widget.attrs.get('class'):
    #             field.widget.attrs['class'] += ' form-control'
    #         else:
    #             field.widget.attrs['class']='form-control'