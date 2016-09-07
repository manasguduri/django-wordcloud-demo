from django.conf.urls import url
from django.views.generic import RedirectView
from .views import DemoListView, WordCloudView


urlpatterns = [
    url(r"^$", RedirectView.as_view(url="index") ),
    url(r"^index/?$", DemoListView.as_view(), name="demos_index"),
    url(r"^wordcloud/?$", WordCloudView.as_view(), name="demos_wordcloud")
]

