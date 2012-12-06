# -*- coding: utf-8 -*-
#
"""
urls.py

.. moduleauthor:: Grischa Meyer <grischa.meyer@monash.edu>

"""

from django.http import HttpResponse
from django.template import Context
from django.utils import simplejson

from tardis.tardis_portal.shortcuts import render_response_index
from tardis.tardis_portal.models.datafile import Dataset_File

def view(request, dataset_file_id):
    context = Context({
        'dataset_file_id': dataset_file_id,
    })
    return HttpResponse(render_response_index(
        request,
        "jolecule/index.html",
        context))


def getFile(request, dataset_file_id):
    structureFile = Dataset_File.objects.get(id=dataset_file_id)
    with open(structureFile.get_absolute_filepath(), 'r') as diskFile:
        pdb_atom_lines = diskFile.readlines()
    protein_data = {'pdb_atom_lines': pdb_atom_lines,
                    'bond_pairs': [],
                }
    datastring = "protein_data = %s" % simplejson.dumps(protein_data)
    return HttpResponse(datastring,
                        mimetype='text/javascript')


def loadViews(request, dataset_file_id):
    emptyview = "var views = [];"
    return HttpResponse(emptyview, mimetype='text/javascript')


def saveView(request, dataset_file_id):
    return HttpResponse("")


def deleteView(request, dataset_file_id):
    """
    yes, it should use DELETE not POST in theory
    """
    return HttpResponse("")
