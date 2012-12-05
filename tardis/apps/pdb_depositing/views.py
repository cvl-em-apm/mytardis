import django.forms as forms
from django.template import Context
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.utils.html import escape
from django.shortcuts import render_to_response

from tardis.tardis_portal.auth import decorators as authz
from tardis.tardis_portal.shortcuts import render_response_index

import tardis.apps.pdb_depositing.forms as app_forms


@never_cache
@authz.datafile_access_required
def view(request, dataset_file_id):
    form = app_forms.PDBAuthorTextForm()
    context = Context({"form": form})
    return HttpResponse(render_response_index(
        request,
        "pdb_depositing/index.html",
        context))


def handlePopupAdd(request, dataset_file_id, addForm, field):
    if request.method == "POST":
        form = addForm(request.POST)
        if form.is_valid():
            try:
                newObject = form.save()
            except forms.ValidationError, error:
                newObject = None
            if newObject:
                return HttpResponse(
                    '<script type="text/javascript">' +
                    'opener.dismissAddAnotherPopup(window, "%s", "%s");' +
                    '</script>' % (escape(newObject._get_pk_val()),
                                   escape(newObject)))
    else:
        form = addForm()
    pageContext = {'form': form, 'field': field,
                   'dataset_file_id': dataset_file_id}
    return render_to_response("pdb_depositing/add_entry_popup.html",
                              pageContext)


def add(request, dataset_file_id, fieldname):
    lookup_dict = {"authors": app_forms.ContactAuthorForm,
                   "structuralGenomics": app_forms.StructuralGenomicsForm,
                   "structureAuthors": app_forms.StructureAuthorForm,
                   "citationAuthors": app_forms.CitationAuthorForm,
                   "citationArticles": app_forms.CitationArticleForm,
                   "moleculeNames": app_forms.MoleculeNameForm,
                   "moleculeDetails": app_forms.MoleculeDetailForm,
                   "gmoSources": app_forms.GMOSourceForm,
                   "naturalSources": app_forms.NaturalSourceForm,
                   "syntheticSources": app_forms.SyntheticSourceForm,
                   "keywords": app_forms.KeywordForm,
                   "biologicalAssemblies": app_forms.BiologicalAbssemblyForm,
                   "methodsAndConditions": app_forms.MethodAndConditionForm,
                   "radiationSources": app_forms.RadiationSourceForm}
    form = lookup_dict[fieldname]()

    return handlePopupAdd(request, dataset_file_id, form, fieldname)
