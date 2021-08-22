import datetime

from taxlover.utils import get_assessment_years


class TaxPayerDTO:

    def __init__(self, payer):
        assessment_year_beg, assessment_year_end = get_assessment_years()

        assessment_year_beg_str = str(assessment_year_beg)
        assessment_year_end_str = str(assessment_year_end)

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

        self.employer_name = payer.get_employer_name

        self.spouse_name = payer.get_spouse_name
        self.spouse_tin = payer.get_spouse_e_tin

        self.fathers_name = payer.get_fathers_name
        self.mothers_name = payer.get_mothers_name

        self.present_address = payer.get_present_address_line_one
        self.permanent_address = payer.get_permanent_address

        self.contact_no = payer.get_contact_no
        self.email = payer.get_email

        self.nid = payer.get_nid
        self.bin = payer.get_bin

        self.tin_digit_1 = self.tin[0]
        self.tin_digit_2 = self.tin[1]
        self.tin_digit_3 = self.tin[2]
        self.tin_digit_4 = self.tin[3]
        self.tin_digit_5 = self.tin[4]
        self.tin_digit_6 = self.tin[5]
        self.tin_digit_7 = self.tin[6]
        self.tin_digit_8 = self.tin[7]
        self.tin_digit_9 = self.tin[8]
        self.tin_digit_10 = self.tin[9]
        self.tin_digit_11 = self.tin[10]
        self.tin_digit_12 = self.tin[11]



