from django.db import models


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        if self.sub_category:
            return f'{self.sub_category}------->***{self.name}***'
        return f'{self.name}'

