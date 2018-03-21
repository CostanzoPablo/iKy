# -*- encoding: utf-8 -*-
from flask import Blueprint, current_app, request, jsonify
from factories._celery import create_celery
home = Blueprint('home_views', __name__)


################################################
# Testing
################################################
@home.route("/testing", methods=["POST"])
def r_testing():
    result = request.get_json()
    print "JSON : ", result
    print "Form : ", request.form
    print "Testing : ", request.form.get('testing')
    print "Username : ", request.form.get('username')
    return repr(result)


################################################
# State
################################################
@home.route("/state/<task_id>/<task_app>")
def r_state(task_id, task_app):
    celery = create_celery(current_app)
    res = celery.AsyncResult(task_id).state
    return jsonify(state=res, task_id=task_id, task_app=task_app)


################################################
# Result 
################################################
@home.route("/result/<task_id>")
def r_result(task_id):
    celery = create_celery(current_app)
    res = celery.AsyncResult(task_id).get()
    return jsonify(result=res)


################################################
# Github 
################################################
@home.route("/github", methods=["POST"])
def r_github():
    celery = create_celery(current_app)
    username = request.form.get('username')
    print "Github - Detected Username : ", username
    res = celery.send_task('modules.github.github_tasks.t_github', args=(username, )) 
    print "Task : ", res.task_id
    return jsonify(module="github", task=res.task_id, param=username)


################################################
# Keybase
################################################
@home.route("/keybase", methods=["POST"])
def r_keybase(username=None):
    celery = create_celery(current_app)
    username = request.form.get('username')
    print "Keybase - Detected Username : ", username
    res = celery.send_task('modules.keybase.keybase_tasks.t_keybase', args=(username, )) 
    print "Task : ", res.task_id
    return jsonify(module="keybase", task=res.task_id, param=username)


################################################
# Gitlab
################################################
@home.route("/gitlab", methods=["POST"])
def r_gitlab(username=None):
    celery = create_celery(current_app)
    username = request.form.get("username")
    print "Gitlab - Detected Username : ", username
    res = celery.send_task('modules.gitlab.gitlab_tasks.t_gitlab', args=(username, )) 
    print "Task : ", res.task_id
    return jsonify(module="gitlab", task=res.task_id, param=username)


################################################
# Usersearch 
################################################
@home.route("/usersearch", methods=["POST"])
def r_usersearch(username=None):
    celery = create_celery(current_app)
    username = request.form.get("username")
    print "Usersearch - Detected Username : ", username
    res = celery.send_task('modules.usersearch.usersearch_tasks.t_usersearch', args=(username, )) 
    print "Task : ", res.task_id
    return jsonify(module="usersearch", task=res.task_id, param=username)
