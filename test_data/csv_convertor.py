def to_csv(filename):
    with open(filename, 'w') as file:
        pass

import os
# import numpy as np
import io
import struct
import datetime

# print(os.path.exists("cv_cv1_05_04_2023_15_54_06_0001.isc"))

#     # lines = f.readlines()
# nlines = []
# for line in lines: # select only last 10 character from line
#     nlines.append(line[:10])


# print(lines[0])




from zahner_analysis.file_import.isc_import import IscImport

a = IscImport('test_data/cv_cv1_05_04_2023_15_54_06_0001.isc')
print(a)
print(a.Time)
print(a.current)
print(a.voltage)
# IsrImport()
# IsrImport 