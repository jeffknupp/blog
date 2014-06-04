from flask import Flask

app = Flask(__name__)

AIRPORT_LOCATIONS = dict()
NORMALIZED_AIRPORT_NAMES = dict()


def load_airport_locations(filename):
    """Populate airport latitude and longitude data from given file.

    The list of US airports is short enough that we can simply read them in at
    startup and keep them in memory for the app's duration. If it were
    considerably larger we would use a database, but that's overkill here.
    """
    with open(filename, 'r') as file_handle:
        for line in file_handle:
            fields = line.split(',')
            name, code, latitude, longitude = fields[1].strip('\"'), fields[4].strip('\"'), fields[-5], fields[-4]
            AIRPORT_LOCATIONS[code] = (float(latitude), float(longitude))
            NORMALIZED_AIRPORT_NAMES[code] = ('{} ({})'.format(name, code), code)
            NORMALIZED_AIRPORT_NAMES[name] = ('{} ({})'.format(name, code), code)


if __name__ == '__main__':
    load_airport_locations('us_airports.txt')
    print NORMALIZED_AIRPORT_NAMES['LAX']
