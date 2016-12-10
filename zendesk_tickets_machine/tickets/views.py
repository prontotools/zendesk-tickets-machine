from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import TicketForm
from .models import Ticket


class TicketView(TemplateView):
    template_name = 'tickets.html'

    def get(self, request):
        form = TicketForm()
        tickets = Ticket.objects.all()

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'tickets': tickets
            }
        )

    def post(self, request):
        form = TicketForm(request.POST)
        form.save()

        tickets = Ticket.objects.all()

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'tickets': tickets
            }
        )
