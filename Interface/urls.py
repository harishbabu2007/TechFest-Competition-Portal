from django.conf.urls import url
from .views import index, rules, problems, solve_event_problem
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
  path("", index, name="interface-index"),
  path("events/rules/<int:id>", rules, name="interface-rules"),
  path("events/problems/<int:id>", problems, name="interface-problems"),
  path("events/<int:event_id>/problem/<int:problem_id>", solve_event_problem, name="interface-solve")
]

urlpatterns += staticfiles_urlpatterns() 