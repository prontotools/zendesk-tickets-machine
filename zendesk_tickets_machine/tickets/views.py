from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

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


class TicketNewView(View):
    def get(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            data = {
                'ticket': {
                    'subject': ticket.subject,
                    'comment': {
                        'body': ticket.comment
                    },
                    'requester_id': ticket.requester_id,
                    'assignee_id': ticket.assignee_id,
                }
            }
        except:
            data = {}

        zendesk_ticket = ZendeskTicket()
        result = zendesk_ticket.create(data)

        return JsonResponse(result)
