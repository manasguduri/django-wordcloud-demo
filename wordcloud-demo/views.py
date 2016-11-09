from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy


from grapeshot_signal import \
    SignalClient, rels, APIError, OverQuotaError

import logging

from requests.exceptions import ConnectionError

from dev_portal.models.api_account import assure_api_account_exists
from dev_portal.models.api_app import assure_account_app_list

from .forms import WordcloudForm

logger = logging.getLogger("gs_dev_portal.wordcloud")


class DemoListView(TemplateView):
    template_name = "demos/index.html"


def remap(vals, low=10, high=30):
    """return a new list with an item corresponding to each element of
    `vals` such ratios are maintained and the new items fall between
    `low` and `high`.  The defaults are intended for use as font
    sizes.

    """
    if (not vals):
        return []
    if len(vals) == 1:
        return [high]
    min_val = min(vals)
    max_val = max(vals)
    val_range = (max_val - min_val)
    if val_range <= 0.0001:
        return [high] * len(vals)
    scale_factor = (high - low) / val_range
    return [(v - min_val) * scale_factor + low for v in vals]


class WordCloudView(FormView):
    template_name = "demos/wordcloud.html"
    form_class = WordcloudForm
    success_url = reverse_lazy("demos_wordcloud")

    def _get_api_token(self):
        # refactor - also used by swagger_ui view
        api_account = assure_api_account_exists(self.request.user)
        app = assure_account_app_list(api_account)[0]
        key = app.apikey_set.first()
        logger.debug("key is: {}".format(key.token()))
        return key.token()

    def form_valid(self, form, **kwargs):

        client = SignalClient(self._get_api_token())
        client.base_url = settings.OPEN_API_URL

        url = form['target_url'].value()

        try:
            page = client.get_page(url, rels.keywords)
            if not page.is_error() and not page.is_queued():
                keywords = page.get_embedded(rels.keywords)
            else:
                keywords = {}
        except (APIError, OverQuotaError, ConnectionError) as e:
            logger.debug("get_page exception: {}".format(e))
            raise

        keywords = keywords.get('keywords', [])  # shouldn't get_embedded do this?

        vals = [item['score'] for item in keywords]
        new_vals = remap(vals)
        logger.debug('************{}'.format(new_vals))
        remapped_keywords = [list(v) for v in
                             zip((item['name'] for item in keywords),
                                 new_vals)]

        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['keywords'] = remapped_keywords

        return render(self.request, self.template_name, context)
