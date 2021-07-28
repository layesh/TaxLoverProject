import datetime


class TaxPayerDTO:

    def __init__(self, payer):
        current_month = datetime.date.today().month
        current_year = datetime.date.today().year

        assessment_year_beg = current_year if current_month > 6 else current_year - 1

        assessment_year_beg_str = str(assessment_year_beg)
        assessment_year_end_str = str(assessment_year_beg + 1)

        self.assessment_year_beg_digit_0 = assessment_year_beg_str[0]
        self.assessment_year_beg_digit_1 = assessment_year_beg_str[1]
        self.assessment_year_beg_digit_2 = assessment_year_beg_str[2]
        self.assessment_year_beg_digit_3 = assessment_year_beg_str[3]

        self.assessment_year_end_digit_2 = assessment_year_end_str[2]
        self.assessment_year_end_digit_3 = assessment_year_end_str[3]

        self.section_82bb = False

        self.name = payer.get_name

        self.male = (payer.gender == 'M')
        self.female = (payer.gender == 'F')

        self.tin = payer.get_e_tin
        self.old_tin = ''

        self.circle = payer.get_tax_circle
        self.zone = payer.get_tax_zone

        self.is_resident = payer.is_resident
        self.is_non_resident = payer.is_non_resident


