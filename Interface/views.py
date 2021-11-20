from django.shortcuts import render, redirect
from .models import Event, ProblemsSolved, Problems, Leaderboard
import os
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from importlib.machinery import SourceFileLoader
from rest_framework.response import Response
from pathlib import Path
import time


# Create your views here.
def index(request):
  events_t = Event.objects.all()

  events = []

  for i in range(len(events_t)):
    events.append(events_t[i])

  for i in range(len(events)):
    if not events[i].can_participate() and events[i].get_time_diff() > 0:
      del events[i]

  params = {
    'title' : "Technex Dps",
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

  print(problems_show, problems_event)

  if len(problems_show) != len(problems_event):
    for prob in problems_event:
      data = ProblemsSolved(problem=prob, user=request.user, solved=False,)
      data.save()

    problems_show = request.user.solved_user.all()

  playerBoard = Leaderboard.objects.filter(user=request.user)
  if len(playerBoard) == 0:
    data = Leaderboard(
      event = event[0],
      user = request.user,
      problems_solved = 0,
      seconds_taken = 0,
    )
    data.save()

  params = {
    "problems" : problems_show,
    'event' : event[0],
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

  solved = request.user.solved_user.filter(problem__pk=event_problem.id)
  solved = solved[0]

  if solved.solved == True :
    return redirect("interface-index")

  absPath = os.path.abspath(f"Interface/problem_files/{event_problem.userFile}")
  userFile = open(absPath, 'r')

  params = { 
    'problem': event_problem,
    'event_id': event_check[0].id,
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

    if problem.event.can_participate() == False:
      return Response({
        "request": "error",
        "msg": 
        """
        TIMES UP!!!
        time is up you can't submit the problems anymore
        """
      })

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
      user_file_name = f"{request.user.username}__attempt__"
      file_check_user = SourceFileLoader(user_file_name, path_write_user).load_module()

      evaluator_path = f"problem_files/{problem.mainFile}"
      evaluator_path = os.path.join(this_file_path, evaluator_path)
      evaluator_name = problem.mainFile.name.replace(".py", "").replace(problem.name + "/", "")
      evaluator = SourceFileLoader(evaluator_name, evaluator_path).load_module()

      out_file_name = request.user.username + "__out__"
      type_msg, eval_message = evaluator.executeProg(file_check_user, out_file_name)

      answers_file_name =  problem.expected_output.name
      answers_file_path = f"problem_files/{answers_file_name}"
      answers_file_path = os.path.join(this_file_path, answers_file_path)
      answers_file = open(answers_file_path, "r")

      out_file_name = f"problem_files/{problem.name}/{out_file_name}.txt"
      out_file_path = os.path.join(this_file_path, out_file_name)
      user_out_file = open(out_file_path, "r")

      user_answer = user_out_file.readlines()
      answer = answers_file.readlines()

      if user_answer != answer:
        return Response({
          "request" : "Wrong",
          "msg":
          """
          Testcases failed.
          Your code couldn't generate the desired outputs.
          Refer the problem again and try writing the code again.
          """
        })

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

    solved = request.user.solved_user.filter(problem__pk=problem.id)
    solved = solved[0]
    solved.solved = True
    solved.save()

    playerBoard = Leaderboard.objects.filter(user=request.user)
    playerBoard = playerBoard[0]
    playerBoard.problems_solved += 1
    playerBoard.seconds_taken += float(request.data.get("timeTaken"))
    playerBoard.save()

    return Response({
      "request": "passed",
      "msg" : 
      """
      Success
      You have solved this problem.
      You can move to the next problem.
      """
    })

  return Response({"request": "failed", "msg" : "server error"})


def leaderboard(request):
  events = Event.objects.all()

  params = {
    "events" : events,
  }

  return render(request, "Interface/leaderboard.html", params)


def leaderboardStanding(request, id):
  def sortStandings(objectDB):
    if objectDB.seconds_taken == 0:
      return objectDB.problems_solved / 1

    return objectDB.problems_solved / objectDB.seconds_taken

  standings = Leaderboard.objects.filter(event__id=id)
  event = Event.objects.filter(id=id)

  standings = list(standings)
  standings.sort(key=sortStandings, reverse=True)

  if len(event) == 0:
    return redirect("interface-leaderboard") 
  
  event = event[0]

  params = {
    "standings" : standings,
    "event" : event
  }

  return render(request, "Interface/standing.html", params)