from django.db import models
from settings import URL_PREFIX

class Composer(models.Model):
	first_name = models.CharField('First Name', max_length=32)
	last_name = models.CharField('Last Name', max_length=32)
	
	def __unicode__(self):
		return u"%s, %s" % (self.last_name, self.first_name)
	
	@models.permalink
	def get_absolute_url(self):
		return ('library.views.composer_list', [str(self.id)])
	
	def get_edit_url(self):
		return '%s/admin/library/composer/%d/' % (URL_PREFIX, self.id)
	
	class Meta:
		ordering = ['last_name']

class Arranger(models.Model):
	first_name = models.CharField('First Name', max_length=32)
	last_name = models.CharField('Last Name', max_length=32)

	def __unicode__(self):
		return u"%s, %s" % (self.last_name, self.first_name)
	
	@models.permalink
	def get_absolute_url(self):
		return ('library.views.arranger_list', [str(self.id)])
	
	def get_edit_url(self):
		return '/admin/library/arranger/%d/' % self.id
	
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
	title = models.CharField('Title', max_length=64)
	subtitle = models.CharField('Subtitle (Optional)', max_length=128, blank=True)
	composer = models.ManyToManyField('Composer')
	arranger = models.ManyToManyField('Arranger', blank=True, null=True)
	score = models.ForeignKey('ScoreType', blank=True, null=True)
	difficulty = models.SmallIntegerField('Difficulty Level', choices=DIFFICULTY_CHOICES, blank=True, null=True)
	comment = models.TextField('Comment', max_length=1024, blank=True)

	def __unicode__(self):
		return u"%s" % self.title
	
	@models.permalink
	def get_absolute_url(self):
		return ('piece_detail', (), { 'object_id': self.id })
	
	def get_edit_url(self):
		return '/admin/library/piece/%d/' % self.id
	
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
		
	@models.permalink
	def get_absolute_url(self):
		return ('library.views.group_list', (), {'group_name': self.shortname})
	
	def get_edit_url(self):
		return '/admin/library/cabinetgroup/%d/' % self.id

class Cabinet(models.Model):
	number = models.IntegerField('Cabinet ID Number')
	group = models.ForeignKey('CabinetGroup')

	def __unicode__(self):
		return u"%s >> %s" % (self.group, self.number)
	
	def __int__(self):
		return self.number
	
	@models.permalink
	def get_absolute_url(self):
		return ('library.views.cabinet_list', (), {
			'group_name': self.group.shortname,
			'cabinet_id': str(int(self)),
		})
	
	def get_edit_url(self):
		return '/admin/library/cabinet/%d/' % self.id
	
class Drawer(models.Model):
	cabinet = models.ForeignKey('Cabinet')
	number = models.SmallIntegerField('Drawer Number')
	
	def __unicode__(self):
		return u"%s >> %s" % (self.cabinet, self.number)
	
	def __int__(self):
		return self.number
	
	@models.permalink
	def get_absolute_url(self):
		return ('library.views.drawer_list', (), {
			'group_name': self.cabinet.group,
			'cabinet_id': str(int(self.cabinet)),
			'drawer_id': str(int(self))
		})
	
	def get_edit_url(self):
		return '/admin/library/drawer/%d/' % self.id

class Orchestra(models.Model):
	shortname = models.CharField('Short Name', max_length=5, unique=True)
	name = models.CharField('Full Name', max_length=64)
	
	def __unicode__(self):
		return u"%s" % self.shortname

class Performance(models.Model):
	place = models.TextField('Place', max_length=1024)
	date = models.DateField('Date')
	orchestra = models.ManyToManyField('Orchestra')
	piece = models.ManyToManyField('Piece')
	
	def __unicode__(self):
		return u"%s, %s" % (self.place, self.date)

	@models.permalink
	def get_absolute_url(self):
		return ('performance_detail', (), { 'object_id': self.id })
	
	def get_edit_url(self):
		return '/admin/library/performance/%d/' % self.id
