from django.conf.urls import url
from .views import index, rules, problems, solve_event_problem, evaluate_problem, leaderboard, leaderboardStanding
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
  path("", index, name="interface-index"),
  path("events/rules/<int:id>", rules, name="interface-rules"),
  path("events/problems/<int:id>", problems, name="interface-problems"),
  path("events/<int:event_id>/problem/<int:problem_id>", solve_event_problem, name="interface-solve"),
  path("interface/requests/evaluate", evaluate_problem, name="interface-rest-request"),
  path("leaderboard/", leaderboard, name="interface-leaderboard"),
  path("leaderboard/event/<int:id>", leaderboardStanding, name="interface-standing"),
]

urlpatterns += staticfiles_urlpatterns() 