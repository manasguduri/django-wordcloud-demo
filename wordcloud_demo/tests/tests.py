import django
from django.test.utils import get_runner
import unittest
from wordcloud_demo.templatetags import wordcloud
import random
from httmock import HTTMock
import urlmocks
from django.template import Template, Context
import sys
from django.conf import settings

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True
        }
    ],
    WORDCLOUD_DEMO_SETTINGS={
        'signal_apikey': 'not used for testing!'
    },
    ROOT_URLCONF='wordcloud_demo.urls',
    INSTALLED_APPS=('django.contrib.auth',
                    'django.contrib.contenttypes',
                    'django.contrib.sessions',
                    'django.contrib.admin',
                    'wordcloud_demo',))

django.setup()


class RemapTests(unittest.TestCase):

    def test_empty_returns_empty(self):
        res = wordcloud.remap([])
        self.assertEqual(list(res), [])

    def test_singleton(self):
        lo, hi = 10, 30

        res = wordcloud.remap([random.randint(-9999999, 999999)], lo, hi)
        self.assertEqual(list(res), [hi])

    def test_scaling_pair(self):
        tlo, thi = [10, 30]
        res = list(wordcloud.remap([1, 2], tlo, thi))
        self.assertEqual(res[0], tlo)
        self.assertEqual(res[1], thi)


class InclusionTagTests(unittest.TestCase):

    def test_tag_content_shows(self):
        template = Template(
            '''{% load wordcloud %}
            {% wordcloud "http://www.bbc.co.uk/news/world-middle-east-37298968" %}
            ''')
        with HTTMock(urlmocks.beeb_middle_east_kw):
            rendered = template.render(Context({}))
            self.assertIn('canvas', rendered)


if __name__ == '__main__':
    unittest.main()
    # TestRunner = get_runner(settings)
    # test_runner = TestRunner(verbosity=1, interactive=True)
    # failures = test_runner.run_tests(['wordcloud_demo'])
    # sys.exit(bool(failures))
