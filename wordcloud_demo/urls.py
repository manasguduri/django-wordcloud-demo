from django.conf.urls import url
from django.views.generic import RedirectView
from .views import wordcloud_demoview


urlpatterns = [
    url(r"wordcloud/?$", wordcloud_demoview, name="wordcloud")
]
