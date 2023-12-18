from ..transforms.xform_string_to_bool import (
    string_to_bool,
)
from ..transforms.xform_string_to_string import (
    string_to_string,
)
from ..transforms.xform_string_to_int import string_to_int
from ..exception_utils import DataMigrationError
from ..base_field_maps import WorkbookFieldInDissem
from ..workbooklib.templates import sections_to_template_paths
from ..sac_general_lib.report_id_generator import (
    xform_dbkey_to_report_id,
)
from ..models import (
    ELECAUDITS as Audits,
    ELECAUDITHEADER as AuditHeader,
)

from openpyxl.utils.cell import (
    rows_from_range,
    coordinate_from_string,
    column_index_from_string,
)

import logging


logger = logging.getLogger(__name__)


def set_range(wb, range_name, values, default=None, conversion_fun=str):
    """
    Helper to set a range of values. Takes a named range, and then walks down
    the range, filling in the given values.

    wb (Workbook)       The workbook
    range_name (string) Name of the range to set
    values (iterable)   Values to set within the range
    default (any)       Default value to use; defaults to None.
    conversion (func)   Conversion function to apply to individual values; defaults to str().
    """
    the_range = wb.defined_names[range_name]
    dests = the_range.destinations

    sheet_title, coord = None, None
    for cur_sheet_title, cur_coord in dests:
        if sheet_title or coord:
            # `destinations` is meant to be iterated over, but we only expect one value
            raise ValueError(f"{range_name} has more than one destination")
        else:
            sheet_title, coord = cur_sheet_title, cur_coord

    ws = None
    try:
        ws = wb[sheet_title]
    except KeyError:
        raise KeyError(f"Sheet title '{sheet_title}' not found in workbook")

    values = list(values)
    for i, row in enumerate(rows_from_range(coord)):
        # Iterate over the rows, but stop when we run out of values
        value = None
        try:
            value = values[i]
        except IndexError:
            break

        # Get the row and column to set the current value
        cell = row[0]  # [('B12',)] -> ('B12',)
        col_str, row = coordinate_from_string(cell)  # ('B12',) -> 'B', 12
        col = column_index_from_string(col_str)  # 'B' -> 2

        # Check for the type and apply the correct conversion method
        converted_value = apply_conversion_function(value, default, conversion_fun)
        # Set the value of the cell
        ws.cell(row=row, column=col, value=converted_value)


def apply_conversion_function(value, default, conversion_function):
    """
    Helper to apply a conversion function to a value, or use a default value
    """
    if value is None and default is None:
        raise ValueError("No value or default provided")

    selected_value = value if value is not None else default

    if conversion_function is str:
        new_value = string_to_string(selected_value)
    elif conversion_function is int:
        new_value = string_to_int(selected_value)
    elif conversion_function is bool:
        new_value = string_to_bool(selected_value)
    else:
        new_value = conversion_function(selected_value)

    return new_value


def get_range_values(ranges, name):
    """
    Helper to get the values linked to a particular range, identified by its name."""
    for item in ranges:
        if item["name"] == name:
            return item["values"]
    return None


def get_ranges(mappings, values):
    """
    Helper to get range of values.The method iterates over a collection of mappings, applying a conversion
    function to constructs a list of dictionaries, each containing a name and a list of
    transformed values."""
    ranges = []
    for mapping in mappings:
        ranges.append(
            {
                "name": mapping.in_sheet,
                "values": list(
                    map(
                        lambda v: apply_conversion_function(
                            getattr(v, mapping.in_db),
                            mapping.default,
                            mapping.type,
                        ),
                        values,
                    )
                ),
            }
        )
    return ranges


def set_workbook_uei(workbook, uei):
    """Sets the UEI value in the workbook's designated UEI cell"""
    if not uei:
        raise DataMigrationError("UEI value is missing or invalid.")
    set_range(workbook, "auditee_uei", [uei])


def get_audit_header(dbkey, year):
    """Returns the AuditHeader record for the given dbkey and audit year."""
    try:
        audit_header = AuditHeader.objects.get(DBKEY=dbkey, AUDITYEAR=year)
    except AuditHeader.DoesNotExist:
        raise DataMigrationError(
            f"No audit header record found for dbkey: {dbkey} and audit year: {year}"
        )
    return audit_header


def map_simple_columns(wb, mappings, values):
    len_passed_in = len(mappings)
    unique_fields = set()
    for mapping in mappings:
        unique_fields.add(mapping.in_sheet)
    if len_passed_in != len(unique_fields):
        logger.info(f"unique: {len(unique_fields)} list: {len(mappings)}")
        logger.error(
            "You repeated a field in the mappings: {}".format(
                list(map(lambda m: m.in_sheet, mappings))
            )
        )
        raise DataMigrationError(
            "Invaid mappings. You repeated a field in the mappings"
        )

    # Map all the simple ones
    for m in mappings:
        set_range(
            wb,
            m.in_sheet,
            map(lambda v: getattr(v, m.in_db), values),
            m.default,
            m.type,
        )


def get_template_name_for_section(section):
    """
    Return a workbook template name corresponding to the given section
    """
    if section in sections_to_template_paths:
        template_name = sections_to_template_paths[section].name
        return template_name
    else:
        raise ValueError(f"Unknown section {section}")


def generate_dissemination_test_table(audit_header, api_endpoint, mappings, objects):
    """Generates a test table for verifying the API queries results."""
    table = {"rows": list(), "singletons": dict()}
    table["endpoint"] = api_endpoint
    table["report_id"] = xform_dbkey_to_report_id(audit_header)

    for o in objects:
        test_obj = {}
        test_obj["fields"] = []
        test_obj["values"] = []
        for m in mappings:
            # What if we only test non-null values?
            raw_value = getattr(o, m.in_db, None)
            attribute_value = apply_conversion_function(raw_value, m.default, m.type)
            if (attribute_value is not None) and (attribute_value != ""):
                if m.in_dissem == WorkbookFieldInDissem:
                    # print(f'in_sheet {m.in_sheet} <- {attribute_value}')
                    test_obj["fields"].append(m.in_sheet)
                    # The typing must be applied here as well, as in the case of
                    # type_requirement, it alphabetizes the value...
                    test_obj["values"].append(m.type(attribute_value))
                else:
                    # print(f'in_dissem {m.in_dissem} <- {attribute_value}')
                    test_obj["fields"].append(m.in_dissem)
                    test_obj["values"].append(m.type(attribute_value))

        table["rows"].append(test_obj)
    return table


def get_audits(dbkey, year):
    """Returns Audits records for the given dbkey and audit year."""
    return Audits.objects.filter(DBKEY=dbkey, AUDITYEAR=year).order_by("ID")


def xform_add_hyphen_to_zip(zip):
    """
    Transform a ZIP code string by adding a hyphen. If the ZIP code has 9 digits, inserts a hyphen after the fifth digit.
    Returns the original ZIP code if it has 5 digits or is malformed.
    """
    strzip = string_to_string(zip)
    if len(strzip) == 5:
        return strzip
    elif len(strzip) == 9:
        # FIXME - MSHD: This is a transformation and might require logging.
        return f"{strzip[0:5]}-{strzip[5:9]}"
    else:
        # FIXME - MSHD: How do we handle 4-digit and 8-digit ZIP codes?
        raise DataMigrationError("Zip code is malformed in secondary auditor.")