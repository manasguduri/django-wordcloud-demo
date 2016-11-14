from django.shortcuts import render
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from .forms import WordcloudForm


class WordCloudDemoView(FormView):
    '''A view to illustrate the use of the wordcloud '''

    template_name = "wordcloud_demo/wordcloud_form.html"
    form_class = WordcloudForm
    success_url = reverse_lazy("demos_wordcloud")

    def form_valid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form

        context['wordcloud_url'] = form['target_url'].value()

        return render(self.request, self.template_name, context)
