# -*- coding: utf-8 -*-
"""
models.py

.. moduleauthor:: Grischa Meyer <grischa.meyer@monash.edu>

"""

from django.db import models

from tardis.tardis_portal.models.datafile import Dataset_File


class PDBAuthorText(models.Model):
    """
================CATEGORY 3:   Release Status==============================
The release status for the coordinates, structure_factors, and sequence
   Status should be chosen from one of the following:
* for coordinate & structure_factor
  (RELEASE NOW, HOLD FOR PUBLICATION,  HOLD FOR 8 WEEKS,
   HOLD FOR 6 MONTHS, HOLD FOR 1 YEAR)
* for sequence (give either RELEASE NOW or HOLD FOR RELEASE)
================CATEGORY 4:   Title=======================================
Enter the title for the structure
Enter any additional features of this structure
that will not be included elsewhere in the deposition
"""
    dataset_file = models.ForeignKey(Dataset_File)
    authors = models.ManyToManyField("ContactAuthor")
    Release_status_for_coordinates = models.CharField(
        max_length=15,
        choices=(
            ("RELEASE NOW", "Release now"),
            ("HOLD FOR RELEASE", "Hold for release"),)
        )
    # (e.g. RELEASE NOW)
    Release_status_for_structure_factor = models.CharField(
        max_length=15,
        choices=(
            ("RELEASE NOW", "Release now"),
            ("HOLD FOR RELEASE", "Hold for release"),
        )
    )
    # (e.g. RELEASE NOW)
    Release_status_for_sequence = models.CharField(
        max_length=15,
        choices=(
            ("RELEASE_NOW", "Release now"),
            ("HOLD FOR RELEASE", "Hold for release"),
        )
    )
    # (only RELEASE NOW or HOLD FOR RELEASE)

    structure_title = models.CharField(max_length=80)
    # (e.g. Crystal Structure Analysis of the B-DNA)
    structure_details = models.TextField()

    structuralGenomics = models.ManyToManyField("StructuralGenomics")
    structureAuthors = models.ManyToManyField("StructureAuthor")
    citationAuthors = models.ManyToManyField("CitationAuthor")
    citationArticles = models.ManyToManyField("CitationArticle")
    moleculeNames = models.ManyToManyField("MoleculeName")
    moleculeDetails = models.ManyToManyField("MoleculeDetail")
    gmoSources = models.ManyToManyField("GMOSource")
    naturalSources = models.ManyToManyField("NaturalSource")
    syntheticSources = models.ManyToManyField("SyntheticSource")
    keywords = models.ManyToManyField("Keyword")
    biologicalAssemblies = models.ManyToManyField("BiologicalAssembly")
    methodsAndConditions = models.ManyToManyField("MethodAndCondition")
    radiationSources = models.ManyToManyField("RadiationSource")


class ContactAuthor(models.Model):
    """
================CATEGORY 1:   Contact Authors=============================
Annotation staff will correspond with all contact authors provided about
the deposition.
Note: PI information should be always given.
1.  Information about the Principal Investigator (PI).
2. Information about other contact authors
Additional contact authors can be added by duplicating this section and
increasing the ID number.
"""
    contact_author_id = models.IntegerField()
    contact_author_salutation = models.CharField(max_length=15, null=True,
                                                 blank=True)
    contact_author_first_name = models.CharField(max_length=30)
    contact_author_last_name = models.CharField(max_length=30)
    contact_author_middle_name = models.CharField(max_length=30, null=True,
                                                  blank=True)
    contact_author_role = models.CharField(max_length=40, null=True)
    contact_author_organization_type = models.CharField(max_length=40)
    contact_author_email = models.CharField(max_length=50)
    contact_author_address = models.CharField(max_length=40)
    contact_author_city = models.CharField(max_length=30)
    contact_author_State_or_Province = models.CharField(max_length=20)
    contact_author_Zip_Code = models.CharField(max_length=15)
    contact_author_Country = models.CharField(max_length=30)
    contact_author_fax_number = models.CharField(max_length=20, null=True)
    contact_author_phone_numer = models.CharField(max_length=20)
    PI_string = "_PI"

    class Meta:
        ordering = ["contact_author_last_name", "contact_author_first_name"]
    
    def __unicode__(self):
        """
        Formatting name with proper spacing and middle initial
        """
        test = lambda x: x if x != None and len(x) > 0 else ""
        pad = lambda x: x + " " if test(x) != "" else ""
        initial = lambda x: x[0] + " " if test(x) != "" else ""
        name = "%s%s%s%s" % (
            pad(self.contact_author_salutation),
            pad(self.contact_author_first_name),
            initial(self.contact_author_middle_name),
            test(self.contact_author_last_name)
            )
        return name


