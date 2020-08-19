import csv, arrow
from pandas import read_csv

your_csv_filename = 'example.csv'

def prep_csv(filename):
   df = read_csv(filename)
   df.columns = ['artist','album','track','date']
   df.to_csv(filename, index=False)
   process_csv(filename)

def process_csv(filename):
    artists = {}
    dates = []

    with open(filename, 'rt', encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)

        for row in csv_reader:
            artist = row['artist']
            month = arrow.get(row['date'], 'DD MMM YYYY HH:mm').format('MMMM')
            year = arrow.get(row['date'], 'DD MMM YYYY HH:mm').format('YYYY')
            date = f'{year} {month}'
            if artist not in artists:
                artists[artist] = {}
            if date not in artists[artist]:
                artists[artist][date] = 1
            else:
                artists[artist][date] += 1
            if date not in dates:
                dates.insert(0, date)

    artistsTotal = {}
    for artist in artists:
        sum = 0
        artistsTotal[artist] = {'artist':artist}
        for date in dates:
            if date in artists[artist]:
                sum += artists[artist][date]
                artistsTotal[artist][date] = sum
    
    dates.insert(0, 'artist')
    with open(f'{filename}-processed.csv', 'w', encoding="utf-8") as out:
        csvOut = csv.DictWriter(out, dates)
        csvOut.writeheader()
        for artist in artistsTotal:
            csvOut.writerow(artistsTotal[artist])

prep_csv(your_csv_filename)
