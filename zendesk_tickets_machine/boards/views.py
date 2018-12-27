# -*- coding: utf-8 -*-
import os
import time

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, View

from django_tables2 import RequestConfig

from .models import Board, BoardGroup
from requesters.models import Requester
from tickets.forms import TicketForm, TicketUpdateOnceForm
from tickets.models import Ticket
from tickets.services import TicketServices
from tickets.tables import TicketTable
from zendesk.api import (
    Organization as ZendeskOrganization,
    User as ZendeskRequester,
    Ticket as ZendeskTicket,
)


class BoardView(TemplateView):
    template_name = 'boards.html'

    def get(self, request):
        board_group_id = request.GET.get('board_group')
        if board_group_id:
            board_group_id = int(board_group_id)
            boards = Board.objects.filter(board_group=board_group_id)
        else:
            boards = Board.objects.all()

        board_groups = BoardGroup.objects.all()

        return render(
            request,
            self.template_name,
            {
                'board_group_id': board_group_id,
                'board_groups': board_groups,
                'boards': boards,
            }
        )


class BoardSingleView(TemplateView):
    template_name = 'board_single.html'

    def get_context_to_render(self, **kwargs):
        firebase_messaging_sender_id = kwargs.get(
            'firebase_messaging_sender_id'
        )

        return {
            'board_name': kwargs.get('board_name'),
            'board_slug': kwargs.get('board_slug'),
            'form': kwargs.get('form'),
            'ticket_update_once_form': kwargs.get('ticket_update_once_form'),
            'tickets': kwargs.get('tickets'),
            'zendesk_ticket_url': kwargs.get('zendesk_ticket_url'),
            'firebase_api_key': settings.FIREBASE_API_KEY,
            'firebase_auth_domain': settings.FIREBASE_AUTH_DOMAIN,
            'firebase_database_url': settings.FIREBASE_DATABASE_URL,
            'firebase_project_id': settings.FIREBASE_PROJECT_ID,
            'firebase_storage_bucket': settings.FIREBASE_STORAGE_BUCKET,
            'firebase_messaging_sender_id': firebase_messaging_sender_id
        }

    def get_tickets(self, slug):
        tickets = TicketTable(
            Ticket.objects.filter(
                board__slug=slug, is_active=True
            ).order_by('id')
        )
        return tickets

    def get(self, request, slug):
        try:
            board = Board.objects.get(slug=slug)
        except Board.DoesNotExist:
            text = 'Oops! The board you are looking for ' \
                'no longer exists..'
            messages.error(request, text)

            return HttpResponseRedirect(reverse('boards'))

        initial = {
            'board': board.id
        }
        form = TicketForm(initial=initial)

        ticket_update_once_form = TicketUpdateOnceForm()

        tickets = self.get_tickets(slug)

        RequestConfig(request).configure(tickets)

        zendesk_ticket_url = settings.ZENDESK_URL + '/agent/tickets/'
        firebase_messaging_sender_id = settings.FIREBASE_MESSAGING_SENDER_ID

        context = self.get_context_to_render(
            board_name=board.name,
            board_slug=board.slug,
            form=form,
            ticket_update_once_form=ticket_update_once_form,
            tickets=tickets,
            zendesk_ticket_url=zendesk_ticket_url,
            firebase_messaging_sender_id=firebase_messaging_sender_id
        )

        return render(
            request,
            self.template_name,
            context
        )

    def post(self, request, slug):
        try:
            board = Board.objects.get(slug=slug)
        except Board.DoesNotExist:
            text = 'Oops! The board you are looking for ' \
                'no longer exists..'
            messages.error(request, text)

            return HttpResponseRedirect(reverse('boards'))

        form = TicketForm(request.POST)
        form.save()

        ticket_update_once_form = TicketUpdateOnceForm()

        tickets = self.get_tickets(slug)

        zendesk_ticket_url = settings.ZENDESK_URL + '/agent/tickets/'
        firebase_messaging_sender_id = settings.FIREBASE_MESSAGING_SENDER_ID

        context = self.get_context_to_render(
            board_name=board.name,
            board_slug=board.slug,
            form=form,
            ticket_update_once_form=ticket_update_once_form,
            tickets=tickets,
            zendesk_ticket_url=zendesk_ticket_url,
            firebase_messaging_sender_id=firebase_messaging_sender_id
        )

        return render(
            request,
            self.template_name,
            context
        )

    def edit_once(self):
        id_list = self.POST.getlist('id_list[]')
        edit_tags = self.POST.get('edit_tags')
        edit_subject = self.POST.get('edit_subject')
        edit_due_at = self.POST.get('edit_due_at')
        edit_assignee = self.POST.get('edit_assignee')
        edit_requester = self.POST.get('edit_requester')

        ticketServices = TicketServices()
        ticketServices.edit_ticket_once(
            id_list=id_list,
            edit_tags=edit_tags,
            edit_requester=edit_requester,
            edit_subject=edit_subject,
            edit_due_at=edit_due_at,
            edit_assignee=edit_assignee
        )

        return HttpResponse(content_type="application/json")


