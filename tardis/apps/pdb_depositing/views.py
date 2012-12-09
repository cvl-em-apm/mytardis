import django.forms as forms
from django.template import Context
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.utils.html import escape
from django.shortcuts import render_to_response

from tardis.tardis_portal.auth import decorators as authz
from tardis.tardis_portal.shortcuts import render_response_index
from tardis.tardis_portal.models.datafile import Dataset_File


import tardis.apps.pdb_depositing.forms as app_forms


def _collect_data(dataset_file_id):

    def add_to_data(name, value, data, force_list=False):
        if name not in data:
            data[name] = [value] if force_list else value
        elif type(data[name]) == list:
            data[name].append(value)
        else:
            existing_value = data[name]
            data[name] = [existing_value, value]

    data = {}

    # data metadata
    datafile = Dataset_File.objects.get(id=dataset_file_id)
    dfpsets = datafile.datafileparameterset_set.all()
    for dfpset in dfpsets:
        for dfp in dfpset.datafileparameter_set.all():
            add_to_data(dfp.name.name, dfp.get(), data)
    dataset = datafile.dataset
    dspsets = dataset.datasetparameterset_set.all()
    for dspset in dspsets:
        for dsp in dspset.datasetparameter_set.all():
            add_to_data(dsp.name.name, dsp.get(), data)
    experiments = dataset.experiments.all()
    for experiment in experiments:
        epsets = experiment.experimentparameterset_set.all()
        for epset in epsets:
            for ep in epset.experimentparameter_set.all():
                add_to_data(ep.name.name, ep.get(), data)
        # owner data
        for owner in experiment.get_owners():
            owner = {"email": owner.email,
                     "first_name": owner.first_name,
                     "last_name": owner.last_name,
                 }
            add_to_data("contact_authors", owner, data, True)
        # authors data
        for author in experiment.author_experiment_set.all():
            split_author = author.author.strip().split()
            try:
                formatted_author = "%s, %s." % (
                    split_author[-1],
                    ".".join([n[0] for n in split_author[0:-1]])
                )
            except:
                formatted_author = author.author
            add_to_data("authors", formatted_author, data, True)
    return data


@never_cache
@authz.datafile_access_required
def view(request, dataset_file_id):
    prefill = _collect_data(dataset_file_id)
    author_infor = render_to_string("pdb_depositing/author-infor.text",
                                    prefill)
    print prefill.keys()
    context = Context({"dataset_file_id": dataset_file_id,
                       "author_infor": author_infor,
                   })
    return HttpResponse(render_response_index(
        request,
        "pdb_depositing/index.html",
        context))


def download(request, dataset_file_id):
    prefill = _collect_data(dataset_file_id)
    response = HttpResponse(
        render_to_string(
            "pdb_depositing/author-infor.text",
            prefill),
        content_type='text/plain'
    )
    response['Content-Disposition'] = 'attachment; filename="author-infor.text"'
    return response
    

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
                    'opener.dismissAddAnotherPopup(window, "%s", "%s");' %
                    (escape(newObject._get_pk_val()),
                                   escape(newObject))
                     + '</script>'
                )
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
                   "biologicalAssemblies": app_forms.BiologicalAssemblyForm,
                   "methodsAndConditions": app_forms.MethodAndConditionForm,
                   "radiationSources": app_forms.RadiationSourceForm}
    form = lookup_dict[fieldname]

    return handlePopupAdd(request, dataset_file_id, form, fieldname)
