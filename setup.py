from distutils.core import setup
from version import VERSION

setup(
    name='llamicron_weber',
    packages=['app'],
    py_modules=["version"],
    version=VERSION,
    description='A web interface for llamicron/brewer',
    author='Luke Sweeney',
    author_email='luke@thesweeneys.org',
    url='https://github.com/llamicron/weber',
    download_url="https://github.com/llamicron/weber/archive/%s.tar.gz" % VERSION,
    keywords=['beer', 'python', 'brewing', 'web', 'Flask', 'Vue.js'],
    classifiers=[],
)
