from census_historical_migration.workbooklib.excel_creation_utils import (
    set_uei,
    set_range,
    map_simple_columns,
    generate_dissemination_test_table,
)
from census_historical_migration.base_field_maps import SheetFieldMap
from census_historical_migration.workbooklib.templates import sections_to_template_paths
from census_historical_migration.workbooklib.census_models.census import dynamic_import
from audit.fixtures.excel import FORM_SECTIONS

import openpyxl as pyxl

import re
import logging


logger = logging.getLogger(__name__)

mappings = [
    SheetFieldMap("note_title", "title", "title", None, str),
    SheetFieldMap("note_content", "content", "content", None, str),
]


def cleanup_string(s):
    if s is None:
        return ""
    else:
        s = s.rstrip()
        # s = unidecode.unidecode(s)
        s = str(s.encode("utf-8").decode("ascii", "ignore"))
        return s


def generate_notes_to_sefa(dbkey, year, outfile):
    logger.info(f"--- generate notes to sefa {dbkey} {year}---")
    Gen = dynamic_import("Gen", year)
    Notes = dynamic_import("Notes", year)
    wb = pyxl.load_workbook(sections_to_template_paths[FORM_SECTIONS.NOTES_TO_SEFA])

    g = set_uei(Gen, wb, dbkey)

    # The mapping is weird.
    # https://facdissem.census.gov/Documents/DataDownloadKey.xlsx
    # The TYPEID column determines which field in the form a given row corresponds to.
    # TYPEID=1 is the description of significant accounting policies.
    # TYPEID=2 is the De Minimis cost rate.
    # TYPEID=3 is for notes, which have sequence numbers... that must align somewhere.
    policies = (
        Notes.select().where((Notes.dbkey == g.dbkey) & (Notes.type_id == 1)).get()
    )
    rate = Notes.select().where((Notes.dbkey == g.dbkey) & (Notes.type_id == 2)).get()
    notes = (
        Notes.select()
        .where((Notes.dbkey == g.dbkey) & (Notes.type_id == 3))
        .order_by(Notes.seq_number)
    )

    rate_content = cleanup_string(rate.content)
    policies_content = cleanup_string(policies.content)

    if rate_content == "":
        rate_content = "FILLED FOR TESTING"
    if policies_content == "":
        policies_content = "FILLED FOR TESTING"

    # WARNING
    # This is being faked. We're askign a Y/N question in the collection.
    # Census just let them type some stuff. So, this is a rough
    # attempt to generate a Y/N value from the content.
    # This means the data is *not* true to what was intended, but
    # it *is* good enough for us to use for testing.
    is_used = "Huh"
    if (
        re.search("did not use", rate_content)
        or re.search("not to use", rate_content)
        or re.search("not use", rate_content)
        or re.search("not elected", rate_content)
    ):
        is_used = "N"
    elif re.search("used", rate_content):
        is_used = "Y"
    else:
        is_used = "Both"

    set_range(wb, "accounting_policies", [policies_content])
    set_range(wb, "is_minimis_rate_used", [is_used])
    set_range(wb, "rate_explained", [rate_content])

    # Map the rest as notes.
    map_simple_columns(wb, mappings, notes)
    # Add a Y/N column
    # def set_range(wb, range_name, values, default=None, conversion_fun=str):

    set_range(wb, "contains_chart_or_table", map(lambda v: "N", notes), "N", str)
    wb.save(outfile)

    table = generate_dissemination_test_table(
        Gen, "notes_to_sefa", dbkey, mappings, notes
    )

    table["singletons"]["accounting_policies"] = policies_content
    table["singletons"]["is_minimis_rate_used"] = is_used
    table["singletons"]["rate_explained"] = rate_content
    table["singletons"]["auditee_uei"] = g.uei

    return (wb, table)
