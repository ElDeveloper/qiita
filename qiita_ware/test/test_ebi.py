#!/usr/bin/env python

from __future__ import division

# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from unittest import TestCase, main
from xml.etree import ElementTree as ET
from xml.dom import minidom
import StringIO

from qiita_ware.ebi import (InvalidMetadataError, SampleAlreadyExistsError,
                            NoXMLError, EBISubmission)


class TestEBISubmission(TestCase):
    def test_init(self):
        e = EBISubmission('2', 'Study Title', 'Study Abstract', 'metagenome')

        self.assertEqual(e.study_id, '2')
        self.assertEqual(e.study_title, 'Study Title')
        self.assertEqual(e.study_abstract, 'Study Abstract')
        self.assertEqual(e.investigation_type, 'metagenome')

        self.assertEqual(e.empty_value, 'no_data')

        self.assertEqual(e.study_xml_fp, None)
        self.assertEqual(e.sample_xml_fp, None)
        self.assertEqual(e.experiment_xml_fp, None)
        self.assertEqual(e.run_xml_fp, None)

        self.assertEqual(e.library_strategy, 'POOLCLONE')
        self.assertEqual(e.library_source, 'METAGENOMIC')
        self.assertEqual(e.library_selection, 'unspecififed')

    def test__stringify_kwargs(self):
        # raise NotImplementedError()
        pass

    def test__get_study_alias(self):
        # raise NotImplementedError()
        pass

    def test__get_sample_alias(self):
        # raise NotImplementedError()
        pass

    def test__get_experiment_alias(self):
        # raise NotImplementedError()
        pass

    def test__get_submission_alias(self):
        # raise NotImplementedError()
        pass

    def test__get_library_name(self):
        # raise NotImplementedError()
        pass

    def test__add_dict_as_tags_and_values(self):
        # raise NotImplementedError()
        pass

    def test_generate_study_xml(self):
        submission = EBISubmission('001', 'teststudy', 'test asbstract',
                                   'metagenome')
        xmlelement = submission.generate_study_xml()
        xml = minidom.parseString(ET.tostring(xmlelement))
        xmlstring = xml.toprettyxml(indent='  ', encoding='UTF-8')
        self.assertEqual(xmlstring, STUDYXML)

    def test_add_sample(self):
        submission = EBISubmission('001', 'teststudy', 'test asbstract',
                                   'metagenome')
        submission.add_sample('test1')
        submission.add_sample('test2')
        samples = submission.samples
        self.assertTrue('test1' in samples and 'test2' in samples)
        with self.assertRaises(SampleAlreadyExistsError):
            submission.add_sample('test1')

    def test_generate_sample_xml(self):
        submission = EBISubmission('001', 'teststudy', 'test asbstract',
                                   'metagenome')
        submission.add_sample('test1')
        submission.add_sample('test2')
        xmlelement = submission.generate_sample_xml()
        xml = minidom.parseString(ET.tostring(xmlelement))
        xmlstring = xml.toprettyxml(indent='  ', encoding='UTF-8')
        self.assertEqual(xmlstring, SAMPLEXML)

    def test_add_sample_prep(self):
        submission = EBISubmission('001', 'teststudy', 'test asbstract',
                                   'metagenome')
        submission.add_sample('test1')
        submission.add_sample('test2')
        submission.add_sample_prep('test1', 'ILLUMINA', 'fastq',
                                   'fakepath', 'experiment description',
                                   'library protocol')
        prep_info = submission.samples['test1']['preps'][0]
        self.assertEqual(prep_info['platform'], 'ILLUMINA')
        self.assertEqual(prep_info['file_path'], 'fakepath')
        with self.assertRaises(KeyError):
            submission.add_sample_prep('test3', 'ILLUMINA', 'fastq',
                                       'fakepath', 'experiment description',
                                       'library protocol')

    def test__generate_library_descriptor(self):
        # raise NotImplementedError()
        pass

    def test__generate_spot_descriptor(self):
        # raise NotImplementedError()
        pass

    def test_generate_experiment_xml(self):
        submission = EBISubmission('001', 'teststudy', 'test asbstract',
                                   'metagenome')
        submission.add_sample('test1')
        submission.add_sample_prep('test1', 'ILLUMINA', 'fastq',
                                   'fakepath', 'experiment description',
                                   'library protocol')
        xmlelement = submission.generate_experiment_xml()
        xml = minidom.parseString(ET.tostring(xmlelement))
        xmlstring = xml.toprettyxml(indent='  ', encoding='UTF-8')
        self.assertEqual(xmlstring, EXPERIEMENTXML)

    def test_generate_run_xml(self):
        submission = EBISubmission('001', 'teststudy', 'test asbstract',
                                   'metagenome')
        submission.add_sample('test1')
        submission.add_sample_prep('test1', 'ILLUMINA', 'fastq',
                                   'fakepath', 'experiment description',
                                   'library protocol')
        xmlelement = submission.generate_run_xml()
        xml = minidom.parseString(ET.tostring(xmlelement))
        xmlstring = xml.toprettyxml(indent='  ', encoding='UTF-8')
        # waiting for checksum function to be done

    def test_generate_submission_xml(self):
        submission = EBISubmission('001', 'teststudy', 'test asbstract',
                                   'metagenome')
        submission.add_sample('test1')
        submission.add_sample_prep('test1', 'ILLUMINA', 'fastq',
                                   'fakepath', 'experiment description',
                                   'library protocol')
        with self.assertRaises(NoXMLError):
            xmlelement = submission.generate_submission_xml('VALIDATE')
        # add more tests

    def test__write_xml_file(self):
        # raise NotImplementedError()
        pass

    def test_write_study_xml(self):
        # raise NotImplementedError()
        pass

    def test_write_sample_xml(self):
        # raise NotImplementedError()
        pass

    def test_write_experiment_xml(self):
        # raise NotImplementedError()
        pass

    def test_write_run_xml(self):
        # raise NotImplementedError()
        pass

    def test_write_submission_xml(self):
        # raise NotImplementedError()
        pass

    def test_write_all_xml_files(self):
        # raise NotImplementedError()
        pass

    def test_add_samples_from_templates(self):

        # raise NotImplementedError()
        pass

    def test_from_templates_and_demux_fastq(self):
        # raise NotImplementedError()
        pass

    def test_from_templates_and_per_sample_fastqs(self):
        # raise NotImplementedError()
        pass


