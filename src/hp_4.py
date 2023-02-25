# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    
    datess = [datetime.strptime(dte, "%Y-%m-%d").strftime('%d %b %Y') for dte in old_dates]
    return datess

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError()
    datesAll = []
    start_date = datetime.strptime(start, '%Y-%m-%d')
    for i in range(n):
        datesAll.append(start_date + timedelta(days=i))
    return datesAll


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    dyas = len(values)
    drls = date_range(start_date, dyas)
    result = list(zip(drls, values))
    return result
def read_bookfile(infile):
    
    fields = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".split(','))
    with open(infile, 'r') as f:
        rdr = DictReader(f, fieldnames=fields)
        allrows = [row for row in rdr]

    allrows.pop(0)

    return allrows

def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    
    data = read_bookfile(infile)
    totalfee = defaultdict(float)
    DTFORMAT = '%m/%d/%Y'
    
    for data1 in data:
        patron = data1['patron_id']
        due = datetime.strptime(data1['date_due'], DTFORMAT)
        returned = datetime.strptime(data1['date_returned'], DTFORMAT)

        days_late = (returned - due).days
        
        totalfee[patron]+= 0.25 * days_late if days_late > 0 else 0.0

    out_list = [
        {'patron_id': p, 'late_fees': f'{f:0.2f}'} for p, f in totalfee.items()
    ]

    with open(outfile, 'w') as f:
        wrtr = DictWriter(f, ['patron_id', 'late_fees'])
        wrtr.writeheader()
        wrtr.writerows(out_list)



# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
