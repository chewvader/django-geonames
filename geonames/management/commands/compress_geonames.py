import datetime
import decimal
import io
import gzip
import os
import sys
import zipfile
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.conf import settings

from geonames import models

GEONAMES_DATA = getattr(settings,
        'GEONAMES_DATA',
        os.path.abspath(os.path.join(os.path.dirname(models.__file__), 'data'))
        )
GEONAMES_DATA_PC = getattr(settings,
        'GEONAMES_DATA_PC',
        os.path.join(GEONAMES_DATA, 'pc'),
        )

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('-t', '--time', action='store_true', dest='time', default=False,
                    help='Print the total time in running this command'),
        make_option('-l', '--lengths', action='store_true', dest='lengths', default=False,
                    help='Print the lengths for each of the fields.'),
        make_option('--no-countries', action='store_true', dest='no_countries', default=False,
                    help='Do not perform compression on allCountries.zip'),
        make_option('--no-alternates', action='store_true', dest='no_alternates', default=False,
                    help='Do not perform compression on alternateNames.zip'),
        make_option('--no-postalcodes', action='store_true', dest='no_postalcodes', default=False,
                    help='Do not perform compression on postalcodes allCountries.zip'),
    )
    clear_line = chr(27) + '[2K' + chr(27) +'[G'

    def allCountries(self, **options):

        print("Processing allCountries.zip")

        zf = zipfile.ZipFile(os.path.join(GEONAMES_DATA, 'allCountries.zip'))
        gzf = gzip.GzipFile(os.path.join(GEONAMES_DATA, 'allCountries.gz'), 'w')

        in_fields = ['geonameid', 'name', 'asciiname', 'alternates', 'latitude', 'longitude',
                     'fclass', 'fcode', 'country_code', 'cc2',
                     'admin1', 'admin2', 'admin3', 'admin4',
                     'population', 'elevation', 'topo', 'timezone', 'mod_date']
        out_fields = [f for f in in_fields if not f in ('latitude', 'longitude')]
        len_fields = ['name', 'asciiname', 'alternates', 'fclass', 'fcode', 'country_code',
                      'cc2', 'admin1', 'admin2', 'admin3', 'admin4', 'timezone']
        if options['lengths']:
            lengths = dict([(f, 0) for f in len_fields])

        unzipped = zf.read('allCountries.txt')
        file_size = len(unzipped)

        buf = io.BytesIO(unzipped)
        size_counter = 0
        display_percent = 0
        while True:
            line = buf.readline()
            size_counter += len(line)
            line = line.decode('utf8')

            if line == '':
                break

            if line:
                row = dict(list(zip(in_fields, list(map(str.strip, line.split('\t'))))))
                if options['lengths']:
                    for k in len_fields:
                        lengths[k] = max(len(row[k]), lengths[k])

                # fixing trailing slash problem in geonames data
                try:
                    for k in len_fields:
                        while row[k][-1:] == "\\":
                            row[k] = row[k][0:-1]
                except:
                    pass

                try:
                    # Setting integers to 0 so they won't have to be NULL.
                    for key in ('population', 'elevation', 'topo'):
                        if not row[key]:
                            row[key] = '0'

                    # Getting the EWKT for the point -- has to be EWKT or else
                    # the insertion of the point will raise a constraint error for
                    # for a non-matching ID.
                    wkt = 'SRID=4326;POINT(%s %s)' % (row['longitude'], row['latitude'])
                except KeyError:
                    sys.stderr.write('Invalid row (line %d):\n' % i)
                    sys.stderr.write('%s\n' % str(row))
                else:
                    new_line = '\t'.join([row[k] for k in out_fields])
                    new_line += '\t%s\n' % wkt
                    gzf.write(bytes(new_line, 'UTF-8'))

            percent = str(decimal.Decimal((size_counter / file_size) * 100).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_UP))
            if percent != display_percent:
                display_percent = percent
                progress = 'Processed %s %%' % (percent)
                sys.stdout.write(progress)
                sys.stdout.write('\b' * len(progress))
                sys.stdout.flush()

        gzf.close()

        sys.stdout.write('\n')

        if options['lengths']:
            for fld in len_fields:
                sys.stdout.write('%s:\t%d\n' % (fld, lengths[fld]))

    def alternateNames(self, **options):

        print("Processing alternateNames.zip")

        zf = zipfile.ZipFile(os.path.join(GEONAMES_DATA, 'alternateNames.zip'))
        gzf = gzip.GzipFile(os.path.join(GEONAMES_DATA, 'alternateNames.gz'), 'w')

        in_fields = ['alternateid', 'geonameid', 'isolanguage', 'variant', 'preferred', 'short', 'colloquial', 'historic']
        bool_fields = ['preferred', 'short', 'colloquial', 'historic']
        len_fields = ['isolanguage', 'variant']
        out_fields = in_fields
        if options['lengths']:
            lengths = dict([(f, 0) for f in len_fields])

        unzipped = zf.read('alternateNames.txt')
        file_size = len(unzipped)

        buf = io.BytesIO(unzipped)
        size_counter = 0
        display_percent = 0
        while True:
            line = buf.readline()
            size_counter += len(line)
            line = line.decode('utf8')

            if line == '':
                break

            if line:
                row = dict(list(zip(in_fields, list(map(str.strip, line.split('\t'))))))
                for bool_field in bool_fields:
                    if row[bool_field]:
                        row[bool_field] = '1'
                    else:
                        row[bool_field] = '0'

                if options['lengths']:
                    for k in len_fields:
                        lengths[k] = max(len(row[k]), lengths[k])

                # fixing trailing slash problem in geonames data
                try:
                    for k in len_fields:
                        while row[k][-1:] == "\\":
                            row[k] = row[k][0:-1]
                except:
                    pass


                new_line = '\t'.join([row[k] for k in out_fields])
                new_line += '\n'
                gzf.write(bytes(new_line, 'UTF-8'))

                percent = str(decimal.Decimal((size_counter / file_size) * 100).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_UP))
                if percent != display_percent:
                    display_percent = percent
                    progress = 'Processed %s %%' % (percent)
                    sys.stdout.write(progress)
                    sys.stdout.write('\b' * len(progress))
                    sys.stdout.flush()

        gzf.close()

        sys.stdout.write('\n')

        if options['lengths']:
            for fld in len_fields:
                sys.stdout.write('%s:\t%d\n' % (fld, lengths[fld]))

    def postalCodes(self, **options):

        print("Processing Postal Codes allCountries.zip")

        zf = zipfile.ZipFile(os.path.join(GEONAMES_DATA_PC, 'allCountries.zip'))
        gzf = gzip.GzipFile(os.path.join(GEONAMES_DATA_PC, 'allCountries.gz'), 'w')

        in_fields = ['countrycode', 'postalcode', 'placename', 'admin1name', 'admin1code', 'admin2name', 'admin2code', 'admin3name', 'admin3code', 'latitude', 'longitude', 'accuracy']
        len_fields = ['countrycode', 'postalcode', 'placename', 'admin1name', 'admin1code', 'admin2name', 'admin2code', 'admin3name', 'admin3code']
        out_fields = in_fields
        if options['lengths']:
            lengths = dict([(f, 0) for f in len_fields])

        unzipped = zf.read('allCountries.txt')
        file_size = len(unzipped)

        buf = io.BytesIO(unzipped)
        size_counter = 0
        display_percent = 0
        while True:
            line = buf.readline()
            size_counter += len(line)
            line = line.decode('utf8')

            if line == '':
                break

            if line:
                row = dict(list(zip(in_fields, list(map(str.strip, line.split('\t'))))))
                if options['lengths']:
                    for k in len_fields:
                        lengths[k] = max(len(row[k]), lengths[k])

                # fixing trailing slash problem in geonames data
                try:
                    for k in len_fields:
                        while row[k][-1:] == "\\":
                            row[k] = row[k][0:-1]
                except:
                    pass

                if row['latitude'] == '' or row['longitude'] == '':
                    continue

                if row['accuracy'] == '':
                    row['accuracy'] = '0'

                new_line = '\t'.join([row[k] for k in out_fields])
                new_line += '\n'
                gzf.write(bytes(new_line, 'UTF-8'))

                percent = str(decimal.Decimal((size_counter / file_size) * 100).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_UP))
                if percent != display_percent:
                    display_percent = percent
                    progress = 'Processed %s %%' % (percent)
                    sys.stdout.write(progress)
                    sys.stdout.write('\b' * len(progress))
                    sys.stdout.flush()

        gzf.close()

        sys.stdout.write('\n')

        if options['lengths']:
            for fld in len_fields:
                sys.stdout.write('%s:\t%d\n' % (fld, lengths[fld]))

    def handle_noargs(self, **options):
        if options['time']:
            start_time = datetime.datetime.now()

        if not options['no_countries']:
            self.allCountries(**options)

        if not options['no_alternates']:
            self.alternateNames(**options)

        if not options['no_postalcodes']:
            self.postalCodes(**options)

        if options['time']:
            sys.stdout.write('\nCompleted in %s\n' % (datetime.datetime.now() - start_time))
