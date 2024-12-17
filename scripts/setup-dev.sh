#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo "Installing development dependencies..."
pip install pytest pytest-cov black flake8 watchdog

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOL
FLASK_APP=api/app.py
FLASK_ENV=development
MONGODB_URI=mongodb://localhost:27017/it_tech_radar
SECRET_KEY=dev_secret_key
DEBUG=True
EOL
fi

# Check if MongoDB is running
echo "Checking MongoDB status..."
if ! pgrep -x "mongod" > /dev/null; then
    echo "MongoDB is not running. Please start MongoDB first."
    echo "You can start it with: brew services start mongodb-community"
    exit 1
fi

echo "Development environment setup complete!"
echo "To start the development server:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run: flask run"
