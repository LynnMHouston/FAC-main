from audit.fixtures.excel import (
    SECTION_NAMES,
)


def err_additional_ueis_empty():
    return (
        "general_information.multiple_ueis_covered is checked, "
        "but no additonal UEIs were found."
    )


def err_additional_ueis_has_auditee_uei():
    return "The additional UEIs list includes the auditee UEI."


def err_additional_ueis_not_empty():
    return (
        "general_information.multiple_ueis_covered is marked false, "
        "but additonal UEIs were found."
    )


def err_auditee_ueis_match():
    return "Not all auditee UEIs matched."


def err_awards_findings_but_no_findings_text():
    return "There are findings indicated in Federal Awards but" "none in Findings Text."


def err_missing_tribal_data_sharing_consent():
    return (
        "As a tribal organization, you must complete the data "
        "sharing consent statement before submitting your audit."
    )


def err_award_ref_repeat_reference(award_ref, ref_number):
    return f"Award {award_ref} repeats reference {ref_number}. The reference {ref_number} should only appear once for award {award_ref}."


def err_number_of_findings_inconsistent(total_expected, total_counted, award_ref):
    return (
        f"You reported {total_expected} findings for award {award_ref} in the {SECTION_NAMES.FEDERAL_AWARDS} workbook, "
        f"but declared {total_counted} findings for the same award in the {SECTION_NAMES.FEDERAL_AWARDS_AUDIT_FINDINGS} workbook."
    )


def err_missing_award_reference(row_num):
    return (
        f"The award listed in row {row_num} of your Federal Award workbook is missing a reference code. "
        f"This should not be possible. Please contact customer support."
    )
