from libmproxyex import VERSION
from setuptools import setup, find_packages

deps = {'mitmproxy==0.13'}
scripts = {'mitmdumpex':set()}
console_scripts = ["%s = libmproxyex.main:%s" % (s, s) for s in scripts.keys()]

setup(
    name='mitmdumpex',
    version=VERSION,
    description='mitmdump with extended functionalities',
    author='isra17',
    author_email='isra017@gmail.com',
    packages=find_packages(),
    install_requires=list(deps),
    entry_points={'console_scripts': console_scripts},
)