SAMPLEXML = """<?xml version="1.0" encoding="UTF-8"?>
<SAMPLE_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noName\
spaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.sample.xsd">
  <SAMPLE alias="qiime_study_001:test1" center_name="CCME-COLORADO">
    <TITLE>test1</TITLE>
    <SAMPLE_NAME>
      <TAXON_ID>no_data</TAXON_ID>
    </SAMPLE_NAME>
    <DESCRIPTION>no_data</DESCRIPTION>
  </SAMPLE>
  <SAMPLE alias="qiime_study_001:test2" center_name="CCME-COLORADO">
    <TITLE>test2</TITLE>
    <SAMPLE_NAME>
      <TAXON_ID>no_data</TAXON_ID>
    </SAMPLE_NAME>
    <DESCRIPTION>no_data</DESCRIPTION>
  </SAMPLE>
</SAMPLE_SET>
"""

STUDYXML = """<?xml version="1.0" encoding="UTF-8"?>
<STUDY_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noName\
spaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.study.xsd">
  <STUDY alias="qiime_study_001" center_name="CCME-COLORADO">
    <DESCRIPTOR>
      <STUDY_TITLE>teststudy</STUDY_TITLE>
      <STUDY_TYPE existing_study_type="metagenome"/>
      <STUDY_ABSTRACT>test asbstract</STUDY_ABSTRACT>
    </DESCRIPTOR>
  </STUDY>
</STUDY_SET>
"""

