import requests


class Ticket(object):
    def create(self):
        requests.post(
            'https://pronto1445242156.zendesk.com/api/v2/tickets.json'
        )
