from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder='static')

# Sample data
PROJECTS = [
    {
        'id': 1,
        'name': 'City Traffic Management System',
        'description': 'AI-powered traffic management system for smart cities',
        'location': 'Sydney CBD',
        'technology': 'Python, TensorFlow, IoT',
        'sector': 'Transportation'
    },
    {
        'id': 2,
        'name': 'Healthcare Data Platform',
        'description': 'Centralized healthcare data management system',
        'location': 'Melbourne',
        'technology': 'Java, Spring Boot, PostgreSQL',
        'sector': 'Healthcare'
    },
    {
        'id': 3,
        'name': 'Smart Energy Grid',
        'description': 'Renewable energy management platform',
        'location': 'Brisbane',
        'technology': 'Python, AWS, IoT',
        'sector': 'Energy'
    }
]

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/projects')
def get_projects():
    sector = request.args.get('sector')
    technology = request.args.get('technology')
    location = request.args.get('location')
    subscription = request.headers.get('X-Subscription-Type', 'free')
    
    filtered_projects = PROJECTS
    
    if sector:
        filtered_projects = [p for p in filtered_projects if sector.lower() in p['sector'].lower()]
    if technology:
        filtered_projects = [p for p in filtered_projects if technology.lower() in p['technology'].lower()]
    if location:
        filtered_projects = [p for p in filtered_projects if location.lower() in p['location'].lower()]
    
    response = []
    for project in filtered_projects:
        if subscription == 'premium':
            response.append(project)
        else:
            response.append({
                'id': project['id'],
                'name': project['name'],
                'location': project['location'],
                'sector': project['sector']
            })
    
    return jsonify(response)

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