EXPERIEMENTXML = """<?xml version="1.0" encoding="UTF-8"?>
<EXPERIMENT_SET xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:no\
NamespaceSchemaLocation="ftp://ftp.sra.ebi.ac.uk/meta/xsd/sra_1_3/SRA.\
experiment.xsd">
  <EXPERIMENT alias="qiime_study_001:test1:0" center_name="CCME-COLORADO">
    <TITLE>qiime_study_001:test1:0</TITLE>
    <STUDY_REF refname="qiime_study_001"/>
    <DESIGN>
      <DESIGN_DESCRIPTION>experiment description</DESIGN_DESCRIPTION>
      <SAMPLE_DESCRIPTOR refname="qiime_study_001:test1"/>
      <LIBRARY_DESCRIPTOR>
        <LIBRARY_NAME>test1:0</LIBRARY_NAME>
        <LIBRARY_STRATEGY>POOLCLONE</LIBRARY_STRATEGY>
        <LIBRARY_SOURCE>METAGENOMIC</LIBRARY_SOURCE>
        <LIBRARY_SELECTION>unspecififed</LIBRARY_SELECTION>
        <LIBRARY_LAYOUT>
          <SINGLE/>
        </LIBRARY_LAYOUT>
        <LIBRARY_CONSTRUCTION_PROTOCOL>library protocol</LIBRARY_CONSTRUCTION\
_PROTOCOL>
      </LIBRARY_DESCRIPTOR>
    </DESIGN>
    <PLATFORM>
      <ILLUMINA>
        <INSTRUMENT_MODEL>unspecified</INSTRUMENT_MODEL>
      </ILLUMINA>
    </PLATFORM>
    <EXPERIMENT_ATTRIBUTES>
      <EXPERIMENT_ATTRIBUTE>
        <TAG>experiment_design_description</TAG>
        <VALUE>experiment description</VALUE>
      </EXPERIMENT_ATTRIBUTE>
      <EXPERIMENT_ATTRIBUTE>
        <TAG>file_path</TAG>
        <VALUE>fakepath</VALUE>
      </EXPERIMENT_ATTRIBUTE>
      <EXPERIMENT_ATTRIBUTE>
        <TAG>file_type</TAG>
        <VALUE>fastq</VALUE>
      </EXPERIMENT_ATTRIBUTE>
      <EXPERIMENT_ATTRIBUTE>
        <TAG>library_construction_protocol</TAG>
        <VALUE>library protocol</VALUE>
      </EXPERIMENT_ATTRIBUTE>
      <EXPERIMENT_ATTRIBUTE>
        <TAG>platform</TAG>
        <VALUE>ILLUMINA</VALUE>
      </EXPERIMENT_ATTRIBUTE>
    </EXPERIMENT_ATTRIBUTES>
  </EXPERIMENT>
</EXPERIMENT_SET>
"""

EXP_SAMPLE_TEMPLATE = (
    "#SampleID\tcollection_timestamp\tdescription\thas_extracted_data\t"
    "has_physical_specimen\thost_subject_id\tlatitude\tlongitude\t"
    "physical_location\trequired_sample_info_status_id\tsample_type\t"
    "str_column\n"
    "Sample1\t2014-05-29 12:24:51\tTest Sample 1\tTrue\tTrue\tNotIdentified\t"
    "42.42\t41.41\tlocation1\t1\ttype1\tValue for sample 1\n"
    "Sample2\t2014-05-29 12:24:51\t"
    "Test Sample 2\tTrue\tTrue\tNotIdentified\t4.2\t1.1\tlocation1\t1\t"
    "type1\tValue for sample 2\n"
    "Sample3\t2014-05-29 12:24:51\tTest Sample 3\tTrue\t"
    "True\tNotIdentified\t4.8\t4.41\tlocation1\t1\ttype1\t"
    "Value for sample 3\n")

EXP_PREP_TEMPLATE = (
    "#SampleID\tcenter_name\tcenter_project_name\tdata_type_id\t"
    "ebi_study_accession\tebi_submission_accession\temp_status_id\tstr_column"
    "\nSKB7.640196\tANL\tTest Project\t2\tNone\tNone\t1\tValue for sample 3\n"
    "SKB8.640193\tANL\tTest Project\t2\tNone\tNone\t1\tValue for sample 1\n"
    "SKD8.640184\tANL\tTest Project\t2\tNone\tNone\t1\tValue for sample 2\n")

if __name__ == "__main__":
    main()