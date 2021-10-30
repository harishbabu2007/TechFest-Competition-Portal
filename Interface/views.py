from django.shortcuts import render, redirect
from .models import Event, ProblemsSolved, Problems
import os
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
  events_t = Event.objects.all()

  events = []

  for i in range(len(events_t)):
    events.append(events_t[i])


  for i in range(len(events)):
    print(events[i].get_time_diff())
    if not events[i].can_participate() and events[i].get_time_diff() > 0:
      del events[i]
         

  params = {
    'title' : "TechFest Dps",
    'events' : events,
  }

  return render(request, "Interface\index.html", params)

@login_required
def rules(request, id):
  event = Event.objects.filter(id=id)

  if len(event) == 0:
    return redirect("interface-index")

  if event[0].can_participate() == False:
    return redirect("interface-index")

  params = {
    "id" : id,
    "name" : event[0].name,
  }

  return render(request, "Interface/rules.html", params)

@login_required
def problems(request, id):
  event = Event.objects.filter(id=id)

  if len(event) == 0:
    return redirect("interface-index")

  if event[0].can_participate() == False:
    return redirect("interface-index")

  problems_show = request.user.solved_user.all()

  problems_event = event[0].prob_event.all()

  if len(problems_show) != len(problems_event):
    for prob in problems_event:
      data = ProblemsSolved(problem=prob, user=request.user, solved=False,)
      data.save()

    problems_show = request.user.solved_user.all()

  params = {
    "problems" : problems_show
  }

  return render(request, "Interface/problems.html", params)


@login_required 
def solve_event_problem(request, event_id, problem_id):
  event_check = Event.objects.filter(id=event_id)

  if len(event_check) == 0:
    return redirect("interface-index")

  if event_check[0].can_participate() == False:
    return redirect("interface-index")

  event_problem = event_check[0].prob_event.filter(id=problem_id)

  if len(event_problem) == 0:
    return redirect("interface-index")

  event_problem = event_problem[0]

  absPath = os.path.abspath(f"Interface/problem_files/{event_problem.userFile}")
  userFile = open(absPath, 'r')

  params = { 
    'problem': event_problem,
    'userFile': userFile.read()
  }
  
  return  render(request, "Interface/solve.html", params)