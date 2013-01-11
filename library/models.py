from django.db import models


class Composer(models.Model):
    first_name = models.CharField('First Name', max_length=32)
    last_name = models.CharField('Last Name', max_length=32)

    def __unicode__(self):
        return u"%s, %s" % (self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name']


class Arranger(models.Model):
    first_name = models.CharField('First Name', max_length=32)
    last_name = models.CharField('Last Name', max_length=32)

    def __unicode__(self):
        return u"%s, %s" % (self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name']


DIFFICULTY_CHOICES = (
    ('0', 'Unknown'),
    ('1', 'Beginner'),
    ('2', 'Intermediate'),
    ('3', 'Advanced'),
    ('4', 'Insane'),
)


class Piece(models.Model):
    id = models.IntegerField('Catalog ID Number', primary_key=True)
    drawer = models.ForeignKey('Drawer')
    title = models.CharField('Title', max_length=256)
    subtitle = models.CharField('Subtitle (Optional)',
                                max_length=128,
                                blank=True)
    composer = models.ManyToManyField('Composer')
    arranger = models.ManyToManyField('Arranger', blank=True, null=True)
    score = models.ForeignKey('ScoreType', blank=True, null=True)
    difficulty = models.SmallIntegerField('Difficulty Level',
                                          choices=DIFFICULTY_CHOICES,
                                          blank=True, null=True)
    comment = models.TextField('Comment', max_length=1024, blank=True)

    def __unicode__(self):
        return u"%d: %s" % (self.id, self.title)

    @property
    def cabinet(self):
        return self.drawer.cabinet

    @property
    def group(self):
        return self.drawer.cabinet.group

    @property
    def scoretype(self):
        return self.score.name

    class Meta:
        ordering = ['title']


class ScoreType(models.Model):
    name = models.CharField('Short Name', max_length=16)
    description = models.CharField('Description', max_length=140)

    def __unicode__(self):
        return u"%s" % self.name


class CabinetGroup(models.Model):
    shortname = models.CharField('Short Name', max_length=5, unique=True)
    description = models.CharField('Description', max_length=140)

    def __unicode__(self):
        return u"%s" % self.shortname

    @property
    def cabinets(self):
        return self.cabinet_set.all()

    @property
    def drawers(self):
        return Drawer.objects.filter(cabinet__in=self.cabinet_set.all())

    class Meta:
        ordering = ['shortname']


class Cabinet(models.Model):
    number = models.IntegerField('Cabinet ID Number')
    group = models.ForeignKey('CabinetGroup')

    def __unicode__(self):
        return u"%s >> %s" % (self.group, self.number)

    def __int__(self):
        return self.number

    @property
    def drawers(self):
        return self.drawer_set.all()

    class Meta:
        ordering = ['group', 'number']


class Drawer(models.Model):
    cabinet = models.ForeignKey('Cabinet')
    number = models.SmallIntegerField('Drawer Number')

    def __unicode__(self):
        return u"%s >> %s" % (self.cabinet, self.number)

    def __int__(self):
        return self.number

    class Meta:
        ordering = ['cabinet', 'number']
    
    @property
    def group(self):
        return self.cabinet.group


class Orchestra(models.Model):
    shortname = models.CharField('Short Name', max_length=5, unique=True)
    name = models.CharField('Full Name', max_length=64)

    def __unicode__(self):
        return u"%s" % self.shortname

    class Meta:
        ordering = ['shortname']


class Performance(models.Model):
    place = models.TextField('Place', max_length=1024)
    date = models.DateField('Date')
    orchestra = models.ManyToManyField('Orchestra')
    piece = models.ManyToManyField('Piece')

    def __unicode__(self):
        return u"%s: %s: %s" % (
            self.date,
            ', '.join([orch.shortname for orch in self.orchestra.all()]),
            self.place)

    class Meta:
        ordering = ['date']
