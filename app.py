from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__, static_folder='.')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'projects.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Project Model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    organization = db.Column(db.String(200))
    company_name = db.Column(db.String(200))  # Added company name
    sector = db.Column(db.String(100))
    technology_stack = db.Column(db.String(500))
    technology_type = db.Column(db.String(100))  # e.g., Web, Mobile, AI/ML, IoT
    status = db.Column(db.String(50))
    size = db.Column(db.String(50))  # e.g., Small, Medium, Large, Enterprise
    start_date = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    suburb = db.Column(db.String(100))  # Added for more specific location
    state = db.Column(db.String(50))    # Added for state information
    contact_email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'organization': self.organization,
            'company_name': self.company_name,
            'sector': self.sector,
            'technology_stack': self.technology_stack,
            'technology_type': self.technology_type,
            'status': self.status,
            'size': self.size,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'location': self.location,
            'suburb': self.suburb,
            'state': self.state,
            'contact_email': self.contact_email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Create database tables
with app.app_context():
    db.create_all()

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Search endpoint
@app.route('/api/projects/search', methods=['GET'])
def search_projects():
    query = request.args.get('q', '')
    sector = request.args.get('sector', '')
    status = request.args.get('status', '')
    location = request.args.get('location', '')
    tech_type = request.args.get('tech_type', '')
    size = request.args.get('size', '')
    company = request.args.get('company', '')
    
    projects_query = Project.query
    
    if query:
        projects_query = projects_query.filter(
            db.or_(
                Project.name.ilike(f'%{query}%'),
                Project.description.ilike(f'%{query}%'),
                Project.technology_stack.ilike(f'%{query}%'),
                Project.company_name.ilike(f'%{query}%'),
                Project.suburb.ilike(f'%{query}%'),
                Project.state.ilike(f'%{query}%')
            )
        )
    
    if sector:
        projects_query = projects_query.filter(Project.sector == sector)
    
    if status:
        projects_query = projects_query.filter(Project.status == status)
        
    if location:
        projects_query = projects_query.filter(
            db.or_(
                Project.location.ilike(f'%{location}%'),
                Project.suburb.ilike(f'%{location}%'),
                Project.state.ilike(f'%{location}%')
            )
        )
        
    if tech_type:
        projects_query = projects_query.filter(Project.technology_type == tech_type)
        
    if size:
        projects_query = projects_query.filter(Project.size == size)

    if company:
        projects_query = projects_query.filter(Project.company_name.ilike(f'%{company}%'))
    
    projects = projects_query.all()
    return jsonify([project.to_dict() for project in projects])

# Add project endpoint
@app.route('/api/projects', methods=['POST'])
def add_project():
    data = request.json
    
    try:
        project = Project(
            name=data['name'],
            description=data.get('description'),
            organization=data.get('organization'),
            company_name=data.get('company_name'),
            sector=data.get('sector'),
            technology_stack=data.get('technology_stack'),
            technology_type=data.get('technology_type'),
            status=data.get('status'),
            size=data.get('size'),
            start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
            location=data.get('location'),
            suburb=data.get('suburb'),
            state=data.get('state'),
            contact_email=data.get('contact_email')
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify(project.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Get all projects endpoint
@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])

if __name__ == '__main__':
    app.run(debug=True, port=3000)
