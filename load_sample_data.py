from app import app, db, Project
from datetime import datetime, timedelta

# Sample data
sample_projects = [
    {
        'name': 'Smart City IoT Network',
        'description': 'Implementing IoT sensors across Melbourne CBD for traffic and environmental monitoring',
        'organization': 'City of Melbourne',
        'company_name': 'Smart Melbourne Technologies Pty Ltd',
        'sector': 'Government',
        'technology_stack': 'IoT, Python, AWS, MongoDB',
        'technology_type': 'IoT',
        'status': 'In Progress',
        'size': 'Large',
        'start_date': datetime.now() - timedelta(days=90),
        'location': 'Melbourne CBD',
        'suburb': 'Melbourne',
        'state': 'Victoria',
        'contact_email': 'smartcity@melbourne.vic.gov.au'
    },
    {
        'name': 'Healthcare Data Platform',
        'description': 'Centralized healthcare data platform for Victorian hospitals',
        'organization': 'Department of Health',
        'company_name': 'HealthTech Solutions Australia',
        'sector': 'Healthcare',
        'technology_stack': 'Java, Spring Boot, PostgreSQL, Azure',
        'technology_type': 'Web',
        'status': 'Planning',
        'size': 'Enterprise',
        'start_date': datetime.now() + timedelta(days=30),
        'location': 'East Melbourne',
        'suburb': 'East Melbourne',
        'state': 'Victoria',
        'contact_email': 'health.it@vic.gov.au'
    },
    {
        'name': 'Digital Learning Platform',
        'description': 'Online learning platform for Victorian schools',
        'organization': 'Department of Education',
        'company_name': 'EduTech Innovations',
        'sector': 'Education',
        'technology_stack': 'React, Node.js, MongoDB, Google Cloud',
        'technology_type': 'Web',
        'status': 'Completed',
        'size': 'Large',
        'start_date': datetime.now() - timedelta(days=180),
        'location': 'Treasury Place',
        'suburb': 'East Melbourne',
        'state': 'Victoria',
        'contact_email': 'edu.support@vic.gov.au'
    },
    {
        'name': 'Public Transport App',
        'description': 'Real-time public transport tracking and journey planning app',
        'organization': 'Public Transport Victoria',
        'company_name': 'TransitTech Solutions',
        'sector': 'Government',
        'technology_stack': 'Flutter, Firebase, Google Maps API',
        'technology_type': 'Mobile',
        'status': 'In Progress',
        'size': 'Medium',
        'start_date': datetime.now() - timedelta(days=45),
        'location': 'Docklands',
        'suburb': 'Docklands',
        'state': 'Victoria',
        'contact_email': 'ptv.tech@vic.gov.au'
    },
    {
        'name': 'AI Medical Diagnosis Assistant',
        'description': 'AI-powered medical diagnosis support system for hospitals',
        'organization': 'Royal Melbourne Hospital',
        'company_name': 'MediAI Systems',
        'sector': 'Healthcare',
        'technology_stack': 'Python, TensorFlow, AWS, Docker',
        'technology_type': 'AI/ML',
        'status': 'Planning',
        'size': 'Medium',
        'start_date': datetime.now() + timedelta(days=15),
        'location': 'Parkville',
        'suburb': 'Parkville',
        'state': 'Victoria',
        'contact_email': 'ai.health@rmh.org.au'
    }
]

def load_sample_data():
    # Clear existing data
    Project.query.delete()
    
    # Add sample projects
    for project_data in sample_projects:
        project = Project(**project_data)
        db.session.add(project)
    
    # Commit changes
    db.session.commit()
    print("Sample data loaded successfully!")

if __name__ == '__main__':
    with app.app_context():
        load_sample_data()
