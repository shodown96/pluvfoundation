from django.contrib import admin
from .models import *
# Register your models here.
class CatAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}
    list_display = ['title', 'slug']

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}
    list_display = ['title', 'slug', 'created', 'tag_list' ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}
    list_display = ['title', 'slug', 'created', 'tag_list' ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}
    list_display = ['title', 'slug', 'created', 'tag_list' ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

admin.site.register(Post, PostAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Image)
admin.site.register(Subscriber)
admin.site.register(Category, CatAdmin)


from django_cleanup import cleanup

def clean_files(*args, **kwargs):
    cleanup.refresh(Post)
    cleanup.refresh(Event)
cleanup.short_description = "Cleanup Files"

# admin.site.add_action(cleanup)