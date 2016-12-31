from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Board
from tickets.forms import TicketForm
from tickets.models import Ticket


class BoardView(TemplateView):
    template_name = 'boards.html'

    def get(self, request):
        boards = Board.objects.all()

        return render(
            request,
            self.template_name,
            {
                'boards': boards
            }
        )


class BoardSingleView(TemplateView):
    template_name = 'board_single.html'

    def get(self, request, slug):
        board = Board.objects.get(slug=slug)

        form = TicketForm()
        tickets = Ticket.objects.filter(board__slug=slug)
        zendesk_ticket_url = settings.ZENDESK_URL + '/agent/tickets/'

        return render(
            request,
            self.template_name,
            {
                'board_name': board.name,
                'form': form,
                'tickets': tickets,
                'zendesk_ticket_url': zendesk_ticket_url

            }
        )
