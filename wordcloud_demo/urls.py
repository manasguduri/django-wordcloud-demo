from django.conf.urls import url
from django.views.generic import RedirectView
from .views import WordCloudDemoView


urlpatterns = [
    url(r"$", RedirectView.as_view(url="wordcloud")),
    url(r"wordcloud/?$", WordCloudDemoView.as_view(), name="wordcloud")
]
