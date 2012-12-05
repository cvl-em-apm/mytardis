from django.forms import ModelForm
from django.template.loader import render_to_string
import django.forms as forms

from tardis.apps.pdb_depositing.models import PDBAuthorText
from tardis.apps.pdb_depositing.models import ContactAuthor
from tardis.apps.pdb_depositing.models import StructuralGenomics
from tardis.apps.pdb_depositing.models import StructureAuthor
from tardis.apps.pdb_depositing.models import CitationAuthor
from tardis.apps.pdb_depositing.models import CitationArticle
from tardis.apps.pdb_depositing.models import MoleculeName
from tardis.apps.pdb_depositing.models import MoleculeDetail
from tardis.apps.pdb_depositing.models import GMOSource
from tardis.apps.pdb_depositing.models import NaturalSource
from tardis.apps.pdb_depositing.models import SyntheticSource
from tardis.apps.pdb_depositing.models import Keyword
from tardis.apps.pdb_depositing.models import BiologicalAssembly
from tardis.apps.pdb_depositing.models import MethodAndCondition
from tardis.apps.pdb_depositing.models import RadiationSource


class SelectWithPop(forms.Select):
    def render(self, name, *args, **kwargs):
        html = super(SelectWithPop, self).render(name, *args, **kwargs)
        add_entry_plus = render_to_string("pdb_depositing/add_entry_plus.html",
                                          {'field': name})
        return html + add_entry_plus


class MultipleSelectWithPop(forms.SelectMultiple):
    def render(self, name, *args, **kwargs):
        html = super(MultipleSelectWithPop, self).render(name, *args, **kwargs)
        add_entry_plus = render_to_string("pdb_depositing/add_entry_plus.html",
                                          {'field': name})
        return html + add_entry_plus


class PDBAuthorTextForm(ModelForm):

    authors = forms.ModelMultipleChoiceField(
        ContactAuthor.objects,
        widget=MultipleSelectWithPop)
    structuralGenomics = forms.ModelMultipleChoiceField(
        StructuralGenomics.objects,
        widget=MultipleSelectWithPop)
    structuralGenomics = forms.ModelMultipleChoiceField(
        StructuralGenomics.objects, widget=MultipleSelectWithPop)
    structureAuthors = forms.ModelMultipleChoiceField(
        StructureAuthor.objects, widget=MultipleSelectWithPop)
    citationAuthors = forms.ModelMultipleChoiceField(
        CitationAuthor.objects, widget=MultipleSelectWithPop)
    citationArticles = forms.ModelMultipleChoiceField(
        CitationArticle.objects, widget=MultipleSelectWithPop)
    moleculeNames = forms.ModelMultipleChoiceField(
        MoleculeName.objects, widget=MultipleSelectWithPop)
    moleculeDetails = forms.ModelMultipleChoiceField(
        MoleculeDetail.objects, widget=MultipleSelectWithPop)
    gmoSources = forms.ModelMultipleChoiceField(
        GMOSource.objects, widget=MultipleSelectWithPop)
    naturalSources = forms.ModelMultipleChoiceField(
        NaturalSource.objects, widget=MultipleSelectWithPop)
    syntheticSources = forms.ModelMultipleChoiceField(
        SyntheticSource.objects, widget=MultipleSelectWithPop)
    keywords = forms.ModelMultipleChoiceField(
        Keyword.objects, widget=MultipleSelectWithPop)
    biologicalAssemblies = forms.ModelMultipleChoiceField(
        BiologicalAssembly.objects, widget=MultipleSelectWithPop)
    methodsAndConditions = forms.ModelMultipleChoiceField(
        MethodAndCondition.objects, widget=MultipleSelectWithPop)
    radiationSources = forms.ModelMultipleChoiceField(
        RadiationSource.objects, widget=MultipleSelectWithPop)

    class Meta:
        model = PDBAuthorText


class ContactAuthorForm(ModelForm):
    class Meta:
        model = ContactAuthor


class StructuralGenomicsForm(ModelForm):
    class Meta:
        model = StructuralGenomics


class StructureAuthorForm(ModelForm):
    class Meta:
        model = StructureAuthor


class CitationAuthorForm(ModelForm):
    class Meta:
        model = CitationAuthor


class CitationArticleForm(ModelForm):
    class Meta:
        model = CitationArticle


class MoleculeNameForm(ModelForm):
    class Meta:
        model = MoleculeName


class MoleculeDetailForm(ModelForm):
    class Meta:
        model = MoleculeDetail


class GMOSourceForm(ModelForm):
    class Meta:
        model = GMOSource


class NaturalSourceForm(ModelForm):
    class Meta:
        model = NaturalSource


class SyntheticSourceForm(ModelForm):
    class Meta:
        model = SyntheticSource


class KeywordForm(ModelForm):
    class Meta:
        model = Keyword


class BiologicalAssemblyForm(ModelForm):
    class Meta:
        model = BiologicalAssembly


class MethodAndConditionForm(ModelForm):
    class Meta:
        model = MethodAndCondition


class RadiationSourceForm(ModelForm):
    class Meta:
        model = RadiationSource
