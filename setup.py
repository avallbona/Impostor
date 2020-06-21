import codecs
import os
import re

from setuptools import setup, find_packages


def get_metadata(package, field):
    """
    Return package data as listed in `__{field}__` in `init.py`.
    """
    init_py = codecs.open(os.path.join(package, '__init__.py'), encoding='utf-8').read()
    return re.search("^__{}__ = ['\"]([^'\"]+)['\"]".format(field), init_py, re.MULTILINE).group(1)


def read(fname):
    """
    Read the README.md file

    :param fname:
    :return:
    """
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name="Impostor",
    version=get_metadata('impostor', 'version'),
    url='https://github.com/avallbona/Impostor/',
    author=get_metadata('impostor', 'author'),
    author_email=get_metadata('impostor', 'email'),
    maintainer=get_metadata('impostor', 'mantainer'),
    maintainer_email=get_metadata('impostor', 'mantainer_email'),
    description='Staff can login as a different user.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT License',
    platforms=['any'],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ],
    install_requires=[
        'Django>=1.11',
    ],
)
