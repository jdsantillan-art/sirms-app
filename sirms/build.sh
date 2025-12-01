#!/usr/bin/env bash
# exit on error
set -o errexit

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🎨 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️  Running migrations..."
python manage.py migrate

echo "📊 Loading initial data..."
# Load data quickly, skip if already exists
python setup_render_data.py 2>&1 | head -n 50 || echo "⚠️  Data loading skipped or had issues"

echo "✅ Build completed successfully!"
