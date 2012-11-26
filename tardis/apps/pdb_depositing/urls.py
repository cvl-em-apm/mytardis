# -*- coding: utf-8 -*-
#
"""
urls.py

.. moduleauthor:: Grischa Meyer <grischa.meyer@monash.edu>

"""
from django.conf.urls.defaults import patterns, include, url

pdb_depositing_urls = patterns(
    'tardis.apps.pdb_depositing',
    (r'^index/(?P<dataset_file_id>\d+)/$', 'viewer'),
)
