from django import forms
from .models import Author, Quotes, Tag
from django_select2.forms import Select2Widget


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_loc', 'desc', 'photo_url']
        labels = {
            "fullname": "Authors Full Name",
            "born_date": "Date of birth",
            "born_loc": "Birth location",
            "desc": "Description",
            "photo_url": "Link to photo"
        }


class AddQuoteForm(forms.ModelForm):
    custom_tags = forms.CharField(label='Custom Tags', required=False)
    custom_author = forms.CharField(label='Custom Author', required=False)
    existing_author = forms.ModelChoiceField(queryset=Author.objects.all(),
                                             widget=Select2Widget(attrs={'style': 'width: 50%'}),
                                             label='Existing Author', required=False)

    class Meta:
        model = Quotes
        fields = ['quote', 'custom_tags']
        labels = {
            'quote': 'Quote',
        }

    def save(self, commit=True):
        quote = super().save(commit=False)

        if commit:
            quote.save()

        # Збереження введених тегів
        custom_tags_input = self.cleaned_data['custom_tags']
        if custom_tags_input:
            custom_tags = custom_tags_input.split()  # Розбиваємо введені теги за пробілами
            for custom_tag in custom_tags:
                tag, created = Tag.objects.get_or_create(name=custom_tag)
                quote.tags.add(tag)

        # Збереження введеного імені автора або вибраного існуючого
        custom_author = self.cleaned_data['custom_author']
        existing_author = self.cleaned_data['existing_author']
        if custom_author:
            author, created = Author.objects.get_or_create(fullname=custom_author)
            quote.author = author
        elif existing_author:
            quote.author = existing_author

        if commit:
            quote.save()
        return quote
