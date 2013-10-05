from django.db import models


class Artist(models.Model):
    first_name = models.CharField('First Name', max_length=64)
    last_name = models.CharField('Last Name', max_length=64)

    def __unicode__(self):
        return u'{s.last_name}, {s.first_name}'.format(s=self)

    class Meta:
        ordering = ('last_name', 'first_name')



class Piece(models.Model):
    DIFFICULTY_CHOICES = (
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Insane'),
    )

    id = models.IntegerField('Catalog ID Number', primary_key=True)
    container = models.ForeignKey('Container', verbose_name='Container')
    title = models.CharField('Title', max_length=256)
    subtitle = models.CharField('Subtitle (Optional)',
                                max_length=128,
                                blank=True)
    composers = models.ManyToManyField('Artist',
                                       verbose_name='Artists (Composer)',
                                       db_table='library_piece_composer',
                                       related_name='pieces_composed')
    arrangers = models.ManyToManyField('Artist',
                                       verbose_name='Artists (Arranger)',
                                       db_table='library_piece_arranger',
                                       blank=True, null=True,
                                       related_name='pieces_arranged')
    score = models.ForeignKey('ScoreType', verbose_name='Type of Score',
                              blank=True, null=True)
    difficulty = models.SmallIntegerField('Difficulty Level',
                                          choices=DIFFICULTY_CHOICES,
                                          blank=True, null=True)
    comment = models.TextField('Comment', max_length=1024, blank=True)

    def __unicode__(self):
        return u"%d: %s" % (self.id, self.title)

    @property
    def scoretype(self):
        return self.score.name

    @property
    def path(self):
        return unicode(self.container)

    class Meta:
        ordering = ['title']


class ScoreType(models.Model):
    name = models.CharField('Short Name', max_length=16)
    description = models.CharField('Description', max_length=140)

    def __unicode__(self):
        return u"%s" % self.name


class Container(models.Model):
    slug = models.SlugField('Slug', max_length=32)
    name = models.CharField('Name', max_length=256)
    description = models.TextField('Description', null=True, blank=True)
    parent = models.ForeignKey('Container', related_name='children',
                               null=True, blank=True)
    number = models.PositiveSmallIntegerField('Number', null=True, blank=True)

    def __unicode__(self):
        if self.parent:
            return u'{} >> {}'.format(self.parent, self.name)
        else:
            return u'{}'.format(self.name)


class Orchestra(models.Model):
    shortname = models.CharField('Short Name', max_length=5, unique=True)
    name = models.CharField('Full Name', max_length=64)

    def __unicode__(self):
        return u"%s" % self.shortname

    class Meta:
        ordering = ['shortname']


class Performance(models.Model):
    place = models.TextField('Place')
    date = models.DateField('Date')
    orchestras = models.ManyToManyField(
        'Orchestra', verbose_name='Orchestras',
        db_table='library_performance_orchestra')
    pieces = models.ManyToManyField(
        'Piece', verbose_name='Pieces', db_table='library_performance_piece')
    comments = models.TextField('Comments')

    def __unicode__(self):
        return u"%s: %s: %s" % (
            self.date,
            ', '.join([orch.shortname for orch in self.orchestra.all()]),
            self.place)

    class Meta:
        ordering = ['date']
