from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConfigManagerConfig(AppConfig):

    name = 'configfactory.configmanager'
    verbose_name = _("Configuration manager")

    def ready(self):
        pass