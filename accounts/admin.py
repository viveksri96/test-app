from django.contrib import admin
from accounts.models import User
# Register your models here.


class MyAdminArea(admin.AdminSite):
    site_header = 'Custom admin area'


my_admin_site = MyAdminArea(name='MyAdmin')

my_admin_site.register(User)