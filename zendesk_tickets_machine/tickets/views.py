from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

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


class TicketNewView(View):
    def get(self, request, ticket_id):
        return HttpResponse()
