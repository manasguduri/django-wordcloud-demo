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

#. Obtain an API Key from the `Dev Portal`_.

#. Set the API Key in your settings.py::

     WORDCLOUD_DEMO_SETTINGS = {
       'signal_apikey': '<your api key here>'
       }

#. In your templates include wordcloud::

     {% load wordcloud %}

   And use the wordcloud tag to generate a wordcloud for a url::

     {% wordcloud "http://www.example.com" %}


#. Restart your django development server and visit http://127.0.0.1:8000/wordcloud_demo.



Wordcloud inclusion tag
-----------------------


The wordcloud tag takes a url and generates an html canvas element with
keywords derived from the text of the web page at that url. The relative size
of the words on the canvas indicates their relative importance in the web page.
Optionally the tag also generates a table of keyword/score pairs. The `url` is
the only mandatory argument, the remaining arguments are optional and their
effects are described below. We use a `third party script`_ to draw the words
on the canvas.

The inclusion tag generates a div with id `wordcloud_tag`. This div contains a
canvas element with id `wordcloud_canvas` and optionally a div with id
`wordcloud_keywords` containing a table of keyword/size pairs.

url
~~~

The url used to generate keywords for the wordcloud.

text_min_size, text_max_size
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The minimum and maximum font sizes for text on the canvas.


canvas_height, canvas_width
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The height and width of the canvas.

text_div
~~~~~~~~

If True generate a div containing a table of keyword/score pairs.

canvas_class, keywords_class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Strings used for the class attribute of the canvas and keywords elements.


Demo form
---------

There is a simple form to illustrate submitting a url and then rendering a
wordcloud. This can be see by including the following in your url
configuration::

     url(r'^wordcloud_demo/', include('wordcloud_demo.urls')


.. _python signal sdk: https://github.com/grapeshot/grapeshot-signal-python
.. _third party script: http://timdream.org/wordcloud2.js/
