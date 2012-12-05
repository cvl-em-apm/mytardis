# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Release_status_for_coordinates', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('Release_status_for_structure_factor', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('Release_status_for_sequence', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('structure_title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('structure_details', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('pdb_depositing', ['PDBAuthorText'])

        # Adding M2M table for field authors on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('contactauthor', models.ForeignKey(orm['pdb_depositing.contactauthor'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_authors', ['pdbauthortext_id', 'contactauthor_id'])

        # Adding M2M table for field structuralGenomics on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_structuralGenomics', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('structuralgenomics', models.ForeignKey(orm['pdb_depositing.structuralgenomics'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_structuralGenomics', ['pdbauthortext_id', 'structuralgenomics_id'])

        # Adding M2M table for field structureAuthors on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_structureAuthors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('structureauthor', models.ForeignKey(orm['pdb_depositing.structureauthor'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_structureAuthors', ['pdbauthortext_id', 'structureauthor_id'])

        # Adding M2M table for field citationAuthors on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_citationAuthors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('citationauthor', models.ForeignKey(orm['pdb_depositing.citationauthor'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_citationAuthors', ['pdbauthortext_id', 'citationauthor_id'])

        # Adding M2M table for field citationArticles on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_citationArticles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('citationarticle', models.ForeignKey(orm['pdb_depositing.citationarticle'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_citationArticles', ['pdbauthortext_id', 'citationarticle_id'])

        # Adding M2M table for field moleculeNames on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_moleculeNames', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('moleculename', models.ForeignKey(orm['pdb_depositing.moleculename'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_moleculeNames', ['pdbauthortext_id', 'moleculename_id'])

        # Adding M2M table for field moleculeDetails on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_moleculeDetails', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('moleculedetail', models.ForeignKey(orm['pdb_depositing.moleculedetail'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_moleculeDetails', ['pdbauthortext_id', 'moleculedetail_id'])

        # Adding M2M table for field gmoSources on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_gmoSources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('gmosource', models.ForeignKey(orm['pdb_depositing.gmosource'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_gmoSources', ['pdbauthortext_id', 'gmosource_id'])

        # Adding M2M table for field naturalSources on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_naturalSources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('naturalsource', models.ForeignKey(orm['pdb_depositing.naturalsource'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_naturalSources', ['pdbauthortext_id', 'naturalsource_id'])

        # Adding M2M table for field syntheticSources on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_syntheticSources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('syntheticsource', models.ForeignKey(orm['pdb_depositing.syntheticsource'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_syntheticSources', ['pdbauthortext_id', 'syntheticsource_id'])

        # Adding M2M table for field keywords on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_keywords', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('keyword', models.ForeignKey(orm['pdb_depositing.keyword'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_keywords', ['pdbauthortext_id', 'keyword_id'])

        # Adding M2M table for field biologicalAssemblies on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_biologicalAssemblies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('biologicalassembly', models.ForeignKey(orm['pdb_depositing.biologicalassembly'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_biologicalAssemblies', ['pdbauthortext_id', 'biologicalassembly_id'])

        # Adding M2M table for field methodsAndConditions on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_methodsAndConditions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('methodandcondition', models.ForeignKey(orm['pdb_depositing.methodandcondition'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_methodsAndConditions', ['pdbauthortext_id', 'methodandcondition_id'])

        # Adding M2M table for field radiationSources on 'PDBAuthorText'
        db.create_table('pdb_depositing_pdbauthortext_radiationSources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdbauthortext', models.ForeignKey(orm['pdb_depositing.pdbauthortext'], null=False)),
            ('radiationsource', models.ForeignKey(orm['pdb_depositing.radiationsource'], null=False))
        ))
        db.create_unique('pdb_depositing_pdbauthortext_radiationSources', ['pdbauthortext_id', 'radiationsource_id'])

        # Adding model 'ContactAuthor'
        db.create_table('pdb_depositing_contactauthor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_author_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('contact_author_salutation', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('contact_author_first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('contact_author_last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('contact_author_middle_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('contact_author_role', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('contact_author_organization_type', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('contact_author_email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('contact_author_address', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('contact_author_city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('contact_author_State_or_Province', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('contact_author_Zip_Code', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('contact_author_Country', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('contact_author_fax_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('contact_author_phone_numer', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('pdb_depositing', ['ContactAuthor'])

        # Adding model 'StructuralGenomics'
        db.create_table('pdb_depositing_structuralgenomics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('SG_project_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('SG_project_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('full_name_of_SG_center', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('pdb_depositing', ['StructuralGenomics'])

        # Adding model 'StructureAuthor'
        db.create_table('pdb_depositing_structureauthor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('structure_author_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('pdb_depositing', ['StructureAuthor'])

        # Adding model 'CitationAuthor'
        db.create_table('pdb_depositing_citationauthor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('citation_author_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('citation_author_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('pdb_depositing', ['CitationAuthor'])

        # Adding model 'CitationArticle'
        db.create_table('pdb_depositing_citationarticle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('citation_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('citation_journal_abbrev', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('citation_title', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('citation_year', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('citation_journal_volume', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('citation_page_first', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('citation_page_last', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal('pdb_depositing', ['CitationArticle'])

        # Adding model 'MoleculeName'
        db.create_table('pdb_depositing_moleculename', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('molecule_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('pdb_depositing', ['MoleculeName'])

        # Adding model 'MoleculeDetail'
        db.create_table('pdb_depositing_moleculedetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Molecular_entity_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pdb_depositing.MoleculeName'])),
            ('Fragment_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('Specific_mutation', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('Enzyme_Comission_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('pdb_depositing', ['MoleculeDetail'])

        # Adding model 'GMOSource'
        db.create_table('pdb_depositing_gmosource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Manipulated_entity_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('Source_organism_scientific_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('Source_organism_gene', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('Source_organism_strain', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('Expression_system_scientific_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('Expression_system_strain', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('Expression_system_vector_type', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('Expression_system_plasmid_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('Manipulated_source_details', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal('pdb_depositing', ['GMOSource'])

        # Adding model 'NaturalSource'
        db.create_table('pdb_depositing_naturalsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('natural_source_entity_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('natural_source_scientific_name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('natural_source_organism_strain', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('natural_source_details', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('pdb_depositing', ['NaturalSource'])

        # Adding model 'SyntheticSource'
        db.create_table('pdb_depositing_syntheticsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('synthetic_source_entity_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('synthetic_source_description', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('pdb_depositing', ['SyntheticSource'])

        # Adding model 'Keyword'
        db.create_table('pdb_depositing_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('pdb_depositing', ['Keyword'])

        # Adding model 'BiologicalAssembly'
        db.create_table('pdb_depositing_biologicalassembly', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('biological_assembly', self.gf('django.db.models.fields.TextField')(default='biological unit is the same as asym.')),
        ))
        db.send_create_signal('pdb_depositing', ['BiologicalAssembly'])

        # Adding model 'MethodAndCondition'
        db.create_table('pdb_depositing_methodandcondition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('crystal_number', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('crystallization_method', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('crystallization_pH', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('crystallization_temperature', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('crystallization_details', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('pdb_depositing', ['MethodAndCondition'])

        # Adding model 'RadiationSource'
        db.create_table('pdb_depositing_radiationsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('radiation_experiment', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('radiation_source', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('radiation_source_type', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('radiation_wavelengths', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('radiation_detector', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('radiation_detector_type', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('radiation_detector_details', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('data_collection_date', self.gf('django.db.models.fields.DateField')()),
            ('data_collection_temperature', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('data_collection_protocol', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('data_collection_monochromator', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal('pdb_depositing', ['RadiationSource'])


    def backwards(self, orm):
        # Deleting model 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext')

        # Removing M2M table for field authors on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_authors')

        # Removing M2M table for field structuralGenomics on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_structuralGenomics')

        # Removing M2M table for field structureAuthors on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_structureAuthors')

        # Removing M2M table for field citationAuthors on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_citationAuthors')

        # Removing M2M table for field citationArticles on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_citationArticles')

        # Removing M2M table for field moleculeNames on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_moleculeNames')

        # Removing M2M table for field moleculeDetails on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_moleculeDetails')

        # Removing M2M table for field gmoSources on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_gmoSources')

        # Removing M2M table for field naturalSources on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_naturalSources')

        # Removing M2M table for field syntheticSources on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_syntheticSources')

        # Removing M2M table for field keywords on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_keywords')

        # Removing M2M table for field biologicalAssemblies on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_biologicalAssemblies')

        # Removing M2M table for field methodsAndConditions on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_methodsAndConditions')

        # Removing M2M table for field radiationSources on 'PDBAuthorText'
        db.delete_table('pdb_depositing_pdbauthortext_radiationSources')

        # Deleting model 'ContactAuthor'
        db.delete_table('pdb_depositing_contactauthor')

        # Deleting model 'StructuralGenomics'
        db.delete_table('pdb_depositing_structuralgenomics')

        # Deleting model 'StructureAuthor'
        db.delete_table('pdb_depositing_structureauthor')

        # Deleting model 'CitationAuthor'
        db.delete_table('pdb_depositing_citationauthor')

        # Deleting model 'CitationArticle'
        db.delete_table('pdb_depositing_citationarticle')

        # Deleting model 'MoleculeName'
        db.delete_table('pdb_depositing_moleculename')

        # Deleting model 'MoleculeDetail'
        db.delete_table('pdb_depositing_moleculedetail')

        # Deleting model 'GMOSource'
        db.delete_table('pdb_depositing_gmosource')

        # Deleting model 'NaturalSource'
        db.delete_table('pdb_depositing_naturalsource')

        # Deleting model 'SyntheticSource'
        db.delete_table('pdb_depositing_syntheticsource')

        # Deleting model 'Keyword'
        db.delete_table('pdb_depositing_keyword')

        # Deleting model 'BiologicalAssembly'
        db.delete_table('pdb_depositing_biologicalassembly')

        # Deleting model 'MethodAndCondition'
        db.delete_table('pdb_depositing_methodandcondition')

        # Deleting model 'RadiationSource'
        db.delete_table('pdb_depositing_radiationsource')


    models = {
        'pdb_depositing.biologicalassembly': {
            'Meta': {'object_name': 'BiologicalAssembly'},
            'biological_assembly': ('django.db.models.fields.TextField', [], {'default': "'biological unit is the same as asym.'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pdb_depositing.citationarticle': {
            'Meta': {'object_name': 'CitationArticle'},
            'citation_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'citation_journal_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'citation_journal_volume': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'citation_page_first': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'citation_page_last': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'citation_title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'citation_year': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pdb_depositing.citationauthor': {
            'Meta': {'object_name': 'CitationAuthor'},
            'citation_author_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'citation_author_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pdb_depositing.contactauthor': {
            'Meta': {'object_name': 'ContactAuthor'},
            'contact_author_Country': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'contact_author_State_or_Province': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'contact_author_Zip_Code': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'contact_author_address': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'contact_author_city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'contact_author_email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'contact_author_fax_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'contact_author_first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'contact_author_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'contact_author_last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'contact_author_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'contact_author_organization_type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'contact_author_phone_numer': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'contact_author_role': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'contact_author_salutation': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pdb_depositing.gmosource': {
            'Expression_system_plasmid_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'Expression_system_scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'Expression_system_strain': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'Expression_system_vector_type': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'Manipulated_entity_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'Manipulated_source_details': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'Meta': {'object_name': 'GMOSource'},
            'Source_organism_gene': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'Source_organism_scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'Source_organism_strain': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pdb_depositing.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pdb_depositing.methodandcondition': {
            'Meta': {'object_name': 'MethodAndCondition'},
            'crystal_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'crystallization_details': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'crystallization_method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'crystallization_pH': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'crystallization_temperature': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pdb_depositing.moleculedetail': {
            'Enzyme_Comission_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'Fragment_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'Meta': {'object_name': 'MoleculeDetail'},
            'Molecular_entity_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pdb_depositing.MoleculeName']"}),
            'Specific_mutation': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pdb_depositing.moleculename': {
            'Meta': {'object_name': 'MoleculeName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'molecule_name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'pdb_depositing.naturalsource': {
            'Meta': {'object_name': 'NaturalSource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'natural_source_details': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'natural_source_entity_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'natural_source_organism_strain': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'natural_source_scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'pdb_depositing.pdbauthortext': {
            'Meta': {'object_name': 'PDBAuthorText'},
            'Release_status_for_coordinates': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'Release_status_for_sequence': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'Release_status_for_structure_factor': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.ContactAuthor']", 'symmetrical': 'False'}),
            'biologicalAssemblies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.BiologicalAssembly']", 'symmetrical': 'False'}),
            'citationArticles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.CitationArticle']", 'symmetrical': 'False'}),
            'citationAuthors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.CitationAuthor']", 'symmetrical': 'False'}),
            'gmoSources': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.GMOSource']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.Keyword']", 'symmetrical': 'False'}),
            'methodsAndConditions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.MethodAndCondition']", 'symmetrical': 'False'}),
            'moleculeDetails': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.MoleculeDetail']", 'symmetrical': 'False'}),
            'moleculeNames': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.MoleculeName']", 'symmetrical': 'False'}),
            'naturalSources': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.NaturalSource']", 'symmetrical': 'False'}),
            'radiationSources': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.RadiationSource']", 'symmetrical': 'False'}),
            'structuralGenomics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.StructuralGenomics']", 'symmetrical': 'False'}),
            'structureAuthors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.StructureAuthor']", 'symmetrical': 'False'}),
            'structure_details': ('django.db.models.fields.TextField', [], {}),
            'structure_title': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'syntheticSources': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pdb_depositing.SyntheticSource']", 'symmetrical': 'False'})
        },
        'pdb_depositing.radiationsource': {
            'Meta': {'object_name': 'RadiationSource'},
            'data_collection_date': ('django.db.models.fields.DateField', [], {}),
            'data_collection_monochromator': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'data_collection_protocol': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'data_collection_temperature': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'radiation_detector': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'radiation_detector_details': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'radiation_detector_type': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'radiation_experiment': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'radiation_source': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'radiation_source_type': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'radiation_wavelengths': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'pdb_depositing.structuralgenomics': {
            'Meta': {'object_name': 'StructuralGenomics'},
            'SG_project_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'SG_project_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'full_name_of_SG_center': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pdb_depositing.structureauthor': {
            'Meta': {'object_name': 'StructureAuthor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'structure_author_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'pdb_depositing.syntheticsource': {
            'Meta': {'object_name': 'SyntheticSource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'synthetic_source_description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'synthetic_source_entity_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['pdb_depositing']