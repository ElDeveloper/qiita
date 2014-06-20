# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from dateutil.parser import parse
import pandas as pd
from functools import partial
try:
    # Python 2
    from ConfigParser import ConfigParser
except ImportError:
    # Python 3
    from configparser import ConfigParser

from .study import Study, StudyPerson
from .user import User
from .util import get_filetypes, get_filepath_types
from .data import RawData, PreprocessedData, ProcessedData
from .metadata_template import SampleTemplate


def make_study_from_cmd(owner, title, info):

    # Parse the configuration file
    config = ConfigParser()
    config.readfp(info)

    optional = dict(config.items('optional'))
    get_optional = lambda name: optional.get(name, None)
    get_required = partial(config.get, 'required')
    required_fields = ['timeseries_type_id', 'mixs_compliant',
                       'number_samples_collected', 'number_samples_promised',
                       'portal_type_id', 'reprocess', 'study_alias',
                       'study_description', 'study_abstract',
                       'metadata_complete']
    optional_fields = ['funding', 'most_recent_contact', 'spatial_series',
                       'vamps_id']
    infodict = {}
    for value in required_fields:
        infodict[value] = get_required(value)

    for value in optional_fields:
        optvalue = get_optional(value)
        if optvalue is not None:
            infodict[value] = optvalue

    emp_person_name_email = get_optional('emp_person_name')
    if emp_person_name_email is not None:
        emp_name, emp_email = emp_person_name_email.split(',')
        infodict['emp_person_id'] = StudyPerson.create(emp_name.strip(),
                                                       emp_email.strip())
    lab_name_email = get_optional('lab_person')
    if lab_name_email is not None:
        lab_name, lab_email = lab_name_email.split(',')
        infodict['lab_person_id'] = StudyPerson.create(lab_name.strip(),
                                                       lab_email.strip())
    pi_name_email = get_required('principal_investigator')
    pi_name, pi_email = pi_name_email.split(',')
    infodict['principal_investigator_id'] = StudyPerson.create(
        pi_name.strip(), pi_email.strip())
    # this will eventually change to using the Experimental Factory Ontolgoy
    # names
    efo_ids = get_required('efo_ids')
    efo_ids = [x.strip() for x in efo_ids.split(',')]

    Study.create(User(owner), title, efo_ids, infodict)


def sample_template_adder(sample_temp_path, study_id):
    r"""Adds a sample template to the database

    Parameters
    ----------
    sample_temp_path : str
        Path to the sample template file
    study_id : int
        The study id to wich the sample template belongs to
    """
    sample_temp = pd.DataFrame.from_csv(sample_temp_path, sep='\t',
                                        infer_datetime_format=True)
    return SampleTemplate.create(sample_temp, Study(study_id))


def load_raw_data_cmd(filepaths, filepath_types, filetype, study_ids):
    """Add new raw data by populating the relevant tables

    Parameters
    ----------
    filepaths : iterable of str
    filepath_types : iterable of str
    filetype : str
    study_ids : iterable of int
    """
    if len(filepaths) != len(filepath_types):
        raise ValueError("Please pass exactly one filepath_type for each "
                         "and every filepath")

    filetypes_dict = get_filetypes()
    filetype_id = filetypes_dict[filetype]

    filepath_types_dict = get_filepath_types()
    filepath_types = [filepath_types_dict[x] for x in filepath_types]

    studies = [Study(x) for x in study_ids]

    return RawData.create(filetype_id, list(zip(filepaths, filepath_types)),
                          studies)


def load_processed_data_cmd(fps, fp_types, processed_params_table_name,
                            processed_params_id, preprocessed_data_id=None,
                            processed_date=None):
    """Add a new processed data entry

    Parameters
    ----------
    fps : list of str
        Paths to the processed data files to associate with the ProcessedData
        object
    fp_types: list of str
        The types of files, one per fp
    processed_params_table_name : str
        The name of the processed_params_ table to use
    processed_params_id : int
        The ID of the row in the processed_params_ table
    preprocessed_data_id : int, optional
        Defaults to ``None``. The ID of the row in the preprocessed_data table.
    processed_date : str, optional
        Defaults to ``None``. The date and time to use as the processing date.
        Must be interpretable as a datetime object

    Returns
    -------
    qiita_db.ProcessedData
        The newly created `qiita_db.ProcessedData` object
    """
    if len(fps) != len(fp_types):
        raise ValueError("Please pass exactly one fp_type for each "
                         "and every fp")

    fp_types_dict = get_filepath_types()
    fp_types = [fp_types_dict[x] for x in fp_types]

    if preprocessed_data_id is not None:
        preprocessed_data = PreprocessedData(preprocessed_data_id)
    else:
        preprocessed_data = None

    if processed_date is not None:
        processed_date = parse(processed_date)

    return ProcessedData.create(processed_params_table_name,
                                processed_params_id, list(zip(fps, fp_types)),
                                preprocessed_data, processed_date)