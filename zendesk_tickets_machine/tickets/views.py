from django.shortcuts import render
from django.views.generic import TemplateView


class TicketView(TemplateView):
    template_name = 'tickets.html'

    def get(self, request):
        return render(request, self.template_name)
