from django.conf.urls import url
from django.views.generic import RedirectView
from .views import WordCloudView


urlpatterns = [
    url(r"^$", RedirectView.as_view(url="wordcloud")),
    url(r"^wordcloud$", WordCloudView.as_view(), name="wordcloud")
]
