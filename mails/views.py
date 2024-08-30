from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from mails.forms import RecipientForm, SendingForm, MaillForm
from mails.models import Recipient, Sending, Maill


def home(request):
    return render(request, "mails/home.html")


def about(request):
    return render(request, "mails/about.html")


def contact(request):
    return render(request, "mails/contact.html")


class RecipientListView(ListView):
    model = Recipient

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        recipients = Recipient.objects.all()
        context_data["recipients"] = recipients
        context_data["title"] = "Адресаты"
        return context_data


class RecipientDetailView(DetailView):
    model = Recipient


class RecipientCreateView(CreateView):
    model = Recipient
    # fields = ["email", "id", "comment"]
    form_class = RecipientForm
    success_url = reverse_lazy("mails:recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = [
        "title",
        "body",
    ]
    success_url = reverse_lazy("mails:recipient_list")

    def get_success_url(self):
        return reverse("mails:recipient_view", args=[self.kwargs.get("pk")])


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("mails:recipient_list")


class SendingListView(ListView):
    model = Sending

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        sendings = Sending.objects.all()
        context_data["sendings"] = sendings
        context_data["title"] = "Рассылки"
        return context_data


class SendingCreateView(CreateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy("mails:sending_list")
    extra_context = {"button_name": "Создать", "title": "Создать рассылку"}


class SendingDeleteView(DeleteView):
    model = Sending
    success_url = reverse_lazy("mails:sending_list")
    extra_context = {"title": "Удаление рассылки"}


class MaillListView(ListView):
    model = Maill

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mails = Sending.objects.all()
        context_data["mails"] = mails
        context_data["title"] = "Письма"
        return context_data


class MaillDetailView(DetailView):
    model = Maill


class MaillCreateView(CreateView):
    model = Maill
    form_class = MaillForm
    success_url = reverse_lazy("mails:maill_list")


class MaillUpdateView(UpdateView):
    model = Maill
    fields = [
        "title",
        "body",
    ]

    def get_success_url(self):
        return reverse("mails:maill_detail", args=[self.kwargs.get("pk")])


class MaillDeleteView(DeleteView):
    model = Maill
    success_url = reverse_lazy("mails:maill_list")
    extra_context = {"title": "Удаление письма"}
