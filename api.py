from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'API on'

@app.route('/users')
def users():
    try:
        data = pd.read_json('players_data.json', encoding='utf-8')
        users_info = []

        for player_id, player_info in data.items():
            name_user = player_info['player_name']
            total_speedpoints = player_info['total_speedpoints']
            total_laps = sum(len(race['laps']) for race in player_info['races'])
            users_info.append({
                'name_user': name_user,
                'speedpoints': total_speedpoints,
                'total_laps': total_laps
            })

        return jsonify(users_info)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/top_users')
def top_users():
    try:
        data = pd.read_json('players_data.json', encoding='utf-8')
        
        users_info = []
        for player_id, player_info in data.items():
            users_info.append({
                'name_user': player_info['player_name'],
                'speedpoints': player_info['total_speedpoints']
            })
        top_users = sorted(users_info, key=lambda x: x['speedpoints'], reverse=True)[:3]

        return jsonify(top_users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/all_users_top')
def all_users_top():
    try:
        data = pd.read_json('players_data.json', encoding='utf-8')

        users_info = []
        for player_id, player_info in data.items():
            users_info.append({
                'name_user': player_info['player_name'],
                'speedpoints': player_info['total_speedpoints']
            })

        sorted_users = sorted(users_info, key=lambda x: x['speedpoints'], reverse=True)

        return jsonify(sorted_users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/all_users_bottom')
def all_users_bottom():
    try:
        data = pd.read_json('players_data.json', encoding='utf-8')

        users_info = []
        for player_id, player_info in data.items():
            users_info.append({
                'name_user': player_info['player_name'],
                'speedpoints': player_info['total_speedpoints']
            })

        bottom_users = sorted(users_info, key=lambda x: x['speedpoints'])

        return jsonify(bottom_users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.run(host='0.0.0.0')