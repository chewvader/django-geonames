import datetime
import os
import re
import sys
import cgi
import urllib.request, urllib.error, urllib.parse, urllib.response
from optparse import make_option

from django.conf import settings
from django.core.management.base import NoArgsCommand

from .compress_geonames import GEONAMES_DATA, GEONAMES_DATA_PC

GEONAMES_DUMPS_URL = getattr(settings,
        'GEONAMES_DUMPS_URL',
        'http://download.geonames.org/export/dump/',
        )
GEONAMES_PC_DUMPS_URL = getattr(settings,
        'GEONAMES_PC_DUMPS_URL',
        'http://download.geonames.org/export/zip/',
        )

def download(url, filepath=False):
    """
    Copy the contents of a file from a given URL to a local file.
    """
    filepath = filepath or url.split('/')[-1]

    web_file = urllib.request.urlopen(url)

    if os.name == "nt":
        path_delimiter = '\\'
    else:
        path_delimiter = '/'

    dir = path_delimiter.join(filepath.split(path_delimiter)[:-1])
    if not os.path.isdir(dir):
        os.makedirs(dir)

    # check size of files
    web_file_info = web_file.info()
    web_file_size = int(web_file_info.get("Content-Length"))
    if os.path.isfile(filepath):
        existing_file = open(filepath, "r")
        existing_file_size = os.path.getsize(filepath)#len(existing_file.read())
        print(existing_file_size, web_file_size)
        if existing_file_size == web_file_size:
            existing_file.close()
            web_file.close()
            print('Skipping. File sizes match.')
            return

    local_file = open(filepath, 'wb')
    readSize = 102400
    bytesRead = 0
    while True:
        read = web_file.read(readSize)
        bytesRead += len(read)
        if not read:
            break

        local_file.write(read)

        progress = 'Downloaded %s of %s' % (bytesRead, web_file_size)
        sys.stdout.write(progress)
        sys.stdout.write('\b' * len(progress))
        sys.stdout.flush()

    sys.stdout.write('\n')
    web_file.close()
    local_file.close()


class Command(NoArgsCommand):
    help = 'Download all data files from geonames to data dir.'

    option_list = NoArgsCommand.option_list + (
        make_option('-t', '--time', action='store_true', dest='time', default=False,
                    help='Print the total time in running this command'),
        make_option('--country', action='store', dest='country', default=False,
                    help='Download only data for specified country.'),
        make_option('--no-alternates', action='store_true', dest='no_alternates', default=False,
                    help='Disable loading of the Geonames alternate names data.'),
        make_option('--no-geonames', action='store_true', dest='no_geonames', default=False,
                    help='Disable loading of the Geonames data.'),
        make_option('--no-postalcodes', action='store_true', dest='no_postalcodes', default=False,
                    help='Disable loading of the postal codes data.'),
    )

    def handle_noargs(self, **options):
        if options['time']:
            start_time = datetime.datetime.now()

        response = urllib.request.urlopen(urllib.request.Request(url=GEONAMES_DUMPS_URL))

        _, params = cgi.parse_header(response.headers.get('Content-Type', ''))
        text = response.read().decode(params['charset'])
        files = re.findall(r'\<a href="(.+\.(?:txt|zip))"\>', text)
        for file in files:

            if options['country'] and file != '%s.zip' % options['country'] \
                or options['no_geonames'] and file == 'allCountries.zip' \
                or options['no_alternates'] and file == 'alternateNames.zip' \
                or not options['country'] and len(file) == 6:
                    continue

            print('\nStart download "%s" file' % file)
            download(urllib.parse.urljoin(GEONAMES_DUMPS_URL, file),
                     os.path.join(GEONAMES_DATA, file))

        if options['no_postalcodes'] == False:
            print('\nLooking for postalcode data to download')
            req = urllib.request.Request(url=GEONAMES_PC_DUMPS_URL)
            postalcodeResponse = urllib.request.urlopen(req)

            _, postalcodeResponse_params = cgi.parse_header(postalcodeResponse.headers.get('Content-Type', ''))
            postalcodeResponse_text = postalcodeResponse.read().decode(postalcodeResponse_params['charset'])
            postalcodeFiles = re.findall(r'\<a href="(.+\.(?:txt|zip))"\>',
                                         postalcodeResponse_text)
            for file in postalcodeFiles:
                if file != 'allCountries.zip':
                    continue

                print('\nStart download "%s" file' % file)
                download(urllib.parse.urljoin(GEONAMES_PC_DUMPS_URL, file),
                         os.path.join(GEONAMES_DATA_PC, file))

        if options['time']:
            print('\nCompleted in %s' % (datetime.datetime.now() - start_time))
