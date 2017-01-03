from django.db import models
from django.template.defaultfilters import slugify

from board_groups.models import BoardGroup


class Board(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(
        max_length=300,
        null=True,
        blank=True,
        editable=False,
        unique=True
    )
    board_group = models.ForeignKey(BoardGroup, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Board, self).save(*args, **kwargs)
