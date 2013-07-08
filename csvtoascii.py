import os
import sys
import datetime

import csv


sys.path.append("/home/krg85/Projects/VoxApp/core")
from core.result.resultutils import RespondentReportGenerator

def csvtoasci(filename, codingfile):
    report_format = open(codingfile, "r").read()
    outputfile = "ascii.dat"
    with open(outputfile, "wb") as reportfile:
        with open(filename, mode='rU') as infile:
            reader = csv.DictReader(infile, ["mobile", "gender", "month", "year", "state","district", "occupation", "education",
                                             "sec classification"],
                                restkey = "answers")
            reader.next()
            for row in reader:
                r = RespondentReportGenerator(None, row["mobile"][2:], row, report_format )
                reportfile.write(r.generate())

if __name__ == "__main__":
    csvtoasci(sys.argv[1], sys.argv[2])
