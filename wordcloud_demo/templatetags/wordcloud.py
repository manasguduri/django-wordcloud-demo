from django import template
from django.conf import settings
from grapeshot_signal import \
    SignalClient, rels, APIError, OverQuotaError
from logging import getLogger
from requests import ConnectionError

logger = getLogger(__name__)

register = template.Library()


class WordCloudException(Exception):
    '''Class for exceptions raised by the wordcloud package
       Args:
         message - explanation of the error.
    '''
    def __init__(self, message):
        self.message = message


def remap(vals, low=10, high=30, tolerance=0.0001):
    """Scale `vals` to fit in the range `low`:`high`

    Args:
      vals: A list of numbers
      low: The bottom of the target range.
      high: The top of the target range.

    Returns:

      A generator for numbers corresponding to the elements of `vals` such that
      the smallest is `low`, the largest is `high` and each element is linearly
      interpolated into the target range.

      If the difference between the min and max in the inputs is less than
      `tolerance` returns [high]. Singleton input is a special case.

      The defaults are intended for use as font sizes.

    """
    if (not vals):
        return []
    min_val = min(vals)
    max_val = max(vals)
    val_range = (max_val - min_val)
    if val_range <= tolerance:
        return [high] * len(vals)
    scale_factor = (high - low) / val_range
    return ((v - min_val) * scale_factor + low for v in vals)


@register.inclusion_tag('wordcloud_demo/wordcloud.html')
def wordcloud(url, text_min_size=10, text_max_size=30,
              canvas_height=300, canvas_width=300, text_div=False,
              canvas_class="", keywords_class=""):
    '''A django inclusion tag to make a wordcloud canvas from a url's keywords

    Usage:
      In a django template put e.g.::

        {% load wordcloud %}
        {{ wordcloud "http://example.com"}}

    Args:
      url (string): The url of the webpage from which to extract keywords.
      text_min_size (int): Minimum font size for words in the wordcloud.
      text_max_size (int): Maximum font size for words in the wordcloud.
      canvas_height (int): Height of the canvas.
      canvas_width (int): Width of the canvas.
      text_div (boolean): If true create a div with id "wordcloud_keywords"
                containing a table of keyword/size pairs corresponding to the
                canvas text
      canvas_class (str): The class attribute for the canvas.
      keywords_class (str): The class attribute for the keywords div.

    '''

    apikey = settings.WORDCLOUD_DEMO_SETTINGS['signal_apikey']
    client = SignalClient(apikey)

    try:
        page = client.get_page(url, rels.keywords)
        if not page.is_error() and not page.is_queued():
            keywords = page.get_embedded(rels.keywords)
        else:
            keywords = {}
    except (APIError, OverQuotaError, ConnectionError) as e:
        logger.debug("get_page exception: {}".format(e))
        raise

    keywords = keywords.get('keywords', [])

    vals = [item['score'] for item in keywords]
    new_vals = remap(vals, text_min_size, text_max_size)
    remapped_keywords = [list(v) for v in
                         zip((item['name'] for item in keywords),
                             new_vals)]
    display_vals = zip((item['name'] for item in keywords),
                       ('{0:.2f}'.format(v) for v in vals))
    context = {
        'wordcloud_keywords': remapped_keywords,
        'wordcloud_canvas_width': canvas_width,
        'wordcloud_canvas_height': canvas_height,
        'text_div': text_div,
        'canvas_class': canvas_class,
        'keywords_class': keywords_class,
        'display_vals': display_vals
    }
    return context


# http://vanderwijk.info/blog/adding-css-classes-formfields-in-django-templates/
@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})
