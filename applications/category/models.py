from typing import Iterable, Optional
from django.db import models
from slugify import slugify

# Create your models here.

class Category(models.Model):
    slug = models.SlugField(primary_key=True, blank=True)
    title = models.CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)  
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        