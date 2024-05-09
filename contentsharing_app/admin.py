from django.contrib import admin
import contentsharing_app.models as model

# Register your models here.

class ShowReaders(admin.ModelAdmin):
    list_display = ["name","email","password","zip","timestamp"]

admin.site.register(model.reader,ShowReaders)

class ShowResource(admin.ModelAdmin):
    list_display = ["readerName","title","description","link","isPublished","admin_photo","admin_file"]

admin.site.register(model.resource,ShowResource)
