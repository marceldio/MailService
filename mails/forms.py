from django import forms
from django.forms import ModelForm
from mails.models import Maill, Recipient, Sending


class MailsModeratorForm(ModelForm):
    class Meta:
        model = Maill
        fields = ("title", "body")


class MaillForm(forms.ModelForm):
    class Meta:
        model = Maill
        exclude = ("recipient",)

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
        fields = "__all__"


class SendingForm(forms.ModelForm):
    class Meta:
        model = Sending
        fields = ["letter", "recipients", "frequency", "status"]
        widgets = {
            "recipients": forms.CheckboxSelectMultiple,
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # передача текущего пользователя в форму
        return kwargs
