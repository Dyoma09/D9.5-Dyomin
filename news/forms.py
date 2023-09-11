from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'post_title',
            'author',
            'categories',
            'post_text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("post_title")
        content = cleaned_data.get("post_text")

        if name == content:
            raise ValidationError(
                "Описание должно быть отличным от названия."
            )

        return cleaned_data