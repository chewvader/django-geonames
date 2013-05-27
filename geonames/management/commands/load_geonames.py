import datetime
import os
from optparse import make_option

from django.core.management import call_command
from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.db import router

from compress_geonames import GEONAMES_DATA, GEONAMES_DATA_PC
from geonames import models as m

Alternate = m.Alternate
Geoname = m.Geoname
PostalCode = m.PostalCode

GEONAMES_SQL = os.path.abspath(
    os.path.join(os.path.dirname(m.__file__), 'sql'))

def get_cmd_options(model):
    "Obtains the command-line PostgreSQL connection options for shell commands."
    # The db_name parameter is optional
    options = ''
    db_settings = settings.DATABASES[router.db_for_write(model)]
    if db_settings['NAME']:
        options += '-d %s ' % db_settings['NAME']
    if db_settings['USER']:
        options += '-U %s ' % db_settings['USER']
    if db_settings['HOST']:
        options += '-h %s ' % db_settings['HOST']
    if db_settings['PORT']:
        options += '-p %s ' % db_settings['PORT']
    if db_settings['PASSWORD']:
        os.environ['PGPASSWORD'] = db_settings['PASSWORD']
        
    return options, {'db_opts': options,}


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('-t', '--time', action='store_true', dest='time', default=False,
                    help='Print the total time in running this command'),
        make_option('--no-alternates', action='store_true', dest='no_alternates', default=False,
                    help='Disable loading of the Geonames alternate names data.'),
        make_option('--no-geonames', action='store_true', dest='no_geonames', default=False,
                    help='Disable loading of the Geonames data.'),
        make_option('--no-postalcodes', action='store_true', dest='no_postalcodes', default=False,
                    help='Disable loading of the postal code data.'),
    )

    def handle_noargs(self, **options):
        if options['time']:
            start_time = datetime.datetime.now()

        # Making sure the db tables exist.
        call_command('syncdb')
        db_table = Geoname._meta.db_table

        db_opts, fromfile_args = get_cmd_options(Geoname)

        fromfile_cmd = 'psql %(db_opts)s -f %(sql_file)s'

        ### COPY'ing into the Geonames table ###

        # Executing a shell command that pipes the unzipped data to PostgreSQL
        # using the `COPY` directive.  This builds the database directly from
        # the file made by the `compress_geonames` command, and eliminates the
        # overhead from using the ORM.  Moreover, copying from a gzipped file
        # reduces disk I/O.
        copy_sql = "COPY %s (geonameid,name,alternates,fclass,fcode,country,cc2,admin1,admin2,admin3,admin4,population,elevation,topo,timezone,moddate,point) FROM STDIN;" % db_table
        copy_cmd = 'gunzip -c %(gz_file)s | psql %(db_opts)s -c "%(copy_sql)s"'
        copy_args = {
            'gz_file': os.path.join(GEONAMES_DATA, 'allCountries.gz'),
            'db_opts': db_opts,
            'copy_sql': copy_sql,
        }

        # Printing the copy command and executing it.
        if not options['no_geonames']:
            fromfile_args['sql_file'] = os.path.join(GEONAMES_SQL, 'drop_geoname_indexes.sql')
            print(fromfile_cmd % fromfile_args)
            os.system(fromfile_cmd % fromfile_args)
            print(copy_cmd % copy_args)
            os.system(copy_cmd % copy_args)
            fromfile_args['sql_file'] = os.path.join(GEONAMES_SQL, 'create_geoname_indexes.sql')
            print(fromfile_cmd % fromfile_args)
            os.system(fromfile_cmd % fromfile_args)
            print('Finished PostgreSQL `COPY` from Geonames all countries data file.')

        ### COPY'ing into the Geonames alternate table ###

        db_table = Alternate._meta.db_table

        db_opts, fromfile_args = get_cmd_options(Alternate)

        copy_sql = "COPY %s (alternateid,geoname_id,isolanguage,variant,preferred,short) FROM STDIN;" % db_table
        copy_cmd = 'gunzip -c %(gz_file)s | psql %(db_opts)s -c "%(copy_sql)s"'
        copy_args = {
            'gz_file': os.path.join(GEONAMES_DATA, 'alternateNames.gz'),
            'db_opts': db_opts,
            'copy_sql': copy_sql,
        }

        if not options['no_alternates']:
            fromfile_args['sql_file'] = os.path.join(GEONAMES_SQL, 'drop_alternate_indexes.sql')
            print(fromfile_cmd % fromfile_args)
            os.system(fromfile_cmd % fromfile_args)
            print(copy_cmd % copy_args)
            os.system(copy_cmd % copy_args)
            print('Finished PostgreSQL `COPY` from Geonames alternate names data file.')
            fromfile_args['sql_file'] = os.path.join(GEONAMES_SQL, 'create_alternate_indexes.sql')
            print(fromfile_cmd % fromfile_args)
            os.system(fromfile_cmd % fromfile_args)

            # cursor = connection.cursor()
            # list_sql = []
            # insert_sql = []
            # for language in settings.LANGUAGES:
            #     insert_sql.append('name_%s' % language[0])
            # for language in settings.LANGUAGES:
            #     list_sql.append("(SELECT variant FROM geonames_alternate "
            #                     "WHERE geoname_id=geonameid AND isolanguage='%s' "
            #                     "ORDER BY preferred DESC LIMIT 1) AS name_%s" %
            #                     (language[0], language[0]))
            # denorm_sql = (
            #     "INSERT INTO geonames_localname (geoname_id, %s) "
            #     "SELECT geonameid, %s FROM geonames_geoname" %
            #     (", ".join(insert_sql), ", ".join(list_sql)))
            # cursor.execute(denorm_sql)


        ### COPY'ing into the Geonames alternate table ###
        db_table = PostalCode._meta.db_table

        db_opts, fromfile_args = get_cmd_options(PostalCode)

        copy_sql = "COPY %s (countrycode, postalcode, placename, admin1name, admin1code, admin2name, admin2code, admin3name, admin3code, latitude, longitude, accuracy) FROM STDIN;" % db_table
        copy_cmd = 'gunzip -c %(gz_file)s | psql %(db_opts)s -c "%(copy_sql)s"'
        copy_args = {
            'gz_file': os.path.join(GEONAMES_DATA_PC, 'allCountries.gz'),
            'db_opts': db_opts,
            'copy_sql': copy_sql,
        }

        if not options['no_postalcodes']:
            fromfile_args['sql_file'] = os.path.join(GEONAMES_SQL, 'drop_postalcode_indexes.sql')
            print(fromfile_cmd % fromfile_args)
            os.system(fromfile_cmd % fromfile_args)
            print(copy_cmd % copy_args)
            os.system(copy_cmd % copy_args)
            print('Finished PostgreSQL `COPY` from Geonames postal code data file.')
            fromfile_args['sql_file'] = os.path.join(GEONAMES_SQL, 'create_postalcode_indexes.sql')
            print(fromfile_cmd % fromfile_args)
            os.system(fromfile_cmd % fromfile_args)

        # Done
        if options['time']:
            print('\nCompleted in %s' % (datetime.datetime.now() - start_time))
