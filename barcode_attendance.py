#!/usr/bin/python

import csv
import sys
import time
import os

now=time.localtime(time.time())
currentmonth=now.tm_mon
currentday=now.tm_mday
currentyear=now.tm_year

#input barcode of attendee
os.system('clear')
print '**Welcome to Python Conference Barcode Attendance Tracker**'
print '\nEnter session barcode: '
session = sys.stdin.readline().rstrip()


filenameIN = "{0}_{1}_{2}_{3}_checkedIN.csv".format(currentyear, currentmonth, currentday, session)
filenameOUT = "{0}_{1}_{2}_{3}_checkedOUT.csv".format(currentyear, currentmonth, currentday, session)

restart = True

if (os.path.isfile(filenameIN) and os.path.isfile(filenameOUT) and restart):
    #restart ensures that it will only execute this once.
    restart = False
    #restarting the file
    os.system('clear')
    print "Opening previously created files",filenameIN, "and",filenameOUT
    time.sleep(2)
    os.system('clear')
    file=open(filenameIN,"a")
    file.close()
    file=open(filenameOUT,"a")
    file.close()

elif not (os.path.isfile(filenameIN) and os.path.isfile(filenameOUT)):
    #informative messaging for starting storage file
    os.system('clear')
    print "Creating",filenameIN, "and",filenameOUT
    time.sleep(2)
    os.system('clear')
    file=open(filenameIN,"a")
    file.write("Barcode,Name,Session,Time In\n")
    file.close()
    file=open(filenameOUT,"a")
    file.write("Barcode,Name,Session,Time In,Time Out\n")
    file.close()

checkSTATUS = 1
attendee_linecount = 0
checkedIN_attendee_linecount = 0

while True:
    try:
        attendee_csv_file = csv.reader(open('attendee_list.csv', "rb"), delimiter=",")
        attendee_row_count = sum(1 for row in attendee_csv_file)
        checkedIN_csv_file = csv.reader(open(filenameIN, "rb"), delimiter=",")
        checkedIN_attendee_row_count = sum(1 for row in checkedIN_csv_file)

        #input barcode of attendee
        if checkSTATUS == 1:
            print "\nSession: {0}\n--- Checking IN ---\nEnter Barcode: ".format(session)
        if checkSTATUS == 2:
            print "\nSession: {0}\n--- Checking OUT ---\nEnter Barcode: ".format(session)

        barcode = sys.stdin.readline().rstrip()
        barcode_int = int(barcode)

        if barcode_int == 0000:
            print "Enter configuration barcode: "
            checkSTATUS = sys.stdin.readline().rstrip()
            checkSTATUS = int(checkSTATUS)
            #currently key commands
            # 1 check in
            # 2 check out
            # 0 exit program
            time.sleep(2)
            os.system('clear')

            if checkSTATUS == 0:
                print '\nExiting program!, bye'
                sys.exit()

        elif checkSTATUS == 1:

            #read csv, and split on "," the line
            checkedIN_csv_file = csv.reader(open(filenameIN, "rb"), delimiter=",")
            #loop through csv list
            for row in checkedIN_csv_file:
                if barcode == row[0]:
                    print "\nYou have already been checked in!\n"
                    time.sleep(2)
                    os.system('clear')
                    checkedin = 1
                else:
                    checkedin = 0

            #read csv, and split on "," the line
            attendee_csv_file = csv.reader(open('attendee_list.csv', "rb"), delimiter=",")
            #loop through csv list
            if checkedin == 0:
                for row in attendee_csv_file:
                    #if current rows first value (0 row) is equal to input, print that row
                    if barcode == row[0]:
                        attendee = row[1].strip()

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
                        file.write("%s,%s,%s,%s\n" % (barcode,attendee,session,pt))
                        file.close()
                        if attendee_linecount < attendee_row_count:
                            print "\nThank you,",attendee,"for checking in!\n"
                            time.sleep(2)
                            os.system('clear')
                            attendee_linecount = 0
                    else:
                        #currently this reports for all lines scaned by above statement, need to find a way to surpress if attendee found.
                        attendee_linecount = attendee_linecount + 1
                        if attendee_linecount == attendee_row_count:
                            print "\nScanned attendee not on list.\n"
                            time.sleep(2)
                            os.system('clear')
                            attendee_linecount = 0

        elif checkSTATUS == 2:
            #get current time
            now=time.localtime(time.time())
            pt=time.asctime(now)  #formatted time for file
            currentmonth=now.tm_mon
            currentday=now.tm_mday
            currentyear=now.tm_year

            #read csv, and split on "," the line
            checkedOUT_csv_file = csv.reader(open(filenameOUT, "rb"), delimiter=",")
            #loop through csv list
            for row in checkedOUT_csv_file:
                if barcode == row[0]:
                    print "\nYou have already been checked out!\n"
                    time.sleep(2)
                    os.system('clear')
                    checkedout = 1
                else:
                    checkedout = 0
            #loop through csv list

            #read csv, and split on "," the line
            checkedIN_csv_file = csv.reader(open(filenameIN, "rb"), delimiter=",")
            #loop through csv list
            if checkedout == 0:
                for row in checkedIN_csv_file:
                    #if current rows first value (0 row) is equal to input, print that row
                    if barcode == row[0]:
                        barcode = int(row[0])
                        attendee = row[1]
                        timeIN = row[3]
                        timeOUT = pt

                        #write attendee name and check in time to file
                        file=open(filenameOUT,"a")
                        file.write("%s,%s,%s,%s,%s\n" % (barcode,attendee,session,timeIN,timeOUT))
                        file.close()
                        if checkedIN_attendee_linecount < checkedIN_attendee_row_count:
                            print "\nThank you,",attendee,"for checking out!\n"
                            time.sleep(2)
                            os.system('clear')
                            checkedIN_attendee_linecount = 0
                    else:
                        #currently this reports for all lines scaned by above statement, need to find a way to surpress if attendee found.
                        checkedIN_attendee_linecount = checkedIN_attendee_linecount + 1
                        if checkedIN_attendee_linecount == checkedIN_attendee_row_count:
                            print "\nScanned attendee not checked in.\n"
                            time.sleep(2)
                            os.system('clear')
                            checkedIN_attendee_linecount = 0

        checkedout = 0

    except KeyboardInterrupt:
            print '\ncaught keyboard interrupt!, bye'
            sys.exit()
