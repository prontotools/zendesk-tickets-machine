from django.test import TestCase

from ..models import BoardGroup


class BoardGroupTest(TestCase):
    def test_save_board_group(self):
        board_group = BoardGroup()
        board_group.name = 'CP Production'
        board_group.save()

        board_group = BoardGroup.objects.last()

        self.assertEqual(board_group.name, 'CP Production')

    def test_board_group_should_represent_name_by_default(self):
        board_group = BoardGroup.objects.create(
            name='CP Production'
        )
        self.assertEquals(board_group.__str__(), 'CP Production')
