"""
Download data from https://facdissem.census.gov/PublicDataDownloads.aspx
Then unzip the files and place the them in data_distro/data_to_load/

Load them with: manage.py public_data_loader
"""
from pandas import read_csv
import logging

from django.core.management.base import BaseCommand

from data_distro.management.commands.process_data import (
    transform_and_save,
    transform_and_save_w_exceptions,
)
from data_distro.management.commands.handle_errors import log_results
from data_distro.management.commands.link_data import (
    link_objects_findings,
    link_objects_cpas,
    link_objects_general,
    add_duns,
)


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
        Loads data from public download files into Django models. Add the data to "/backend/data_distro/data_to_load". \
        If you just want one file, you can pass the name of the file with -f.

        Requires pandas.

        See docs/data_loaing.md for more details.
    """

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="file name")

    def handle(self, *args, **kwargs):
        """
        1) Find the files for upload
        2) Grab just the files we want
        3) Load data into Django models
        4) Add DUNS relationships
        """
        if kwargs["file"] is not None:
            load_file_names = [kwargs["file"]]
            if "duns" in load_file_names:
                add_duns()
            else:
                exceptions_list = load_files(load_file_names)

        else:
            # Dependent objects are created first
            load_file_names = [
                "findingstext_formatted.txt",  # 12 errors, no text
                "findings.txt",  # 10 errors, no finding ref num
                "captext_formatted.txt",  # 19 errors no text
                "cfda.txt",
                "notes.txt",  # 64 content, probably should migrate
                "revisions.txt",
                "agency.txt",
                "passthrough.txt",
                "gen.txt",
                "cpas.txt",
            ]

            exceptions_list = load_files(load_file_names)
            # Doesn't seem to be multiple eins, but need to confirm
            add_duns()

        log_results(exceptions_list)


def load_files(load_file_names):
    """Load files into django models"""

    for file in load_file_names:
        exceptions_list = []

        file_path = f"data_distro/data_to_load/{file}"
        file_name = file_path.replace("data_distro/data_to_load/", "")
        # Remove numbers, there are years in the file names, remove file extension
        table = "".join([i for i in file_name if not i.isdigit()])[:-4]
        # Remove for testing
        table = table.replace("test_data/", "")
        logger.info(f"Starting to load {file_name}...")
        expected_object_count = 0

        for i, chunk in enumerate(
            read_csv(file_path, chunksize=35000, sep="|", encoding="mac-roman")
        ):
            csv_dict = chunk.to_dict(orient="records")
            expected_object_count += len(csv_dict)

            # Just to speed things up check things per table and not per row or element
            logger.info(f"------------Table: {table}--------------")
            if table not in ["gen", "general", "cpas"]:
                for row in csv_dict:
                    objects_dict, exceptions_list, = transform_and_save(
                        row,
                        csv_dict,
                        table,
                        file_path,
                        exceptions_list,
                    )
                    if table == "findings":
                        link_objects_findings(objects_dict)
            elif table == "cpas":
                for row in csv_dict:
                    objects_dict, exceptions_list, = transform_and_save_w_exceptions(
                        row,
                        csv_dict,
                        table,
                        file_path,
                        exceptions_list,
                    )
                    link_objects_cpas(objects_dict, row)
            else:
                # Some years the table is called gen and sometimes general
                for row in csv_dict:
                    objects_dict, exceptions_list, = transform_and_save_w_exceptions(
                        row,
                        csv_dict,
                        "gen",
                        file_path,
                        exceptions_list,
                    )
                    link_objects_general(objects_dict)

            logger.info("finished chunk")
        logger.info(f"Finished {file_name}, {expected_object_count} expected objects")

    return exceptions_list
