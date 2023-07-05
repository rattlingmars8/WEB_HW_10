from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.CharField(max_length=50)
    born_loc = models.CharField(max_length=150)
    desc = models.TextField()
    photo_url = models.URLField(blank=True,
                                default='https://media.npr.org/assets/img/2022/08/25/trh_incognito_artwork_wide-98bd003daa0a817e661cb600cbdb44b26b0c718c-s1100-c50.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)


class Quotes(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
