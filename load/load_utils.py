
class LoadUtils:

    @staticmethod
    def generate_report_filename(raport_type: str, year: int, month: int) -> str:
        """
        Generates the report filename in the format EP<YY><MM><TableType>,
        e.g., EP2412C1 for December 2024 C1 report.

        :param table_type: Report table identifier, e.g. 'A1', 'B1', 'C1'.
        :param year: Full year, e.g. 2024.
        :param month: Month as integer, e.g. 4 or 12.
        :return: Formatted filename string.
        """
        year_suffix = str(year)[-2:]
        month_str = str(month).zfill(2)
        return f"EP{year_suffix}{month_str}{raport_type}"
