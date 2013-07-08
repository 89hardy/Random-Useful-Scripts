import StringIO
from collections import OrderedDict
import json
import traceback
import datetime
from django.utils.datastructures import SortedDict
import sys
from core.result.models import Result

blank_char = " "

class ResultRowWriter(object):
    def __init__(self, card):
        self.code_dict = {}
        self.max_length = 0
        self.card = card

    def write(self, startpos, content):
        maxlen = startpos + len(content) - 1
        for i, item in enumerate(content, startpos):
            self.code_dict[i] = item

        self.max_length = max(self.max_length, maxlen)


    def write_n(self, startpos, endpos, content):
        no_chars = endpos - startpos + 1
        self.write(startpos, content.zfill(no_chars)[0:no_chars])



    def read(self):
        char_arr = [blank_char] * self.max_length
        for pos, value in self.code_dict.iteritems():
            char_arr[pos - 1] = value

        return "".join(char_arr)

    def get_card(self):
        return self.card




class RespondentReportGenerator(object):

    KEY_DEMOGRAPHICS = "demographic"
    KEY_AGE = "age"
    KEY_UPPER_VALUE = "upperValue"
    KEY_LOWER_VALUE = "lowerValue"
    KEY_GENDER = "gender"
    KEY_LOCATION = "district"
    KEY_ANSWER_OPTIONS = "answerOptions"
    KEY_QUESTION_OPTIONS = "questionOptions"
    KEY_CODE_VALUE = "outputKey"
    KEY_ADDRESS = "address"
    KEY_CARD = "row"
    KEY_COL_START = "colStart"
    KEY_COL_END = "colEnd"
    KEY_QUESTIONS = "questions"
    KEY_ANSWERS = "answers"
    KEY_ANSWER = "answer"
    KEY_QUESTION_ID = "qid"
    KEY_DOB = "dob"
    KEY_MONTH = "month"
    KEY_YEAR = "year"


    def __init__(self, respondent, identifier, response_schema, coding_json):
        self.respondent_schema = response_schema
        self.identifier = identifier
        self.output_coding = json.loads(coding_json)
        self.report = []
        self.current_row = None



    def set_age_code(self, ageinfo):
        age = self._calculate_age()
        agedict = None
        for ansoption, ansdict in ageinfo.iteritems():
            if not age:
                if not ansdict[self.KEY_UPPER_VALUE] and not ansdict[self.KEY_LOWER_VALUE]:
                    agedict = ansdict
                    break
            else:
                if age <= ansdict[self.KEY_UPPER_VALUE] and age >= ansdict[self.KEY_LOWER_VALUE]:
                    agedict = ansdict
                    break

        if agedict:
            self._writeValue(agedict[self.KEY_ADDRESS], agedict[self.KEY_CODE_VALUE])

    def _calculate_age(self):

        delta =  datetime.date.today() - \
                 datetime.date(int(self.respondent_schema[self.KEY_YEAR]),
                               int(self.respondent_schema[self.KEY_MONTH]), 1)

        age =  delta.days / 365

        print "Age for respondent %s is %d" % (self.respondent_schema["mobile"], age)

        return age


    def set_location_code(self, locinfo):
        others = locinfo.get("Other", None)
        locdict = locinfo.get(self.respondent_schema["district"], others)
        self._writeValue(locdict[self.KEY_ADDRESS], locdict[self.KEY_CODE_VALUE])


    def set_gender_code(self, genderinfo):
        genderdict = genderinfo[self.respondent_schema["gender"]]
        self._writeValue(genderdict[self.KEY_ADDRESS], genderdict[self.KEY_CODE_VALUE])


    def _writeValue(self, address, code):
        self._set_current_row(address[self.KEY_CARD])
        self.current_row.write(int(address[self.KEY_COL_START]), code)


    def _set_current_row(self, card):
        if not self.current_row or self.current_row.get_card() != card:
            self._create_new_row(card)

    def _create_new_row(self, card):
        if self.current_row:
            self.report.append(self.current_row.read())

        row = ResultRowWriter(card)
        row.write_n(1, 2,  str(card))
        row.write_n(3, 10, self.identifier)
        self.current_row = row

    def generate_demographics(self):
        demographics = self.output_coding[self.KEY_DEMOGRAPHICS]
        self.set_age_code(demographics[self.KEY_AGE][self.KEY_ANSWER_OPTIONS])
        self.set_gender_code(demographics[self.KEY_GENDER][self.KEY_ANSWER_OPTIONS])
        self.set_location_code(demographics[self.KEY_LOCATION][self.KEY_ANSWER_OPTIONS])

    def generate(self):
        try:
            self.generate_demographics()
            self.generate_answers()
            print "Result for Respondent %s" % self.respondent_schema["mobile"]
            print "\n".join(self.report)
            return "%s%s" % ("\n".join(self.report), "\n")

        except Exception, e:
            print "Exception while trying to parse result for respondent ", self.respondent_schema["mobile"]
            traceback.print_exc()
            return ""

    def generate_answers(self):
        answers = self.respondent_schema[self.KEY_ANSWERS]
        coding_format = self.output_coding[self.KEY_QUESTIONS]
        for i, answer  in enumerate(answers):
            answer = answer.lower()
            if not answer.strip() or i == 1 or answer == "n/a":
                continue

            answer = convert_to_python_ds(answer)


            codes_dict = coding_format[i]
            if isinstance(answer, list):
                codes = codes_dict[self.KEY_ANSWER_OPTIONS]
                self._prepare_answer_code(codes)
                for selection in answer:
                    selected_code = codes[selection]
                    self._writeValue(selected_code[self.KEY_ADDRESS],
                                     selected_code[self.KEY_CODE_VALUE])

            elif isinstance(answer, dict):
                question_codes = codes_dict[self.KEY_QUESTION_OPTIONS]

                answer_codes = codes_dict[self.KEY_ANSWER_OPTIONS]
                print answer_codes
                self._prepare_answer_code(question_codes)
                for id, ans in answer.iteritems():
                    address = question_codes[id][self.KEY_ADDRESS]
                    selected_code = answer_codes[ans]
                    self._writeValue(address, selected_code[self.KEY_CODE_VALUE])

        self.report.append(self.current_row.read())


    def _prepare_answer_code(self, optionsdict):

        for values in optionsdict.values():
            address = values[self.KEY_ADDRESS]
            card = address[self.KEY_CARD]
            colStart = address[self.KEY_COL_START]
            colEnd = address[self.KEY_COL_END]
            if not colEnd:
                cont = blank_char
            else:
                cont = blank_char * (colEnd - colStart + 1)

            self._set_current_row(card)
            self.current_row.write(colStart, cont)



def convert_to_python_ds(str):

    if ":" in str:
        return dict([tuple(elem.strip().split(":")) for elem in str.split(",")])
    else:
        return map(lambda x: x.strip(), str.split(","))

