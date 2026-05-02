from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import models


class PublisherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True, unique=True, max_length=260)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug

            count = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True, unique=True, max_length=260)
    intro = models.TextField(max_length=1000)
    cover = models.ImageField(upload_to='article/cover/')

    views = models.PositiveIntegerField(default=0)
    read_time = models.DurationField(blank=True, null=True)

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)

    published = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    pub_objects = PublisherManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.important:
            Article.objects.exclude(pk=self.pk).update(important=False)

        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug

            i = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{i}"
                i += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Context(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='article/context/', blank=True, null=True)

    def clean(self):
        if not self.text and not self.image:
            raise ValidationError("Iltimos rasm yoki matn kiriting!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    content = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:40]


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=15)
    subject = models.CharField(max_length=255)
    seen = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Newsletter(models.Model):
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email or "No email"


class Moment(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='moments')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)