from django.db import models
from django.urls import reverse
from student.models import Session
from Accounts.models import Account


class Event(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
	title = models.CharField(max_length=200, unique=True)
	description = models.TextField()
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	created_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('event-detail', args=(self.id,))

	@property
	def get_html_url(self):
		url = reverse('event-detail', args=(self.id,))
		return f'<a href="{url}"> {self.title} </a>'


class EventMember(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	session = models.ForeignKey(Session,on_delete=models.CASCADE)


	class Meta:
		unique_together = ['event','session']


	def __str__(self):
		return str(self.session)
