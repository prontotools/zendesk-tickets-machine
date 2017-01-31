from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .forms import TicketForm
from .models import Ticket


class TicketEditView(TemplateView):
    template_name = 'ticket_edit.html'

    def get(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            text = 'Oops! That board or ticket you are looking for ' \
                'no longer exists..'
            messages.error(request, text)

            return HttpResponseRedirect(reverse('boards'))

        initial = {
            'subject': ticket.subject,
            'comment': ticket.comment,
            'requester': ticket.requester,
            'created_by': ticket.created_by,
            'assignee': ticket.assignee,
            'assignee_id': ticket.assignee_id,
            'group': ticket.group,
            'ticket_type': ticket.ticket_type,
            'due_at': ticket.due_at,
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
        ticket.is_active = False
        ticket.save()

        board_slug = ticket.board.slug

        return HttpResponseRedirect(
            reverse('board_single', kwargs={'slug': board_slug})
        )
