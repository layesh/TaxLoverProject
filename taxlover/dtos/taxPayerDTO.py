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

        self.is_gazetted_war_wounded_freedom_fighter = payer.is_gazetted_war_wounded_freedom_fighter
        self.is_differently_abled = payer.is_differently_abled
        self.is_aged_65_years_or_more = payer.is_aged_65_years_or_more
        self.is_has_differently_abled_children = payer.is_has_differently_abled_children

        self.dob_day_digit_1 = payer.get_dob[0] if payer.get_dob else ""
        self.dob_day_digit_2 = payer.get_dob[1] if payer.get_dob else ""

        self.dob_mon_digit_1 = payer.get_dob[3] if payer.get_dob else ""
        self.dob_mon_digit_2 = payer.get_dob[4] if payer.get_dob else ""

        self.dob_year_digit_1 = payer.get_dob[6] if payer.get_dob else ""
        self.dob_year_digit_2 = payer.get_dob[7] if payer.get_dob else ""
        self.dob_year_digit_3 = payer.get_dob[8] if payer.get_dob else ""
        self.dob_year_digit_4 = payer.get_dob[9] if payer.get_dob else ""

        self.income_year_beg = assessment_year_beg - 1
        self.income_year_end = assessment_year_beg


