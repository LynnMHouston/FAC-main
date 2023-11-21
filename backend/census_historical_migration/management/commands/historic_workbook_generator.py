from census_historical_migration.workbooklib.workbook_builder import (
    generate_workbook,
)
from census_historical_migration.workbooklib.workbook_section_handlers import (
    sections_to_handlers,
)
from django.core.management.base import BaseCommand

import os
import sys
import json
import argparse
import pprint
import logging


pp = pprint.PrettyPrinter(indent=2)

parser = argparse.ArgumentParser()

logger = logging.getLogger(__name__)
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--output", type=str, required=True)
        parser.add_argument("--dbkey", type=str, required=True)
        parser.add_argument("--year", type=str, default="22")

    def handle(self, *args, **options):  # noqa: C901
        out_basedir = None
        if options["output"]:
            out_basedir = options["output"]
        else:
            out_basedir = "output"

        if not os.path.exists(out_basedir):
            try:
                os.mkdir(out_basedir)
                logger.info(f"Made directory {out_basedir}")
            except Exception as e:
                logger.info(e)
                logger.info(f"Could not create directory {out_basedir}")
                sys.exit()

        outdir = os.path.join(out_basedir, f'{options["dbkey"]}-{options["year"]}')

        if not os.path.exists(outdir):
            try:
                os.mkdir(outdir)
                logger.info(f"Made directory {outdir}")
            except Exception as e:
                logger.info(e)
                logger.info("could not create output directory. exiting.")
                sys.exit()

        json_test_tables = []
        for section, fun in sections_to_handlers.items():
            (wb, api_json, _, filename) = generate_workbook(
                fun, options["dbkey"], options["year"], section
            )
            if wb:
                wb_path = os.path.join(outdir, filename)
                wb.save(wb_path)
            if api_json:
                json_test_tables.append(api_json)

        json_path = os.path.join(outdir, f'test-array-{options["dbkey"]}.json')
        logger.info(f"Writing JSON to {json_path}")
        with open(json_path, "w") as test_file:
            jstr = json.dumps(json_test_tables, indent=2, sort_keys=True)
            test_file.write(jstr)
