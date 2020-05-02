from flask import *
from markupsafe import escape
import os
import requests
import random

app = Flask(__name__)

players={}
dead={}
game_started = False

@app.route('/palermo')
def index():
    return render_template('palermo.html')

@app.route('/palermo/state',methods=['POST'])
def state():
    global game_started,players,dead
    role=""
    print(request.json)
    username = request.json
    if username not in players and not game_started:
        players[username]=""
        print("Player {} joined".format(username))
    if game_started and username in players:
        role = players[username]
    print(game_started,username,players)
    state = {"role":role,"players":list(players.keys()),"dead":dead}
    return jsonify(state)

@app.route('/palermo/admin')
def admin():
    return render_template('palermo_admin.html')

@app.route('/palermo/admin/kill_hide/<username>',methods=['POST'])
def kill_hide(username):
    global dead
    dead[username]="HIDDEN"
    print("kill_show: {} - HIDDEN".format(username))
    return ""


@app.route('/palermo/admin/kill_show/<username>',methods=['POST'])
def kill_show(username):
    global dead
    dead[username]=players[username]
    print("kill_show: {} - {}".format(username,players[username]))
    return ""


@app.route('/palermo/admin/start',methods=['POST'])
def start():
    global game_started,players
    if game_started:
        return ""
    roles_list = request.json
    print("Starting")
    if len(roles_list)==len(players):
        for player in players:
            role_id = random.randint(0,len(roles_list)-1)
            players[player]=roles_list[role_id]
            roles_list.pop(role_id)
        game_started = True
        print("Game started - {}".format(game_started))
        print(players)
    else:
        print("Roles are not equal to the number of players")
        print(players)
        print(roles_list)
    return ""


@app.route('/palermo/admin/reset',methods=['POST'])
def reset():
    global game_started,players,dead
    players={}
    dead={}
    game_started = False
    print("Game was reset")
    return ""

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)