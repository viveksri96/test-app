from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class MyAdminConfig(AdminConfig):
    default_site = 'accounts.admin.MyAdminArea'

class AccountsConfig(AppConfig):
    name = 'accounts'
