from django import forms

from api.models import Client


class ClientForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        Client.objects.all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # if this is not a new object, we load related clients
            self.initial['clients'] = self.instance.clients.values_list('pk', flat=True)

    def save(self, *args, **kwargs):
        instance = super(ClientForm, self).save(*args, **kwargs)
        if instance.pk:
            for client in instance.clients.all():
                if client not in self.cleaned_data["clients"]:
                    # we remove clients which have been unselected
                    instance.clients.remove(client)
            for client in self.cleaned_data["clients"]:
                if client not in instance.clients.all():
                    # we add newly selected clients
                    instance.clients.add(client)
        return instance
