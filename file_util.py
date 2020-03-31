from openpyxl import load_workbook


def get_excel_sheet():
    """
    Retrieves excel sheet from our vocabulary file. At the moment we know that we only have 1 sheet,
    so we can just retrieve the first one.
    :return: Excel sheet
    """
    workbook = load_workbook('vocab.xlsx', data_only=True)
    sheet = workbook[workbook.sheetnames[0]]
    return sheet


def get_entries(sheet):
    """
    Retrieves vocabulary entries
    :param sheet: Excel sheet from vocabulary file
    :return: Vocabulary entries as dictionary
    """
    vocabulary = {"entries": []}
    for row in sheet.iter_rows():
        entry = [row[0].value,
                 row[1].value,
                 row[2].value,
                 row[3].value,
                 row[4].value]
        vocabulary["entries"].append(entry)
    return vocabulary


def get_vocabulary():
    """
    Master function to get vocabulary
    :return: Vocabulary entries as dictionary
    """
    sheet = get_excel_sheet()
    entries = get_entries(sheet)
    return entries
