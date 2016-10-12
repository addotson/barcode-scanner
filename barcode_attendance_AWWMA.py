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
print '** Conference Barcode Attendance Tracker **'
print '\nEnter session barcode: '
session = sys.stdin.readline().rstrip()


filenameIN = "{0}_{1}_{2}_{3}_checkedIN.csv".format(currentyear, currentmonth, currentday, session)
filenameOUT = "{0}_{1}_{2}_{3}_checkedOUT.csv".format(currentyear, currentmonth, currentday, session)
attendee_list = "AttendeeReport.csv"

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
checkedINcount = 0
checkedOUTcount = 0
attendee_linecount = 0
checkedIN_linecount = 0
checkedin = 0
checkedout = 0

while True:
    try:
        attendee_csv_file = csv.reader(open(attendee_list, "rb"), delimiter=",")
        attendee_row_count = sum(1 for row in attendee_csv_file)

        checkedIN_rows = list( csv.reader(open(filenameIN)) )
        checkedIN_row_count = len(checkedIN_rows)

        checkedIN_csv_file = csv.reader(open(filenameIN, "rb"), delimiter=",")
        #checkedIN_row_count = sum(1 for row in checkedIN_csv_file)
        #print checkedIN_row_count
        attendee_csv_file = csv.reader(open(attendee_list, "rb"), delimiter=",")
        checkedOUT_csv_file = csv.reader(open(filenameOUT, "rb"), delimiter=",")

        #input barcode of attendee
        if checkSTATUS == 1:
            print "\nSession: {0}\n--- Checking IN ---\nEnter Barcode: ".format(session)
            attendee_linecount = 0

        if checkSTATUS == 2:
            print "\nSession: {0}\n--- Checking OUT ---\nEnter Barcode: ".format(session)
            checkedIN_linecount = 0
            checkedin = 0

        checkedINcount = 0
        checkedOUTcount = 0

        barcode = sys.stdin.readline().rstrip()
        if barcode == 'config':
            #currently key commands
            # config - enter configuration mode
            # checkin - check in
            # checkout - check out
            # exit - exit program

            print "Enter configuration barcode: "
            checkSTATUS = sys.stdin.readline().rstrip()
            if checkSTATUS == 'checkin':
                checkSTATUS = 1
                checkSTATUS = int(checkSTATUS)
            if checkSTATUS == 'checkout':
                checkSTATUS = 2
                checkSTATUS = int(checkSTATUS)

            time.sleep(2)
            os.system('clear')

            if checkSTATUS == 'exit':
                print '\nExiting program! bye'
                sys.exit()

        elif checkSTATUS == 1:

            #loop through csv list
            for row in checkedIN_csv_file:
                if barcode == row[0]:
                    os.system('clear')
                    print '\x1b[0;30;43m' + '\nYou have already been checked in!\n' + '\x1b[0m'
                    time.sleep(2)
                    checkedin = 1
                    checkedINcount = checkedINcount + 1 #used to stop repeat check in
                else:
                    checkedin = 0

            #loop through csv list
            if checkedin == 0 and checkedINcount == 0:
                for row in attendee_csv_file:
                    #if current rows first value (0 row) is equal to input, print that row
                    if barcode == row[2]:
                        attendee = row[3].strip()

                        attendeeQUOTE = '"'+attendee+'"'
                        attendee.split(',')
                        lastname, firstname = attendee.split(',')
                        firstname = firstname.strip(' ')

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
                        file.write("%s,%s,%s,%s\n" % (barcode,attendeeQUOTE,session,pt))
                        file.close()

                        if attendee_linecount < attendee_row_count:
                            os.system('clear')
                            print '\x1b[6;30;42m' '\n',firstname,lastname,'-- Thank you for checking in!\n' + '\x1b[0m'
                            time.sleep(2)
                            attendee_linecount = 0
                            checkedin = 1

                    if barcode != row[2]:
                        attendee_linecount = attendee_linecount + 1
                        if attendee_linecount == attendee_row_count:
                            os.system('clear')
                            print '\x1b[1;30;41m' + '\nScanned attendee not on list.\n' + '\x1b[0m'
                            time.sleep(2)
                            attendee_linecount = 0

        elif checkSTATUS == 2:
            #get current time
            now=time.localtime(time.time())
            pt=time.asctime(now)  #formatted time for file
            currentmonth=now.tm_mon
            currentday=now.tm_mday
            currentyear=now.tm_year

            #loop through csv list
            for row in checkedOUT_csv_file:
                if barcode == row[0]:
                    os.system('clear')
                    print '\x1b[0;30;43m' + '\nYou have already been checked out!\n' + '\x1b[0m'
                    time.sleep(2)
                    checkedout = 1
                else:
                    checkedout = 0

            #loop through csv list
            if checkedout == 0:
                for row in checkedIN_csv_file:
                    #if current rows first value (0 row) is equal to input, print that row
                    if barcode == row[0]:
                        barcode = int(row[0])
                        attendee = row[1]

                        attendeeQUOTE = '"'+attendee+'"'
                        attendee.split(',')
                        lastname, firstname = attendee.split(',')
                        firstname = firstname.strip(' ')

                        timeIN = row[3]
                        timeOUT = pt

                        #write attendee name and check in time to file
                        file=open(filenameOUT,"a")
                        file.write("%s,%s,%s,%s,%s\n" % (barcode,attendeeQUOTE,session,timeIN,timeOUT))
                        file.close()
                        os.system('clear')
                        print '\x1b[6;30;42m' '\n',firstname,lastname,'-- Thank you for checking out!\n' + '\x1b[0m'
                        time.sleep(2)
                        checkedout = 1

                    else:
                        checkedIN_linecount = checkedIN_linecount + 1
                        if checkedIN_linecount == checkedIN_row_count:
                            os.system('clear')
                            print '\x1b[1;30;41m' +'\nScanned attendee not checked in.\n' + '\x1b[0m'
                            time.sleep(2)
                            checkedIN_linecount = 0
                            checkedout = 1

        checkedout = 0

    except KeyboardInterrupt:
            print '\ncaught keyboard interrupt!, bye'
            sys.exit()
