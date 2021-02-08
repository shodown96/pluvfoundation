from django.db import models
from django.shortcuts import reverse, redirect
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from ckeditor.fields import RichTextField
from .utils import image_resize

TYPES = (
    ('P', 'Post'),
    ('PR', 'Project')
)

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    cat_type = models.CharField(max_length=100, choices=TYPES)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("ngo:category", kwargs={"slug": self.slug})
    class Meta:
        verbose_name_plural = "Categories"

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    tags = TaggableManager()
    content = RichTextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    cover = models.ImageField(upload_to="posts/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("ngo:post", kwargs={"slug": self.slug})
    class Meta:
        ordering  = ['-created']
    
    def save(self, *args, **kwargs):
        image_resize(self.cover, 950,950)
        super().save(*args, **kwargs)
    

class Event(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    tags = TaggableManager()
    content = RichTextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    due_datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    embed_script = models.CharField(max_length=255, blank=True, null=True)
    cover = models.ImageField(upload_to="events/")

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("ngo:event", kwargs={"slug": self.slug})
    class Meta:
        ordering  = ['-due_datetime']

    def save(self, *args, **kwargs):
        image_resize(self.cover, 950,950)
        super().save(*args, **kwargs)


class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    tags = TaggableManager()
    content = RichTextField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    cover = models.ImageField(upload_to="projects/")
    raised = models.FloatField()
    goal = models.FloatField()

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("ngo:project", kwargs={"slug": self.slug})
    class Meta:
        ordering  = ['-created']

    def save(self, *args, **kwargs):
        image_resize(self.cover, 950,950)
        super().save(*args, **kwargs)

class Image(models.Model):
    name = models.CharField(max_length=100)
    source = models.ImageField()
    description = models.TextField()
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering  = ['-published']

    def save(self, *args, **kwargs):
        image_resize(self.source, 950,950)
        super().save(*args, **kwargs)

class Subscriber(models.Model):
    email = models.EmailField(max_length=254, unique=True)

# def post_reciever(sender, instance, created, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = instance.title.replace(' ', '-').strip("('')").lower()

# pre_save.connect(post_reciever, sender=User)
# def save(self, *args, **kwargs):
#     try:
#         this = MyModelName.objects.get(id=self.id)
#         if this.MyImageFieldName != self.MyImageFieldName:
#             this.MyImageFieldName.delete()
#     except: pass
#     super(MyModelName, self).save(*args, **kwargs)