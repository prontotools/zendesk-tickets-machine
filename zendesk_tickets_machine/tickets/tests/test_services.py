import datetime

from django.test import TestCase
from django.utils.timezone import utc

from ..models import Ticket
from ..services import TicketServices
from boards.models import Board
from agents.models import Agent
from agent_groups.models import AgentGroup
from requesters.models import Requester


class TicketServicesTest(TestCase):
    def setUp(self):
        agent = Agent.objects.create(name='Kan', zendesk_user_id='123')
        agent_group = AgentGroup.objects.create(
            name='Development',
            zendesk_group_id='123'
        )
        self.board = Board.objects.create(name='Pre-Production')
        self.first_ticket = Ticket.objects.create(
            subject='Ticket 1',
            comment='Comment 1',
            requester='client@hisotech.com',
            created_by=agent,
            assignee=agent,
            group=agent_group,
            ticket_type='question',
            priority='urgent',
            tags='welcome',
            private_comment='Private comment',
            zendesk_ticket_id='24328',
            board=self.board
        )
        self.second_ticket = Ticket.objects.create(
            subject='Ticket 2',
            comment='Comment 2',
            requester='client+another@hisotech.com',
            created_by=agent,
            assignee=agent,
            group=agent_group,
            ticket_type='question',
            priority='high',
            tags='welcome internal',
            private_comment='Private comment',
            board=self.board
        )

    def test_edit_ticket_once_edit_subject_and_tags_if_select_all(self):
        agent = Agent.objects.create(name='Natty', zendesk_user_id='456')
        requester = Requester.objects.create(
            email='customer@test.com', zendesk_user_id='123'
        )
        ticketServices = TicketServices()
        ticketServices.edit_ticket_once(
            [self.first_ticket.id, self.second_ticket.id],
            'aa bb',
            requester.email,
            'New Subject',
            '01/31/2017',
            agent)

        self.assertEqual(
            Ticket.objects.get(id=self.first_ticket.id).tags,
            'aa bb'
            )
        self.assertEqual(
            Ticket.objects.get(id=self.second_ticket.id).tags,
            'aa bb'
            )
        self.assertEqual(
            Ticket.objects.get(id=self.first_ticket.id).requester,
            requester.email
            )
        self.assertEqual(
            Ticket.objects.get(id=self.second_ticket.id).requester,
            requester.email
            )
        self.assertEqual(
            Ticket.objects.get(id=self.first_ticket.id).subject,
            'New Subject'
            )
        self.assertEqual(
            Ticket.objects.get(id=self.second_ticket.id).subject,
            'New Subject'
            )
        self.assertEqual(
            Ticket.objects.get(id=self.first_ticket.id).due_at,
            datetime.datetime.strptime(
                '01/31/2017', "%m/%d/%Y"
            ).replace(tzinfo=utc)
        )
        self.assertEqual(
            Ticket.objects.get(id=self.second_ticket.id).due_at,
            datetime.datetime(2017, 1, 31, tzinfo=utc)
        )
        self.assertEqual(
            Ticket.objects.get(id=self.first_ticket.id).assignee,
            agent
        )
        self.assertEqual(
            Ticket.objects.get(id=self.second_ticket.id).assignee,
            agent
        )

    def test_edit_ticket_once_if_select_one(self):
        agent = Agent.objects.create(name='Natty', zendesk_user_id='456')
        requester = Requester.objects.create(
            email='customer@test.com', zendesk_user_id='123'
        )
        ticketServices = TicketServices()
        ticketServices.edit_ticket_once(
            [self.first_ticket.id],
            'aa bb',
            requester.email,
            'New Subject',
            '01/31/2017',
            agent)

        self.assertEqual(
            Ticket.objects.get(id=self.first_ticket.id).tags,
            'aa bb'
            )
        self.assertNotEqual(
            Ticket.objects.get(id=self.second_ticket.id).tags,
            'aa bb'
            )
        self.assertEqual(
            Ticket.objects.get(id=self.first_ticket.id).requester,
            requester.email
            )
        self.assertNotEqual(
            Ticket.objects.get(id=self.second_ticket.id).requester,
            requester.email
            )
        self.assertEqual(
            Ticket.objects.get(id=self.first_ticket.id).subject,
            'New Subject'
            )
        self.assertNotEqual(
            Ticket.objects.get(id=self.second_ticket.id).subject,
            'New Subject'
            )
        self.assertEqual(
            Ticket.objects.get(id=self.first_ticket.id).due_at,
            datetime.datetime.strptime(
                '01/31/2017', "%m/%d/%Y"
            ).replace(tzinfo=utc)
        )
        self.assertNotEqual(
            Ticket.objects.get(id=self.second_ticket.id).due_at,
            datetime.datetime(2017, 1, 31, tzinfo=utc)
        )
        self.assertEqual(
            Ticket.objects.get(id=self.first_ticket.id).assignee,
            agent
        )
        self.assertNotEqual(
            Ticket.objects.get(id=self.second_ticket.id).assignee,
            agent
        )
