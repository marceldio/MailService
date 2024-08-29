from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mails.models import Maill


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


class MaillListView(ListView):
    model = Maill
    # template_name = "maill_list.html"


class MaillDetailView(DetailView):
    model = Maill


class MaillCreateView(CreateView):
    model = Maill
    fields = ["title", "body",]
    success_url = reverse_lazy("mails:maill_list")


class MaillUpdateView(UpdateView):
    model = Maill
    fields = ["title", "body",]
    success_url = reverse_lazy("mails:maill_list")

    def get_success_url(self):
        return reverse("mails:maill_detail", args=[self.kwargs.get("pk")])


class MaillDeleteView(DeleteView):
    model = Maill
    success_url = reverse_lazy("mails:maill_list")



