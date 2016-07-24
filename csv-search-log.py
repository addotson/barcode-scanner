#!/usr/bin/python

import csv
import sys
import time

now=time.localtime(time.time())
currentmonth=now.tm_mon
currentday=now.tm_mday
currentyear=now.tm_year
filenameIN = "{0}_{1}_{2}_checkedIN.csv".format(currentyear, 
currentmonth, currentday)
filenameOUT = "{0}_{1}_{2}_checkedOUT.csv".format(currentyear, currentmonth, currentday)

#### informative messaging for starting storage file
print "Creating ",filenameIN, "and ",filenameOUT," for appending..."
print "waiting for barcode inputs and storing data..."
file=open(filenameIN,"a")
file.write("Barcode,Name,Time In\n")
file.close()
file=open(filenameOUT,"a")
file.write("Barcode,Name,Time In,Time Out\n")
file.close()


#select check in or check out
checkSTATUS = raw_input('Checking in (1) or checking out (0): ')
checkSTATUS = int(checkSTATUS)

if checkSTATUS == 1:
    #input barcode of attendee
    barcode = raw_input('Enter attendee barcode: ')

    #read csv, and split on "," the line
    attendee_csv_file = csv.reader(open('attendee_list.csv', "rb"), delimiter=",")

    #loop through csv list
    for row in attendee_csv_file:
        #if current rows first value (0 row) is equal to input, print that row
        if barcode == row[0]:
            attendee = row[1].strip()
            print attendee #prints only the numbered column in the found row

            #get current time
            now=time.localtime(time.time())
            pt=time.asctime(now)  #formatted time for file
            currentmonth=now.tm_mon
            currentday=now.tm_mday
            currentyear=now.tm_year

            #cast barcode to integer
            barcode = int(barcode)

            #write attendee name and check in time to file
            file=open(filenameIN,"a")
            file.write("%i,%s,%s\n" % (barcode,attendee,pt))
            file.close()
elif checkSTATUS == 0:
    #get current time
    now=time.localtime(time.time())
    pt=time.asctime(now)  #formatted time for file
    currentmonth=now.tm_mon
    currentday=now.tm_mday
    currentyear=now.tm_year

    #input barcode of attendee
    barcode = raw_input('Enter attendee barcode: ')

    #read csv, and split on "," the line
    checkedIN_csv_file = csv.reader(open(filenameIN, "rb"), delimiter=",")

    #loop through csv list
    for row in checkedIN_csv_file:
        #if current rows first value (0 row) is equal to input, print that row
        if barcode == row[0]:
            barcode = int(row[0])
            attendee = row[1]
            timeIN = row[2]
            timeOUT = pt

            #write attendee name and check in time to file
            file=open(filenameOUT,"a")
            file.write("%s,%s,%s,%s\n" % (barcode,attendee,timeIN,timeOUT))
            file.close()
