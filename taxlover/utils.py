from decimal import Decimal


def parse_data(row, total_columns):
    for i in range(1, total_columns):
        try:
            d = 0.0
            parsed_data = Decimal(remove_comma(row[i]))
            if parsed_data > 0.0:
                return parsed_data
        except Exception:
            d = 0.0
    return 0


def remove_comma(val):
    return val.replace(',', '')



