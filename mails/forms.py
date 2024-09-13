from django import forms
from django.forms import ModelForm
from mails.models import Maill, Recipient, Sending


class MaillForm(forms.ModelForm):
    class Meta:
        model = Maill
        exclude = ("author",)

    # Список запрещенных слов
    forbidden_words = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    def clean_name(self):
        name = self.cleaned_data.get("title")
        if any(word in name.lower() for word in self.forbidden_words):
            raise forms.ValidationError("Заголовок содержит запрещенные слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("body")
        if any(word in description.lower() for word in self.forbidden_words):
            raise forms.ValidationError("Содержание содержит запрещенные слова.")
        return description


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        exclude = ("owner",)


class SendingForm(forms.ModelForm):
    class Meta:
        model = Sending
        fields = ["letter", "recipient", "frequency", "status"]
        widgets = {
            "recipients": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Извлекаем текущего пользователя
        super(SendingForm, self).__init__(*args, **kwargs)

        # Фильтруем список адресатов, исключая самого пользователя
        if user:
            self.fields["recipient"].queryset = Recipient.objects.filter(
                owner=user
            ).exclude(email=user.email)


class SendingManagerForm(ModelForm):
    class Meta:
        model = Sending
        fields = ("is_active",)