class StructuralGenomics(models.Model):
    """
================CATEGORY 2:   Structural Genomics=========================
For structures from the structural genomics projects.
Additional centers can be added by duplicating this section and increasing
the ID number.
"""
    SG_project_id = models.IntegerField()
    SG_project_name = models.CharField(max_length=60)
    full_name_of_SG_center = models.CharField(max_length=60)


class StructureAuthor(models.Model):
    """
================CATEGORY 5: Authors of Structure============================
Enter authors of the deposited structures (e.g. Surname, F.M.)
Additional authors can be added by duplicating this token.
"""
    structure_author_name = models.CharField(max_length=30)
    # !(e.g.  Surname, F.M.)


class CitationAuthor(models.Model):
    """
================CATEGORY 6:   Citation Authors============================
Enter author names for the publications associated with this deposition.

      The primary citation is the article in which the deposited coordinates
      were first reported. Other related citations may also be provided.

1. For the primary citation
2. For related citations  (if applicable)
"""
    citation_author_id = models.IntegerField()  # 0 for primary
    citation_author_name = models.CharField(max_length=30)


class CitationArticle(models.Model):
    """
================CATEGORY 7:   Citation Article============================
Enter citation article (journal, title, year, volume, page)
      If the citation has not yet been published, use 'To be published'
      for the category 'journal_abbrev' and leave pages and volume blank.
1. For primary citation
2. For other related citation (if applicable)
Additional citations can be added by duplicating section 2 and increasing
the citation_id number. ID number should correspond to the ID of the
citation authors given.
"""
    citation_id = models.IntegerField()  # 0 for primary
    # same as id for citation authors
    citation_journal_abbrev = models.CharField(max_length=20)
    citation_title = models.CharField(max_length=80)
    citation_year = models.CharField(max_length=5)
    citation_journal_volume = models.CharField(max_length=8)
    citation_page_first = models.CharField(max_length=8)
    citation_page_last = models.CharField(max_length=8)


class MoleculeName(models.Model):
    """
================CATEGORY 8:   Molecule Names==============================
Enter the names of the molecules (entities) that are in the asymmetric unit
Additional names can be added by duplicating this token.
NOTE: Each chemically unique molecule is called an entity.
      The name of molecule should be obtained from the appropriate
      sequence database reference, if available. Otherwise the gene name or
      other common name of the entity may be used.
      e.g. HIV-1 integrase for protein
           RNA Hammerhead Ribozyme for RNA
"""
    molecule_name = models.CharField(max_length=60)


class MoleculeDetail(models.Model):
    """
================CATEGORY 9:   Molecule Details============================
Enter additional information about each entity, if known. (optional)
      Additional information would include details such as fragment name
      (if applicable), mutation, and E.C. number.
1. For entity 1
2. For entity 2
Additional molecule details can be added by duplicating section 2 and
increasing the ID number.
"""
    Molecular_entity_id = models.ForeignKey(MoleculeName)
    Fragment_name = models.CharField(max_length=60)
    Specific_mutation = models.CharField(max_length=80)
    Enzyme_Comission_number = models.CharField(max_length=20)


class GMOSource(models.Model):
    """
================CATEGORY 10:   Genetically Manipulated Source=============
Enter data in the genetically manipulated source category
      If the biomolecule has been genetically manipulated, describe its
      source and expression system here.
1. For entity 1
2. For entity 2
Additional information can be added by duplicating section 2 and increasing
the ID number.
"""
    Manipulated_entity_id = models.IntegerField()
    Source_organism_scientific_name = models.CharField(max_length=60)
    Source_organism_gene = models.CharField(max_length=60)
    Source_organism_strain = models.CharField(max_length=60)
    Expression_system_scientific_name = models.CharField(max_length=60)
    Expression_system_strain = models.CharField(max_length=60)
    Expression_system_vector_type = models.CharField(max_length=60)
    Expression_system_plasmid_name = models.CharField(max_length=60)
    Manipulated_source_details = models.CharField(max_length=60)


