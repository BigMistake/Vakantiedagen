import csv
import os
import datetime
from datetime import timedelta

now = datetime.datetime.now()
directory = "Folder containing CSV files"
days = []
# These are the holiday dates in that my company that are actually counted: Nieuwjaarsdag, 1e en 2e Paasdag, Koningsdag, Hemelvaartsdag, 1e en 2e Pinksterdag, 1e en 2e Kerstdag.
holidays = ["2016-01-01","2016-03-27","2016-03-28","2016-04-27","2016-05-05","2016-05-15","2016-05-16","2016-12-25","2016-12-26",
              "2017-01-01","2017-04-16","2017-04-17","2017-04-27","2017-05-25","2017-06-04","2017-06-05","2017-12-25","2017-12-26",
              "2018-01-01","2018-04-01","2018-04-02","2018-04-27","2018-05-10","2018-05-20","2018-05-21","2018-12-25","2018-12-26",
              "2019-01-01","2019-04-21","2019-04-22","2019-04-27","2019-05-30","2019-06-09","2019-06-10","2019-12-25","2019-12-26",
              "2020-01-01","2020-04-12","2020-04-13","2020-04-27","2020-05-21","2020-05-31","2020-06-01","2020-12-25","2020-12-26"]
files = os.listdir(directory)

for file in files:
    with open(directory + file ) as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            # There's a couple of different types of entries in the CSV's, we're looking for the one that indicated time off was taken, here called "Opname".
            if row[4] == "Opname":
                number = row[0]
                start = datetime.datetime.strptime(row[5], '%d-%m-%Y').date()
                end = datetime.datetime.strptime(row[6], '%d-%m-%Y').date()
                amount = row[7]

                if (end - start).days == 0:
                    # If it's a single day
                    date = start.strftime('%Y-%m-%d')
                    entry = [number, date, amount]
                    days.append(entry)
                else:
                    # If it's multiple days
                    difference = ((end - start).days + 1)
                    amountdays = ((end - start).days + 1)

                    # Because we need to filter out the holidays we loop over the days twice. First to check how many days are actually personally taken off
                    # ( because we need to divide the amount of hours by the amount of days), a second time to add them to the list.
                    for i in range(difference):
                        date = (start + timedelta(days=i)).strftime('%Y-%m-%d')
                        if date in holidays:
                            amountdays -= 1
                        elif (start + timedelta(days=i)).weekday() > 4:
                            amountdays -= 1

                    for i in range(difference):
                        date = (start + timedelta(days=i)).strftime('%Y-%m-%d')
                        if (date not in holidays) and (start + timedelta(days=i)).weekday() < 5:
                            uren = float(amount.replace(",", ".")) / int(
                                amountdays)
                            entry = [number, date, ('%.2f' % uren).replace(".",",")]
                            days.append(entry)

with open('vacationdays' + str(now.year) + '.csv', mode='w', newline='') as vacationdays:
    vacation_writer = csv.writer(vacationdays)
    vacation_writer.writerow(["Employee","Date","Amount"])

    for day in days:
        vacation_writer.writerow(day)