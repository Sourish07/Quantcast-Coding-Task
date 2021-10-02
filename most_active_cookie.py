import argparse
import datetime

parser = argparse.ArgumentParser(description="Process log files and return most active cooking for specified day")
parser.add_argument('file_name', metavar='file_name', help='Name of log file csv')
parser.add_argument('-d', metavar='date', help='Date to search for in csv')
args = parser.parse_args()
if args.d is None:
    print('Please enter a date. -d')
    quit()

input_date = datetime.datetime.fromisoformat(args.d).date()  # Converting date into Python date object

file = open(args.file_name, "r")
try:
    next(file)  # Skipping headers in log file
except:
    print("File is empty")
    quit()

# Dictionary: Key is the date, value is another dict
# Key of second dict is the cookie name, value is count of how many times its appeared on that date
cookie_dict = {}

# Key is the date, value is tuple
# First element of tuple is max number of times the most common cookie has appeared on that date
# Second element of tuple is a set of most active cookies on that date
max_value_dict = {}

for line in file:
    l = line.strip()  # Removing \n from end of line
    cookie, date = l.split(',')  # Splitting line into cookie and timestamp
    date = datetime.datetime.fromisoformat(date).date()  # Converting date into Python date object

    # Checking if this is the first time seeing date
    if date not in cookie_dict:
        cookie_dict[date] = {}
        max_value_dict[date] = (float('-inf'), set())

    # Checking if this is the first time seeing cookie on above date
    if cookie not in cookie_dict[date]:
        cookie_dict[date][cookie] = 0

    cookie_dict[date][cookie] += 1

    # Checking if current cookie matches or exceeds current max for that date
    if cookie_dict[date][cookie] > max_value_dict[date][0]:
        # If current cookie's count exceeds new max, update max value and create new set with only that cookie
        max_value_dict[date] = (cookie_dict[date][cookie], {cookie})
    elif cookie_dict[date][cookie] == max_value_dict[date][0]:
        # If current cookie's count equals new max, add cookie to set
        max_value_dict[date][1].add(cookie)

if len(max_value_dict) == 0:
    print("No cookies in log file.")
    quit()

# Print each element of the set of most active cookies for that date
for i in max_value_dict[input_date][1]:
    print(i)
