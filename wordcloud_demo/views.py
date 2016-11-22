from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from .forms import WordcloudForm
from django.contrib import messages


def wordcloud_demoview(request):
    template = "wordcloud_demo/wordcloud_form.html"
    if request.method == 'POST':
        form = WordcloudForm(request.POST)
        if form.is_valid():
            context = {
                'form': form,
                'wordcloud_url': form['target_url'].value()
            }
            return render(request, template, context)
        else:
            messages.add_message(request, messages.ERROR,
                                 'Please enter an http or https url')
            return redirect(reverse_lazy('wordcloud'))
    else:
        form = WordcloudForm()
        return render(request, template, context={'form': form})
