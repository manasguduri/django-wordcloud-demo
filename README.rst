=====================
Django Wordcloud Demo
=====================

Wordcloud demo is a simple Django app to illustrate making a wordcloud from a
url's keywords using the Grapeshot signal API. This demo makes use of the
`python signal sdk`_.


Quick Start
-----------

#. Add wordcloud_demo to INSTALLED_APPS::

     INSTALLED_APPS = [
       ...
       'wordcloud_demo',
     ]

#. Include the wordcloud demo URLconf in your project urls.py, e.g.::

     url(r'^wordcloud_demo/', include('wordcloud_demo.urls')

#. Obtain an API Key from the `Dev Portal`_.

#. Set the API Key in your settings.py::

     WORDCLOUD_DEMO_SETTINGS = {
       'signal_apikey': '<your api key here>'
       }

#. Restart your django development server and visit http://127.0.0.1:8000/wordcloud_demo.

.. _python signal sdk: https://github.com/grapeshot/grapeshot-signal-python
