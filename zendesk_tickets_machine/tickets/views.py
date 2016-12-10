from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import TicketForm


class TicketView(TemplateView):
    template_name = 'tickets.html'

    def get(self, request):
        form = TicketForm()
        return render(
            request,
            self.template_name,
            {
                'form': form
            }
        )