class BoardRequestersResetView(View):
    def get(self, request, slug):
        Ticket.objects.filter(board__slug=slug).update(
            requester='',
            organization=''
        )

        return HttpResponseRedirect(
            reverse('board_single', kwargs={'slug': slug})
        )


class BoardResetView(View):
    def get(self, request, slug):
        Ticket.objects.filter(board__slug=slug).update(zendesk_ticket_id=None)

        return HttpResponseRedirect(
            reverse('board_single', kwargs={'slug': slug})
        )


class BoardZendeskTicketsCreateView(View):
    def get(self, request, slug):
        zendesk_ticket = ZendeskTicket()
        zendesk_user = ZendeskRequester()
        zendesk_organization = ZendeskOrganization()

        selected_tickets = request.GET.get('tickets')
        if selected_tickets:
            tickets = Ticket.objects.filter(
                id__in=selected_tickets.split(','),
                board__slug=slug,
                is_active=True
            )
        else:
            tickets = Ticket.objects.filter(
                board__slug=slug,
                is_active=True
            )

        tickets = tickets.exclude(zendesk_ticket_id__isnull=False)

        for each in tickets:
            if each.requester == '':
                continue

            if each.assignee:
                assignee_id = each.assignee.zendesk_user_id
            else:
                assignee_id = os.environ.get('DEFAULT_ZENDESK_USER_ID', 0)

            requester_result = zendesk_user.search(each.requester)

            if each.due_at is not None:
                due_at = each.due_at.isoformat()
            else:
                due_at = ''

            if each.created_by:
                created_by = each.created_by.zendesk_user_id
            else:
                created_by = assignee_id

            try:
                requester_id = requester_result['users'][0]['id']
                data = {
                    'ticket': {
                        'subject': each.subject,
                        'comment': {
                            'body': each.comment,
                            'author_id': created_by
                        },
                        'requester_id': requester_id,
                        'assignee_id': assignee_id,
                        'group_id': each.group.zendesk_group_id,
                        'type': each.ticket_type,
                        'due_at': due_at,
                        'priority': each.priority,
                        'tags': [tag.strip() for tag in each.tags.split(',')]
                    }
                }

                organization_id = requester_result['users'][0][
                    'organization_id'
                ]
                organization_result = zendesk_organization.show(
                    organization_id
                )

                result = zendesk_ticket.create(data)
                ticket = result.get('ticket')
                if ticket:
                    each.zendesk_ticket_id = ticket.get('id')
                else:
                    requester_email = requester_result['users'][0]['email']
                    result_error = result.get('error')
                    result_requester = result.get('details').get('requester')
                    for each in result_requester:
                        each_description = each.get('description')
                        error_message = f'{result_error}: ' \
                            f'{each_description} ({requester_email})'
                        messages.error(request, error_message)
                    continue

                try:
                    each.organization = organization_result['organization'][
                        'name'
                    ]
                except KeyError:
                    each.organization = '---'

                each.save()

                Requester.objects.get_or_create(
                    email=each.requester,
                    zendesk_user_id=requester_id
                )

                data = {
                    'ticket': {
                        'comment': {
                            'author_id': assignee_id,
                            'body': each.private_comment,
                            'public': False
                        }
                    }
                }
                result = zendesk_ticket.create_comment(
                    data,
                    each.zendesk_ticket_id
                )
            except IndexError:
                pass

            if not settings.DEBUG:
                time.sleep(1)

        return HttpResponseRedirect(
            reverse('board_single', kwargs={'slug': slug})
        )
