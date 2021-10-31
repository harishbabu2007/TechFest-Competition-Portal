from django.shortcuts import render, redirect
from .models import Event, ProblemsSolved, Problems
import os
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from importlib.machinery import SourceFileLoader
from rest_framework.response import Response
from pathlib import Path

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


@login_required
@api_view(["POST", "GET"])
def evaluate_problem(request):
  try:
    print(request.data.get("key"))
  except:
    return Response({"request": "failed"})

  if request.method == "POST" and request.data.get("key") == "TechFestOC":
    problem = Problems.objects.filter(id=request.data.get("id"))

    if len(problem) == 0:
      return Response({"request": "failed"})

    problem = problem[0]

    code = request.data.get("code")

    this_file_path = Path(__file__).resolve().parent
    data_path = f"problem_files\\{problem.name}\\{request.user.username}__attempt__.py"
    path_write_user = os.path.join(this_file_path, data_path)

    line_write = code.split("\n")

    for i in range(len(line_write)):
      line_write[i] += "\n"
    
    user_file = open(path_write_user, 'w')
    user_file.writelines(line_write)
    user_file.close()

    try:
      username = f"{request.user.username}__attempt__"
      file_check_user = SourceFileLoader(username, path_write_user).load_module()

      evaluator_path = f"problem_files/{problem.mainFile}"
      evaluator_path = os.path.join(this_file_path, evaluator_path)
      evaluator_name = problem.mainFile.name.replace(".py", "").replace(problem.name + "/", "")
      evaluator = SourceFileLoader(evaluator_name, evaluator_path).load_module()

      type_msg, eval_message = evaluator.executeProg(file_check_user)

      if type_msg == False:
        return Response({
          "request": "error",
          "msg": eval_message,
        })
              
    except Exception as e:
      return Response({
          "request": "error",
          "msg": str(e),
        })

    return Response({"request": "passed"})

  return Response({"request": "failed"})