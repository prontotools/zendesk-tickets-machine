from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from tickets.forms import TicketForm
from tickets.models import Ticket


class BoardView(View):
    def get(self, request):
        return HttpResponse()


class BoardSingleView(TemplateView):
    template_name = 'tickets.html'

    def get(self, request, slug):
        form = TicketForm()
        tickets = Ticket.objects.filter(board__slug=slug)
        zendesk_ticket_url = settings.ZENDESK_URL + '/agent/tickets/'

        return render(
            request,
            self.template_name,
            {
                'form': form,
                'tickets': tickets,
                'zendesk_ticket_url': zendesk_ticket_url

            }
        )
