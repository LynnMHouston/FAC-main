import re

from ..transforms.xform_string_to_int import string_to_int
from ..transforms.xform_string_to_bool import string_to_bool
from ..exception_utils import DataMigrationError
from ..transforms.xform_string_to_string import string_to_string
from ..workbooklib.excel_creation_utils import get_audits

from ..base_field_maps import FormFieldMap, FormFieldInDissem
from ..sac_general_lib.utils import (
    create_json_from_db_object,
    is_single_word,
)
import audit.validators
from django.conf import settings


def xform_apply_default_thresholds(value):
    """Applies default threshold when value is None."""
    str_value = string_to_string(value)
    if str_value == "":
        # FIXME-MSHD: This is a transformation that we may want to record
        return settings.DOLLAR_THRESHOLD
    return string_to_int(str_value)


mappings = [
    FormFieldMap(
        "dollar_threshold",
        "DOLLARTHRESHOLD",
        FormFieldInDissem,
        None,
        int,  # FIXME-MSHD: If team approves, we can change this to xform_apply_default_thresholds
    ),
    FormFieldMap(
        "is_going_concern_included", "GOINGCONCERN", FormFieldInDissem, None, bool
    ),
    FormFieldMap(
        "is_internal_control_deficiency_disclosed",
        "MATERIALWEAKNESS",
        FormFieldInDissem,
        None,
        bool,
    ),
    FormFieldMap(
        "is_internal_control_material_weakness_disclosed",
        "MATERIALWEAKNESS_MP",
        FormFieldInDissem,
        None,
        bool,
    ),
    FormFieldMap(
        "is_material_noncompliance_disclosed",
        "MATERIALNONCOMPLIANCE",
        FormFieldInDissem,
        None,
        bool,
    ),
    FormFieldMap(
        "is_aicpa_audit_guide_included",
        "REPORTABLECONDITION",
        FormFieldInDissem,
        None,
        bool,
    ),
    FormFieldMap("is_low_risk_auditee", "LOWRISK", FormFieldInDissem, None, bool),
    FormFieldMap("agencies", "PYSCHEDULE", "agencies_with_prior_findings", [], list),
]


def _get_agency_prefixes(dbkey, year):
    """Returns the agency prefixes for a given dbkey and audit year."""
    agencies = set()
    audits = get_audits(dbkey, year)

    for audit_detail in audits:
        agencies.add(string_to_string(audit_detail.CFDA_PREFIX))

    return agencies


def xform_framework_basis(basis):
    """Transforms the framework basis from Census format to FAC format.
    For context, see ticket #2912.
    """
    basis = string_to_string(basis)
    if is_single_word(basis):
        # FIXME-MSHD: Update validation schema to include `regulatory_basis`
        mappings = {
            r"cash": "cash_basis",
            r"contractual": "contractual_basis",
            r"regulatory": "regulatory_basis",
            r"tax": "tax_basis",
            r"other": "other_basis",
        }
        # Check each pattern in the mappings with case-insensitive search
        for pattern, value in mappings.items():
            if re.search(pattern, basis, re.IGNORECASE):
                # FIXME-MSHD: This is a transformation that we may want to record
                return value

    raise DataMigrationError(
        f"Could not find a match for historic framework basis: '{basis}'"
    )


def xform_census_keys_to_fac_options(census_keys, fac_options):
    """Maps the census keys to FAC options.
    For context, see ticket #2912.
    """

    if "U" in census_keys:
        fac_options.append("unmodified_opinion")
    if "Q" in census_keys:
        fac_options.append("qualified_opinion")
    if "A" in census_keys:
        fac_options.append("adverse_opinion")
    if "D" in census_keys:
        fac_options.append("disclaimer_of_opinion")


def xform_build_sp_framework_gaap_results(audit_header):
    """Returns the SP Framework and GAAP results for a given audit header."""

    sp_framework_gaap_data = string_to_string(audit_header.TYPEREPORT_FS).upper()
    if not sp_framework_gaap_data:
        raise DataMigrationError(
            f"GAAP details are missing for DBKEY: {audit_header.DBKEY}"
        )

    sp_framework_gaap_results = {}
    sp_framework_gaap_results["gaap_results"] = []
    xform_census_keys_to_fac_options(
        sp_framework_gaap_data, sp_framework_gaap_results["gaap_results"]
    )
    if "S" in sp_framework_gaap_data:
        sp_framework_gaap_results["gaap_results"].append("not_gaap")
        sp_framework_gaap_results["is_sp_framework_required"] = string_to_bool(
            audit_header.SP_FRAMEWORK_REQUIRED
        )
        sp_framework_gaap_results["sp_framework_opinions"] = []
        sp_framework_opinions = string_to_string(
            audit_header.TYPEREPORT_SP_FRAMEWORK
        ).upper()
        xform_census_keys_to_fac_options(
            sp_framework_opinions, sp_framework_gaap_results["sp_framework_opinions"]
        )
        sp_framework_gaap_results["sp_framework_basis"] = []
        basis = xform_framework_basis(audit_header.SP_FRAMEWORK)
        sp_framework_gaap_results["sp_framework_basis"].append(basis)

    return sp_framework_gaap_results


# FIXME-MSHD: Not being used, but we may need it in the future
def _xform_agencies(audit_info):
    """Transforms the agencies from Census format to FAC format."""

    new_audit_info = audit_info.copy()
    # Apply transformation to each key
    transformed_agencies = [
        str(i) if len(str(i)) > 1 else f"0{str(i)}" for i in audit_info.get("agencies")
    ]

    new_audit_info["agencies"] = transformed_agencies
    return new_audit_info


def audit_information(audit_header):
    """Generates audit information JSON."""
    results = xform_build_sp_framework_gaap_results(audit_header)
    agencies_prefixes = _get_agency_prefixes(audit_header.DBKEY, audit_header.AUDITYEAR)
    audit_info = create_json_from_db_object(audit_header, mappings)
    audit_info = {
        key: results.get(key, audit_info.get(key))
        for key in set(audit_info) | set(results)
    }
    audit_info["agencies"] = list(agencies_prefixes)

    # Validate against the schema
    audit.validators.validate_audit_information_json(audit_info)

    return audit_info