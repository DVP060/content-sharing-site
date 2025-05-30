from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.

class reader(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=60)
    password = models.TextField(blank=True,null=True)
    zip = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.name

class resource(models.Model):
    readerName = models.ForeignKey(reader,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='resource-img',null=True,blank=True)
    description = models.TextField()
    link = models.TextField(null=True,blank=True)
    resfile = models.FileField(upload_to='resource-file',blank=True,null=True)
    isPublished = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def admin_photo(self):
        return mark_safe("<img src='{}' height='100' width='100'".format(self.img.url))

    def admin_file(self):
        return mark_safe("<file src='{}'".format(self.resfile.url))

    admin_file.allow_tags = True
    admin_photo.allow_tags = True