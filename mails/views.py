from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
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
from mails.forms import RecipientForm, SendingForm, MaillForm, SendingManagerForm
from mails.models import Recipient, Sending, Maill, Event
from mails.services import (
    get_sendings_from_cache,
    get_mails_from_cache,
    get_recipients_from_cache,
)


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
        # return Recipient.objects.filter(owner=self.request.user)
        return get_recipients_from_cache(self)

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

    def form_valid(self, form):
        recipient = form.save(commit=False)
        recipient.owner = self.request.user  # Присваиваем текущего пользователя
        recipient.save()
        return redirect(self.success_url)


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


class SendingListView(ListView):
    model = Sending
    context_object_name = "sendings"
    template_name = "mails/sending_list.html"

    def get_queryset(self):
        # Возвращаем только объекты, принадлежащие текущему пользователю
        # return Sending.objects.filter(company=self.request.user)
        return get_sendings_from_cache()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["title"] = "Рассылки"
        return context_data


class SendingCreateView(CreateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy("mails:sending_list")
    # extra_context = {"button_name": "Создать", "title": "Создать рассылку"}

    def form_valid(self, form):
        # Передаем текущего пользователя в метод save для установки company
        form.instance.company = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        # Передаем текущего пользователя в kwargs
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class SendingUpdateView(LoginRequiredMixin, UpdateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy("mails:sending_list")
    extra_context = {"button_name": "Сохранить", "title": "Редактировать рассылку"}

    def get_form_class(self):
        user = self.request.user
        if user == self.object.company:
            return SendingForm
        if user.has_perm("mails.can_disable_sending") and user.has_perm(
            "mails.can_view_sending"
        ):
            return SendingManagerForm
        raise PermissionDenied


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
        # return Maill.objects.filter(author=self.request.user)
        return get_mails_from_cache(self)

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

    def get_queryset(self):
        # Фильтруем события только для текущего пользователя
        event_list = Event.objects.all()[::-1]
        return event_list[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = self.get_queryset()
        return context
