from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .forms import TicketForm
from .models import Ticket


class TicketEditView(TemplateView):
    template_name = 'ticket_edit.html'

    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)

        initial = {
            'subject': ticket.subject,
            'comment': ticket.comment,
            'requester': ticket.requester,
            'requester_id': ticket.requester_id,
            'assignee': ticket.assignee,
            'assignee_id': ticket.assignee_id,
            'group': ticket.group,
            'ticket_type': ticket.ticket_type,
            'priority': ticket.priority,
            'tags': ticket.tags,
            'private_comment': ticket.private_comment,
            'zendesk_ticket_id': ticket.zendesk_ticket_id,
            'board': ticket.board.id
        }
        form = TicketForm(initial=initial)

        return render(
            request,
            self.template_name,
            {
                'board_slug': ticket.board.slug,
                'form': form
            }
        )

    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form = TicketForm(request.POST, instance=ticket)
        form.save()

        return HttpResponseRedirect(
            reverse('board_single', kwargs={'slug': ticket.board.slug})
        )


class TicketDeleteView(View):
    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        board_slug = ticket.board.slug
        ticket.delete()

        return HttpResponseRedirect(
            reverse('board_single', kwargs={'slug': board_slug})
        )
