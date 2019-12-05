import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import QuantLib as ql
from datetime import datetime


class ConvertDate:
    def __init__(self, date, dateFormat, newFormat=None):
        self._sDate = date  # input format %Y-%m-%d
        self._sFormat = dateFormat
        self._sNewFormat = newFormat
        self.mdtFormat = self.stringIntoDateTime()
        self.mqlFormat = self.dtIntoQuantLib()
        self.mqlFormat2 = self.stringIntoQuantLib()  # from string into quantlib
        self.mDateAfterChange = self.changeFormatDate()

    def stringIntoDateTime(self):
        return datetime.strptime(self._sDate, self._sFormat)

    def dtIntoQuantLib(self):
        quantDate = ql.Date(self.mdtFormat.day, self.mdtFormat.month, self.mdtFormat.year)
        return quantDate

    def changeFormatDate(self):
        return datetime.strptime(self._sDate, '%Y-%m-%d').strftime(self._sNewFormat)

    def stringIntoQuantLib(self):
        year = int(self._sDate[0:4])
        month = int(self._sDate[5:7])
        day = int(self._sDate[8:])
        ql_date = ql.Date(day, month, year)
        return ql_date


if __name__ == '__main__':
    datetime.strptime('2019-05-22', '%Y-%m-%d').strftime('%d/%m/%y')
    pass
