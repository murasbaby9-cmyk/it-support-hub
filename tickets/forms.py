from django import forms
from .models import Request,Review
class EntryForm(forms.ModelForm):
    class Meta:
        model=Request
        fields=('name','phone','address','service','title','description','priority')
        labels=dict(name='Имя',phone='Телефон',address='Адрес (необязательно)',service='Услуга',title='Тема',description='Описание проблемы',priority='Срочность')
    def clean_title(self):
        v=self.cleaned_data['title']
        if len(v)<5: raise forms.ValidationError('Минимум 5 символов')
        return v
    def clean_phone(self):
        v=self.cleaned_data['phone']
        if not 7<=sum(c.isdigit() for c in v)<=15: raise forms.ValidationError('Укажите корректный телефон')
        return v
class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=('name','text')
        labels={'name':'Имя','text':'Отзыв'}
