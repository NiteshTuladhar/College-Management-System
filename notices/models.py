from django.db import models
from Accounts.models import Account
from student.models import Session, Course, Batch


type = [('Notice','Notice'),('Announcement','Announcement')]
class NoticeBoard(models.Model):

	notice_annoucer = models.ForeignKey(Account, on_delete=models.CASCADE)
	notice_title = models.CharField(max_length=100)
	notice_description = models.TextField()
	notice_date = models.DateTimeField(auto_now=True)
	semester = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
	type = models.CharField(max_length=30, choices=type, default=type[1])
	

	def __str__(self):

		return self.notice_title



