from httmock import urlmatch
import os


def load_data_file(filename):
    fi = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename
        )
    with open(fi) as f:
        return f.read()


@urlmatch(path='/v1/pages',
          query='.*news.bbc.co.uk/news/world-middle-east-37298968.*')
def beeb_middle_east_kw(url, request):
    return load_data_file('beeb_middle_east_page.txt')
