from django.db import models
from django.utils.timezone import utc
from django.contrib.auth.models import User
import datetime


EventCategories = [
  ("7-8", "Class 7 to 8"),
  ("9-10", "Class 9 to 10"),
  ("11-12", "Class 11 to 12"),
]

# Create your models here.
class Event(models.Model):
  name = models.CharField(max_length=200)
  categories = models.CharField(max_length=100, choices=EventCategories)
  TimeOfEvent = models.DateTimeField("Date and Time of Event only in UTC (IST not supported for server)", auto_now_add=False)
  timeLimit = models.FloatField("Time Limit (hrs only)", default=0.0)


  def __str__(self):
    return self.name + " " + self.categories

  def get_time_diff(self):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    timediff = now - self.TimeOfEvent
    return timediff.total_seconds()

  def check_event_started(self):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    timeDiff = (now - self.TimeOfEvent).total_seconds()

    if timeDiff >= 0:
      return True

    return False 

  def can_participate(self):
    if not self.check_event_started():
      return False

    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    time_seconds = (now -self.TimeOfEvent).total_seconds()

    time_hrs = time_seconds / 3600

    if time_hrs < self.timeLimit:
      return True
    
    return False


class Problems(models.Model):
  name = models.CharField(max_length=200)
  event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="prob_event")

  def upload_path(self, filename):
    return f'{self.name}/{filename}' 
 
  problemHtml = models.FileField("Problem statement in png", upload_to=upload_path, default="")
  mainFile = models.FileField("Problem main execution file", upload_to=upload_path, default="")
  userFile = models.FileField("User execution code file", upload_to=upload_path, default="")
  test_module = models.FileField("Test cases file (txt)", upload_to=upload_path, default="")
  expected_output = models.FileField("Expected Answer (txt)", upload_to=upload_path, default="")

  def __str__(self):
    string = ""
    string += self.name + " - "
    string += self.event.name

    return string

class ProblemsSolved(models.Model):
  problem = models.ForeignKey(Problems, on_delete=models.CASCADE, related_name="problem_solved")
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solved_user')
  solved = models.BooleanField("Has Solved", default=False)

  def __str__(self):
    string = ""
    string += self.user.username + " - "
    string += self.problem.name + " - "
    string += str(self.solved)

    return string


class Leaderboard(models.Model):
  problem = models.ForeignKey(Problems, on_delete=models.CASCADE, related_name="problem_leaderboard")
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_leaderboard")
  problems_solved = models.IntegerField("solved problems", default=0)
  seconds_taken = models.FloatField("seconds taken", default=0.0)

  def __str__(self):
    return self.user.username + " " + self.problem.name

