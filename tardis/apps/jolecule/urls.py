# -*- coding: utf-8 -*-
#
"""
urls.py

.. moduleauthor:: Grischa Meyer <grischa.meyer@monash.edu>

"""
from django.conf.urls.defaults import patterns, include, url

jolecule_urls = patterns(
    'tardis.apps.jolecule',
    (r'^viewer/(?P<dataset_file_id>\d+)/$', 'viewer'),
)
