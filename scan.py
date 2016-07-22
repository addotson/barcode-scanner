import time
import sys

now=time.localtime(time.time())
currentmonth=now.tm_mon
currentday=now.tm_mday
currentyear=now.tm_year
filename = "{0}_{1}_{2}_barcode-log.csv".format(currentyear, currentmonth, currentday)

#### informative messaging for starting storage file
print "Opening ",filename, " for appending..."
print "ready to read and storing barcodes..."
file=open(filename,"a")
file.write("Time,Barcode\n")
file.close()

while True:
    try:
        #get current time
        now=time.localtime(time.time())
        pt=time.asctime(now)  #formatted time for file
        currentmonth=now.tm_mon
        currentday=now.tm_mday
        currentyear=now.tm_year

        barcode = sys.stdin.readline().rstrip()

        #open file to append
        file=open(filename,"a")
        #add first column date/time stamp
        file.write(pt)
        #add next columns with raw reading, and converted voltage
        file.write(",%s\n" % (barcode))
        file.close()
        #if MM/DD/YR changes, update filename
        #this translates to a new file every day
        ##!!!!header row is dropped from subsequent days
        filename = "{0}_{1}_{2}_barcode-log.csv".format(currentyear, currentmonth, currentday)

    except KeyboardInterrupt:
        print '\ncaught keyboard interrupt!, bye'
        sys.exit()
