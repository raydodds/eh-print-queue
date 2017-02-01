from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
Abstract class that extends the Django default user to include extra information.
"""
class endUser(models.Model):
    # Allows adding of extra fields to the same object
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Allows admins to permit someone to print
    isAdmin = models.BooleanField(default=False)
    # Allows Computer Chairman to view pertinent information.
    isCC = models.BooleanField(default=False)

    def __str__(self):
        return self.user.last_name+", "+self.user.first_name


"""
Connects the user and endUser at creation.
"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        endUser.objects.create(user=instance)


"""
Log object that makes up the activity log.
"""
class log(models.Model):
    user = models.ForeignKey('endUser', blank=True, null=True)
    event = models.CharField(max_length=50, default="an event happened")
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return str(self.date) + " " + str(self.time) + " " + str(self.user) + ": " + str(self.event)

"""
Class which deals with printing events.
"""
class printEvent(models.Model):
	# Marks the time the print block will begin.
	startTime = models.DateTimeField()

	# Marks the length of the print block.
	duration = models.TimeField()

	# Denotes which user is printing.
	user = models.ForeignKey('enduser', blank=False, null=False)

	# Denotes how many grams of filament were used in the print.
	printAmount = models.IntegerField()

	# Marks whether an admin has approved the print.
	approved = models.BooleanField(default=False)

	
