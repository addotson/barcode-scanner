#!/usr/bin/python

import csv
import sys

#input number you want to search
number = raw_input('Enter number to find\n')

#read csv, and split on "," the line
csv_file = csv.reader(open('test.csv', "rb"), delimiter=",")


#loop through csv list
for row in csv_file:
    #if current rows 2nd value is equal to input, print that row
    if number == row[0]:
         print row[1].strip() #prints only the numbered column in the found row
