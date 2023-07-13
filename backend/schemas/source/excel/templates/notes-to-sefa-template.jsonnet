local Fun = import '../libs/Functions.libsonnet';
local Help = import '../libs/Help.libsonnet';
local SV = import '../libs/SheetValidations.libsonnet';
local Sheets = import '../libs/Sheets.libsonnet';
local sefaMandatorySheet = 'MandatoryNotes';
local sefaAdditionalSheet = 'AdditionalNotes';
local ueiSheet = 'UEI';
local title_row = 1;

local single_cells = [
  Sheets.single_cell {
    title: 'Auditee UEI',
    range_name: 'auditee_uei',
    width: 36,
    title_cell: 'A1',
    range_cell: 'A2',
    validation: SV.StringOfLengthTwelve,
    help: Help.uei,
  },
];
local other_single_cells = [
  Sheets.single_cell {
    title: 'Describe the significant accounting policies \nused in preparing the SEFA. (2 CFR 200.510(b)(6))',
    range_name: 'accounting_policies',
    width: 56,
    title_cell: 'A1',
    range_cell: 'A2',
    validation: SV.NoValidation,
    help: Help.plain_text,
  },
  Sheets.single_cell {
    title: 'Did the auditee use the de minimis cost rate? \n(2 CFR 200.414(f))',
    range_name: 'is_minimis_rate_used',
    width: 24,
    title_cell: 'B1',
    range_cell: 'B2',
    validation: SV.YoNValidation,
    help: Help.yorn,
  },
  Sheets.single_cell {
    title: 'Please explain',
    range_name: 'rate_explained',
    width: 56,
    title_cell: 'C1',
    range_cell: 'C2',
    validation: SV.StringOfLengthTwelve,
    help: Help.plain_text,
  },
];

local open_ranges_defns = [
  [
    Sheets.open_range {
      title_cell: 'A1',
      width: 36,
      help: Help.plain_text,
    },
    SV.NoValidation,
    'Note title',
    'note_title',
  ],
  [
    Sheets.open_range {
      title_cell: 'B1',
      width: 56,
      help: Help.plain_text,
    },
    SV.YoNValidation,
    'Note content',
    'note_content',
  ],
];

local sheets = [
  {
    name: sefaMandatorySheet,
    single_cells: other_single_cells,
    header_height: 100,
  },
  {
    name: sefaAdditionalSheet,
    open_ranges: Fun.make_open_ranges_with_column(title_row, open_ranges_defns),
    header_height: 100,
  },
  {
    name: ueiSheet,
    single_cells: single_cells,
    header_height: 100,
  },
];

local workbook = {
  filename: 'notes-to-sefa-template.xlsx',
  sheets: sheets,
  title_row: title_row,
};

{} + workbook
