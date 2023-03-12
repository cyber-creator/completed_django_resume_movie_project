from django import forms

from .models import Review, Comment, Contact


class FormReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'review', 'rating')


class FormComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
