#!/usr/bin/python

import csv
import sys
import time

now=time.localtime(time.time())
currentmonth=now.tm_mon
currentday=now.tm_mday
currentyear=now.tm_year
filenameIN = "{0}_{1}_{2}_checkedIN.csv".format(currentyear, currentmonth, currentday)
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

global barcode

while True:
    try:
        #input barcode of attendee
        barcode = int(raw_input('Enter attendee barcode: '))
        #barcode = sys.stdin.readline().rstrip()

        if barcode == 1:
            checkSTATUS = 1
            print "Checking IN registered attendees!"

        elif barcode == 0:
            checkSTATUS = 0
            print "Checking OUT registered attendees!"

        elif barcode != 0 & barcode != 1:
            if checkSTATUS == 1:
                #read csv, and split on "," the line
                attendee_csv_file = csv.reader(open('attendee_list.csv', "rb"), delimiter=",")

                #get current time
                now=time.localtime(time.time())
                pt=time.asctime(now)  #formatted time for file
                currentmonth=now.tm_mon
                currentday=now.tm_mday
                currentyear=now.tm_year

                #loop through csv list
                for row in attendee_csv_file:
                    #if current rows first value (0 row) is equal to input, print that row
                    barcode = str(barcode)
                    if barcode == row[0]:
                        attendee = row[1].strip()
                        print "Thank you,",attendee #prints only the numbered column in the found row

                        #get current time
                        now=time.localtime(time.time())
                        pt=time.asctime(now)  #formatted time for file
                        currentmonth=now.tm_mon
                        currentday=now.tm_mday
                        currentyear=now.tm_year

                        barcode = int(barcode)

                        #write attendee name and check in time to file
                        file=open(filenameIN,"a")
                        file.write("%i,%s,%s\n" % (barcode,attendee,pt))
                        file.close()

                    else:
                        print "Attendee NOT registered!\n"

            elif checkSTATUS == 0:
                #get current time
                now=time.localtime(time.time())
                pt=time.asctime(now)  #formatted time for file
                currentmonth=now.tm_mon
                currentday=now.tm_mday
                currentyear=now.tm_year

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
                        file.write("%i,%s,%s,%s\n" % (barcode,attendee,timeIN,timeOUT))
                        file.close()
                        print "Thank you,",attendee #prints only the numbered column in the found row

                    elif barcode != row[0]:
                        print "Attendee NOT checked in!\n"

    except KeyboardInterrupt:
        print '\ncaught keyboard interrupt!, bye'
        sys.exit()
