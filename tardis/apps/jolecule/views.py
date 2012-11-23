# -*- coding: utf-8 -*-
#
"""
urls.py

.. moduleauthor:: Grischa Meyer <grischa.meyer@monash.edu>

"""

from django.http import HttpResponse
from django.template import Context

from tardis.tardis_portal.shortcuts import render_response_index


def viewer(request, dataset_file_id):
    context = Context({})
    return HttpResponse(render_response_index(
        request,
        "jolecule/viewer.html",
        context))
