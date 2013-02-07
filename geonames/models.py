from django.contrib.gis.db import models


class Admin1Code(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=58)

    objects = models.GeoManager()

    def __unicode__(self):
        return u': '.join([unicode(self.code), unicode(self.name)])


class Admin2Code(models.Model):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=46)

    objects = models.GeoManager()

    def __unicode__(self):
        return u': '.join([unicode(self.code), unicode(self.name)])


class TimeZone(models.Model):
    tzid = models.CharField(max_length=30)
    gmt_offset = models.FloatField()
    dst_offset = models.FloatField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.tzid


class GeonameManager(models.GeoManager):
    def countries(self, *args, **kwargs):
        """
        Filter returns only countries
        """
        return self.filter(fcode__in=['PCLI']).filter(*args, **kwargs)

    def continents(self, *args, **kwargs):
        """
        Filter returns only continents
        """
        return self.filter(fcode__in=['CONT']).filter(*args, **kwargs)

    def cities(self, *args, **kwargs):
        """
        Filter returns only cities and other populated places
        """
        return self.filter(fcode__in=['PPL']).filter(*args, **kwargs)


class Geoname(models.Model):
    geonameid = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200, db_index=True)
    alternates = models.TextField(blank=True)
    fclass = models.CharField(max_length=1, db_index=True)
    fcode = models.CharField(max_length=10, db_index=True)
    country = models.CharField(max_length=2, blank=True, db_index=True)
    cc2 = models.CharField('Alternate Country Code', max_length=60, blank=True)
    admin1 = models.CharField(max_length=20, blank=True, db_index=True)
    admin2 = models.CharField(max_length=80, blank=True, db_index=True)
    admin3 = models.CharField(max_length=20, blank=True, db_index=True)
    admin4 = models.CharField(max_length=20, blank=True, db_index=True)
    population = models.BigIntegerField(db_index=True)
    elevation = models.IntegerField(db_index=True)
    topo = models.IntegerField(db_index=True)
    timezone = models.CharField(max_length=30, blank=True)
    moddate = models.DateField('Date of Last Modification')
    point = models.PointField(null=True, geography=True, spatial_index=True)

    objects = GeonameManager()

    def __unicode__(self):
        return self.name

    def is_country(self):
        return self.fcode == 'PCLI'

    def is_continent(self):
        return self.fcode == 'CONT'

    def is_populated(self):
        return self.fcode == 'PPL'

    def get_country(self):
        if not self.is_country():
            try:
                return self.__class__.objects.get(
                    fcode='PCLI', country=self.country)
            except self.__class__.DoesNotExist:
                return None
        else:
            return self

    class Meta:
        ordering = ('name', 'country')

# class LocalName(models.Model):
#     uuid = UUIDField(auto=True)
#     language = models.CharField(max_length=20, db_index=True)
#     name = models.CharField(max_length=255)
#     value = models.TextField()
# 
#     def __unicode__(self):
#         return self.name


class Alternate(models.Model):
    alternateid = models.PositiveIntegerField(primary_key=True, unique=True)
    geoname = models.ForeignKey(Geoname, related_name='alternate_names')
    isolanguage = models.CharField(max_length=7)
    variant = models.CharField(max_length=200, db_index=True)
    preferred = models.BooleanField(db_index=True)
    short = models.BooleanField()

    objects = models.GeoManager()

    class Meta:
        ordering = ('-preferred',)

    def __unicode__(self):
        return self.geoname.name


class PostalCode(models.Model):
    countrycode = models.CharField(max_length=2)
    postalcode = models.CharField(max_length=20)
    placename = models.CharField(max_length=180)
    admin1name = models.CharField(max_length=100)
    admin1code = models.CharField(max_length=20)
    admin2name = models.CharField(max_length=100)
    admin2code = models.CharField(max_length=20)
    admin3name = models.CharField(max_length=100)
    admin3code = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    accuracy = models.SmallIntegerField()

    objects = models.GeoManager()

    def __unicode__(self):
        return self.placename
