from django.contrib.auth.mixins import LoginRequiredMixin
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


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    context_object_name = 'recipients'
    template_name = 'mails/recipient_list.html'

    def get_queryset(self):
        # Возвращаем только объекты, принадлежащие текущему пользователю
        return Recipient.objects.filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
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
        "email", "id", "comment",
    ]
    success_url = reverse_lazy("mails:recipient_list")

    def get_success_url(self):
        return reverse("mails:recipient_view", args=[self.kwargs.get("pk")])


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("mails:recipient_list")


class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    context_object_name = 'sendings'
    template_name = 'mails/sending_list.html'

    def get_queryset(self):
        # Возвращаем только объекты, принадлежащие текущему пользователю
        return Sending.objects.filter(company=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Рассылки"
        return context_data


class SendingCreateView(CreateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy("mails:sending_list")
    extra_context = {"button_name": "Создать", "title": "Создать рассылку"}

    def form_valid(self, form):
        # Передаем текущего пользователя в метод save для установки company
        form.instance.company = self.request.user
        return super().form_valid(form)


class SendingUpdateView(UpdateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy("mails:sending_list")
    extra_context = {"button_name": "Сохранить", "title": "Редактировать рассылку"}


class SendingDeleteView(DeleteView):
    model = Sending
    success_url = reverse_lazy("mails:sending_list")
    extra_context = {"title": "Удаление рассылки"}


class SendingDetailView(DetailView):
    model = Sending



class MaillListView(ListView):
    model = Maill
    context_object_name = 'mails'
    template_name = 'mails/maill_list.html'

    def get_queryset(self):
        # Возвращаем только объекты, принадлежащие текущему пользователю
        return Maill.objects.filter(author=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
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
    # fields = [
    #     "title",
    #     "body",
    # ]
    form_class = MaillForm

    def get_success_url(self):
        return reverse("mails:maill_detail", args=[self.kwargs.get("pk")])
        # return reverse("mails:maill_detail")


class MaillDeleteView(DeleteView):
    model = Maill
    success_url = reverse_lazy("mails:maill_list")
    extra_context = {"title": "Удаление письма"}
