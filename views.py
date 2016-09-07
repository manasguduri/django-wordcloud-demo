from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class DemoView(TemplateView):
    pass

class DemoListView(DemoView):
    template_name="demos/index.html"

class WordCloudView(DemoView):
    template_name="demos/wordcloud.html"
