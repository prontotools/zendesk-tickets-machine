from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import TicketForm
from .models import Ticket
from zendesk.api import Ticket as ZendeskTicket


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


class TicketEditView(TemplateView):
    template_name = 'tickets.html'

    def get(self, request, ticket_id):
        return render(
            request,
            self.template_name
        )