class NaturalSource(models.Model):
    """
================CATEGORY 11:   Natural Source=============================
Enter data in the natural source category  (if applicable)
    If the biomolecule was derived from a natural source, describe it here.
1. For entity 1
2. For entity 2
Additional information can be added by duplicating section 2 and increasing
the ID number.
"""
    natural_source_entity_id = models.IntegerField()
    natural_source_scientific_name = models.CharField(max_length=60)
    natural_source_organism_strain = models.CharField(max_length=40)
    natural_source_details = models.CharField(max_length=80)


class SyntheticSource(models.Model):
    """
================CATEGORY 12:  Synthetic Source=============================
If the biomolecule has not been genetically manipulated or synthesized,
describe its source here.
1. For entity 1
2. For entity 2
Additional information can be added by duplicating section 2 and increasing
the ID number.
"""
    synthetic_source_entity_id = models.IntegerField()
    synthetic_source_description = models.TextField(null=True)


class Keyword(models.Model):
    """
================CATEGORY 13:   Keywords===================================
Enter a list of keywords that describe important features of the deposited
structure.
      For example, beta barrel, protein-DNA complex, double helix,
      hydrolase, structural genomics etc.
"""
    structure_keywords = None  # " ">   !(e.g. beta barrel)
    # TODO: many vars or one comma separated one?


class BiologicalAssembly(models.Model):
    """
================CATEGORY 14:   Biological Assembly========================
Enter data in the biological assembly category (if applicable)
      Biological assembly describes the functional unit(s) present in the
      structure. There may be part of a biological assembly, one or more
      than one biological assemblies in the asymmetric unit.
      Case 1
      * If the asymmetric unit is the same as the biological assembly
        nothing special needs to be noted here.
      Case 2
      * If the asymmetric unit does not contain a complete biological unit.
        Please provide symmetry operations including translations required
        to build the biological unit.
        (example:
        The biological assembly is a hexamer generated from the dimer
        in the asymmetric unit by the operations:  -y, x-y-1, z-1 and
        -x+y, -x-1, z-l.)
      Case 3
      * If the asymmetric unit has multiple biological units
        Please specify how to group the contents of the asymmetric unit into
        biological units.
        (example:
        The biological unit is a dimer. There are 2 biological units in the
        asymmetric unit (chains A & B and chains C & D).
Additional information can be added by duplicating this token.
"""
    biological_assembly = models.TextField(
        default="biological unit is the same as asym.")


class MethodAndCondition(models.Model):
    """
================CATEGORY 15:   Methods and Conditions=====================
Enter the crystallization conditions for each crystal
1. For crystal 1:
Additional information can be added by duplicating this section and increasing
the ID number.
"""
    crystal_number = models.IntegerField()
    crystallization_method = models.CharField(max_length=50)
    crystallization_pH = models.CharField(max_length=10)
    crystallization_temperature = models.CharField(max_length=5)
    crystallization_details = models.CharField(max_length=80)


class RadiationSource(models.Model):
    """
================CATEGORY 16:   Radiation Source (experiment)============
Enter the details of the source of radiation, the X-ray generator,
and the wavelength for each diffraction.
1. For experiment 1:
2. For experiment 2:
Additional information can be added by duplicating this section and increasing
the ID number.
"""
    radiation_experiment = models.IntegerField()
    radiation_source = models.CharField(max_length=40)
    radiation_source_type = models.CharField(max_length=80)
    radiation_wavelengths = models.CharField(max_length=10)
    radiation_detector = models.CharField(max_length=80)
    radiation_detector_type = models.CharField(max_length=80)
    radiation_detector_details = models.CharField(max_length=80)
    data_collection_date = models.DateField()
    data_collection_temperature = models.CharField(max_length=10)
    data_collection_protocol = models.CharField(max_length=80)
    data_collection_monochromator = models.CharField(max_length=80)
