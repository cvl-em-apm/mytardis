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
from tardis.tardis_portal.models.parameters import Schema
from tardis.tardis_portal.models.parameters import DatafileParameterSet
from tardis.tardis_portal.models.parameters import DatafileParameter
from tardis.tardis_portal.models.parameters import ParameterName

from tardis.apps.jolecule.settings import JOLECULE_VIEWS_SCHEMA
from tardis.apps.jolecule.settings import JOLECULE_VIEWS_PARNAME


def _get_create_schema(namespace):
    try:
        the_schema = Schema.objects.get(namespace=namespace)
    except Schema.DoesNotExist:
        the_schema = Schema(namespace=namespace, hidden=True)
        the_schema.save()
    return the_schema


def _get_create_dfps(namespace, dataset_file_id):
    schema = _get_create_schema(namespace)
    try:
        dfps = DatafileParameterSet.objects.get(
            schema=schema,
            dataset_file_id=dataset_file_id)
    except DatafileParameterSet.DoesNotExist:
        dfps = DatafileParameterSet(schema=schema,
                                    dataset_file_id=dataset_file_id)
        dfps.save()
    return dfps


def _get_create_pn(namespace, name):
    schema = _get_create_schema(namespace)
    try:
        pn = ParameterName.objects.get(schema=schema,
                                       name=name)
    except ParameterName.DoesNotExist:
        pn = ParameterName(schema=schema,
                           name=name,
                           full_name=name)
        pn.save()
    return pn


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


def _get_views(dataset_file_id):
    dfps = _get_create_dfps(JOLECULE_VIEWS_SCHEMA, dataset_file_id)
    pn = _get_create_pn(JOLECULE_VIEWS_SCHEMA, JOLECULE_VIEWS_PARNAME)
    views = DatafileParameter.objects.filter(parameterset=dfps,
                                             name=pn)
    return views


def loadViews(request, dataset_file_id):
    views = _get_views(dataset_file_id)
    returnstring = simplejson.dumps([simplejson.loads(view.get())
                                         for view in views])
    return HttpResponse(returnstring, mimetype='text/javascript')


def saveView(request, dataset_file_id):
    if request.method == "POST":
        newview = request.POST
        existing_views = _get_views(dataset_file_id)
        for view in existing_views:
            if newview["id"] == simplejson.loads(view.get())["id"]:
                view.delete()
        viewstring = simplejson.dumps(newview)
        dfps = _get_create_dfps(JOLECULE_VIEWS_SCHEMA, dataset_file_id)
        pn = _get_create_pn(JOLECULE_VIEWS_SCHEMA, JOLECULE_VIEWS_PARNAME)
        viewObj = DatafileParameter(parameterset=dfps,
                                    name=pn)
        viewObj.string_value = viewstring
        viewObj.save()
    return HttpResponse("")


def deleteView(request, dataset_file_id):
    """
    yes, it should use DELETE not POST in theory
    """
    if request.method == "POST":
        view_id = request.POST["pdb_id"]
        views = _get_views(dataset_file_id)
        for view in views:
            if simplejson.loads(view.get())["id"] == view_id:
                view.delete()

    return HttpResponse("")
