from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Sheet(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, null=True, blank=True, editable=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Sheet, self).save(*args, **kwargs)