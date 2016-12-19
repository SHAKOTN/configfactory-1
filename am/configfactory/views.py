from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from am.configfactory import backup
from am.configfactory.forms import (
    ComponentForm,
    ComponentSchemaForm,
    ComponentSettingsForm,
)
from am.configfactory.models import Component
from am.configfactory.utils import flatten_dict, sort_dict


def index(request):
    return render(request, 'index.html')


def component_create(request):

    if request.method == 'POST':

        form = ComponentForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(to=reverse('index'))
    else:
        form = ComponentForm()

    return render(request, 'components/create.html', {
        'form': form
    })


def component_edit(request, alias):

    component = get_object_or_404(Component, alias=alias)

    if request.method == 'POST':

        form = ComponentForm(data=request.POST, instance=component)

        if form.is_valid():
            form.save()
            messages.success(request, "Component successfully updated.")
            return redirect(to=reverse('components-view',
                                       kwargs={'alias': component.alias}))
    else:
        form = ComponentForm(instance=component)

    return render(request, 'components/edit.html', {
        'form': form,
        'component': component
    })


def component_edit_schema(request, alias):

    component = get_object_or_404(Component, alias=alias)
    schema = component.schema

    if request.method == 'POST':

        form = ComponentSchemaForm(data=request.POST, initial={
            'schema': schema
        })

        if form.is_valid():
            data = form.cleaned_data
            component.schema = data['schema']
            component.save()
            messages.success(request, "Component schema successfully updated.")
    else:
        form = ComponentSchemaForm(initial={
            'schema': schema
        })

    return render(request, 'components/edit_schema.html', {
        'form': form,
        'component': component
    })


def component_delete(request, alias):

    component = get_object_or_404(Component, alias=alias)

    if request.method == 'POST':
        component.delete()
        messages.success(request, "Component successfully deleted.")
        return redirect(to=reverse('index'))

    return render(request, 'components/delete.html', {
        'component': component
    })


def component_view(request, alias, environment=None):

    component = get_object_or_404(Component, alias=alias)
    environments = settings.ENVIRONMENTS

    try:
        readonly = int(request.GET.get('readonly', False))
    except TypeError:
        raise Http404

    if environment:
        settings_attr = 'settings_{}'.format(environment)
    else:
        settings_attr = 'settings'

    try:
        settings_val = getattr(component, settings_attr)
    except AttributeError:
        raise Http404

    if environment:
        settings_val = component.get_settings(environment)

    if readonly:
        settings_val = sort_dict(flatten_dict(settings_val))

    if request.method == 'POST':

        form = ComponentSettingsForm(
            require_schema=component.require_schema, schema=component.schema, data=request.POST,
            initial={
                'settings': settings_val
            })

        if form.is_valid():

            data = form.cleaned_data
            setattr(component, settings_attr, data['settings'])
            component.save()
            messages.success(
                request, "Component settings successfully updated.")
        else:
            messages.error(
                request,
                "Validation error.",
                extra_tags=' alert-danger')

    else:
        form = ComponentSettingsForm(
            require_schema=component.require_schema, schema=component.schema,
            initial={
                'settings': settings_val
            })

    return render(request, 'components/view.html', {
        'component': component,
        'environments': environments,
        'current_environment': environment,
        'form': form,
        'readonly': readonly
    })


def backup_dump(request):

    if request.method == 'POST':

        name = backup.dump()

        messages.success(
            request,
            'Settings successfully dumped as `{}`.'.format(name))
        return redirect(to=reverse('backup-load'))

    return render(request, 'backup/dump.html', {

    })


def backup_load(request, filename=None):

    if filename:

        if request.method == 'POST':
            backup.load(filename)
            messages.success(
                request, 'Backup `{}` successfully loaded.'.format(filename))
            return redirect(to=reverse('backup-load'))

        return render(request, 'backup/load_confirmation.html', {
            'filename': filename
        })

    backups = backup.get_all()

    return render(request, 'backup/load.html', {
        'backups': backups
    })


def backup_delete(request, filename):

    if not backup.exists(filename):
        raise Http404

    if request.method == 'POST':
        backup.delete(filename)
        messages.success(
            request,
            'Backup `{}` successfully deleted.'.format(filename))
        return redirect(to=reverse('backup-load'))

    return render(request, 'backup/delete.html', {

    })
