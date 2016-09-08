import requests

from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
import logging

from dev_portal.models.api_account import assure_api_account_exists
from dev_portal.models.api_app import assure_account_app_list

from .forms import WordcloudForm

logger = logging.getLogger("demos")
logger.setLevel(logging.DEBUG)


class DemoListView(TemplateView):
    template_name = "demos/index.html"


def remap(vals, low=10, high=30):
    """return a new list with an item corresponding to each element of
    `vals` such ratios are maintained and the new items fall between `low` and `high`.
    """

    min_val = min(vals)
    max_val = max(vals)
    vals_range = max_val - min_val
    new_range = high - low
    return [((v - min_val) / vals_range) * new_range + low for v in vals]


class WordCloudView(FormView):
    template_name = "demos/wordcloud.html"
    form_class = WordcloudForm
    success_url = reverse_lazy("demos_wordcloud")

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        # refactor - also used by swagger_ui view
        api_account = assure_api_account_exists(self.request.user)
        app = assure_account_app_list(api_account)[0]
        key = app.apikey_set.first()
        token = key.token()

        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Accept': 'application/hal+json',
            #FIXME
            'X-Forwarded-Proto': 'https'
        }

        url = form['target_url'].value()

        params = {
            'url': url,
            'embed': 'keywords'
        }

        json = requests.get(
            "{}v1/pages".format(settings.OPEN_API_URL),
            params=params,
            headers=headers
        ).json()

        keyword_raw_data = json['_embedded']['grapeshot:keywords']['keywords']
        vals = [item['score'] for item in keyword_raw_data]
        new_vals = remap(vals)
        remapped_keywords = [list(v) for v in zip((item['name'] for item in keyword_raw_data), new_vals)]

        context['keywords'] = remapped_keywords
        context['json'] = json

        return render(self.request, self.template_name, context)
