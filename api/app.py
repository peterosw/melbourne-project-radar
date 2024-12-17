from flask import Flask, request, jsonify
from flask_cors import CORS
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime
import pymongo
from pymongo import MongoClient
import json

app = Flask(__name__)
CORS(app)

# MongoDB setup (we'll use a local MongoDB instance for now)
client = MongoClient('mongodb://localhost:27017/')
db = client['it_tech_radar']
projects_collection = db['projects']

class ProjectSchema(Schema):
    """Schema for validating project submissions"""
    projectName = fields.Str(required=True, validate=validate.Length(min=3, max=100))
    organization = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    description = fields.Str(required=True, validate=validate.Length(min=10, max=1000))
    sector = fields.Str(required=True, validate=validate.OneOf([
        'fintech', 'healthcare', 'retail', 'education', 
        'government', 'manufacturing', 'logistics', 'other'
    ]))
    projectStage = fields.Str(required=True, validate=validate.OneOf([
        'planning', 'inProgress', 'completed'
    ]))
    startDate = fields.Date(required=True)
    endDate = fields.Date(required=False, allow_none=True)
    technologies = fields.List(fields.Str(), required=True, validate=validate.Length(min=1))
    frameworks = fields.List(fields.Str(), required=False)
    city = fields.Str(required=True)
    suburb = fields.Str(required=False, allow_none=True)
    contactName = fields.Str(required=True)
    contactEmail = fields.Email(required=True)
    contactPhone = fields.Str(required=False, allow_none=True)

project_schema = ProjectSchema()

@app.route('/api/projects', methods=['POST'])
def submit_project():
    try:
        # Validate request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate against schema
        validated_data = project_schema.load(data)
        
        # Add metadata
        validated_data['createdAt'] = datetime.utcnow()
        validated_data['updatedAt'] = datetime.utcnow()
        
        # Insert into database
        result = projects_collection.insert_one(validated_data)
        
        return jsonify({
            'message': 'Project submitted successfully',
            'projectId': str(result.inserted_id)
        }), 201

    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'details': err.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

@app.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        # Get query parameters
        sector = request.args.get('sector')
        technology = request.args.get('technology')
        framework = request.args.get('framework')
        project_stage = request.args.get('projectStage')
        organization = request.args.get('organization')
        search = request.args.get('search')
        suburb = request.args.get('suburb')
        start_date_from = request.args.get('startDateFrom')
        start_date_to = request.args.get('startDateTo')
        sort_by = request.args.get('sortBy', 'createdAt')  # Default sort by creation date
        sort_order = request.args.get('sortOrder', 'desc')  # Default sort order
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        # Build query
        query = {}
        if sector:
            query['sector'] = sector
        if technology:
            query['technologies'] = {'$in': [technology]}
        if framework:
            query['frameworks'] = {'$in': [framework]}
        if project_stage:
            query['projectStage'] = project_stage
        if organization:
            query['organization'] = {'$regex': organization, '$options': 'i'}
        if suburb:
            query['suburb'] = {'$regex': suburb, '$options': 'i'}
        
        # Date range filter
        date_query = {}
        if start_date_from:
            date_query['$gte'] = start_date_from
        if start_date_to:
            date_query['$lte'] = start_date_to
        if date_query:
            query['startDate'] = date_query
        
        # Text search across multiple fields
        if search:
            query['$or'] = [
                {'projectName': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}},
                {'organization': {'$regex': search, '$options': 'i'}},
                {'technologies': {'$in': [search]}},
                {'frameworks': {'$in': [search]}}
            ]
        
        # Calculate skip value for pagination
        skip = (page - 1) * limit
        
        # Determine sort direction
        sort_direction = pymongo.DESCENDING if sort_order.lower() == 'desc' else pymongo.ASCENDING
        
        # Get total count for pagination
        total_count = projects_collection.count_documents(query)
        
        # Execute query with pagination and sorting
        projects = list(projects_collection.find(
            query,
            {'_id': False}
        ).sort(sort_by, sort_direction).skip(skip).limit(limit))
        
        # Get unique values for filters
        unique_sectors = projects_collection.distinct('sector')
        unique_technologies = projects_collection.distinct('technologies')
        unique_frameworks = projects_collection.distinct('frameworks')
        unique_stages = projects_collection.distinct('projectStage')
        unique_suburbs = projects_collection.distinct('suburb')
        
        return jsonify({
            'projects': projects,
            'pagination': {
                'currentPage': page,
                'totalPages': (total_count + limit - 1) // limit,
                'totalItems': total_count,
                'itemsPerPage': limit
            },
            'filters': {
                'sectors': unique_sectors,
                'technologies': unique_technologies,
                'frameworks': unique_frameworks,
                'stages': unique_stages,
                'suburbs': unique_suburbs
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    try:
        project = projects_collection.find_one({'_id': project_id})
        if not project:
            return jsonify({'error': 'Project not found'}), 404
            
        # Convert ObjectId to string for JSON serialization
        project['_id'] = str(project['_id'])
        return jsonify(project), 200

    except Exception as e:
        return jsonify({'error': 'Server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
