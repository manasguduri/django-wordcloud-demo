import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-wordcloud-demo',
    version='0.0.a.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description="A Django wordcloud generation app using Grapeshot's Signal API.",
    long_description=README,
    url='https://github.com/grapeshot/django-wordcloud-demo',
    author='Paul Rudin',
    author_email='paul.rudin@grapeshot.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
