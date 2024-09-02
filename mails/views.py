from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from blog.models import Blog
from mails.forms import RecipientForm, SendingForm, MaillForm
from mails.models import Recipient, Sending, Maill, Event


def about(request):
    return render(request, "mails/about.html")


def contact(request):
    return render(request, "mails/contact.html")


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    context_object_name = "recipients"
    template_name = "mails/recipient_list.html"

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
    form_class = RecipientForm
    success_url = reverse_lazy("mails:recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = [
        "email",
        "id",
        "comment",
    ]
    success_url = reverse_lazy("mails:recipient_list")

    def get_success_url(self):
        return reverse("mails:recipient_view", args=[self.kwargs.get("pk")])


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("mails:recipient_list")


class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    context_object_name = "sendings"
    template_name = "mails/sending_list.html"

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
    context_object_name = "mails"
    template_name = "mails/maill_list.html"

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
    form_class = MaillForm

    def get_success_url(self):
        return reverse("mails:maill_detail", args=[self.kwargs.get("pk")])
        # return reverse("mails:maill_detail")


class MaillDeleteView(DeleteView):
    model = Maill
    success_url = reverse_lazy("mails:maill_list")
    extra_context = {"title": "Удаление письма"}


class HomePageView(View):
    template_name = "mails/home_page.html"  # Указываем шаблон

    def get(self, request, *args, **kwargs):
        total_sendings = Sending.objects.count()
        active_sendings = Sending.objects.filter(status="launched").count()
        unique_recipients = Recipient.objects.distinct("email").count()

        # Получение трех случайных статей из блога
        total_articles = Blog.objects.count()
        if total_articles >= 3:
            random_articles = sample(list(Blog.objects.all()), 3)
        else:
            random_articles = Blog.objects.all()

        context = {
            "total_sendings": total_sendings,
            "active_sendings": active_sendings,
            "unique_recipients": unique_recipients,
            "random_articles": random_articles,
        }
        return render(request, self.template_name, context)


class EventReportView(ListView):
    model = Event
    template_name = "mails/event_report.html"
    context_object_name = "events"
    paginate_by = 20  # Количество событий на одной странице, если нужно

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(event_status=status)
        return queryset.order_by("-event_datetime")
