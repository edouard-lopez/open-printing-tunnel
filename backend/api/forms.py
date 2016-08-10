from django import forms

from api.models import Client


class CompanyForm(forms.ModelForm):
    companies = forms.ModelMultipleChoiceField(
        Client.objects.all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # if this is not a new object, we load related companies
            self.initial['companies'] = self.instance.companies.values_list('pk', flat=True)

    def save(self, *args, **kwargs):
        instance = super(CompanyForm, self).save(*args, **kwargs)
        if instance.pk:
            for company in instance.companies.all():
                if company not in self.cleaned_data["companies"]:
                    # we remove companies which have been unselected
                    instance.companies.remove(company)
            for company in self.cleaned_data["companies"]:
                if company not in instance.companies.all():
                    # we add newly selected companies
                    instance.companies.add(company)
        return instance
