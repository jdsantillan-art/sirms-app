#!/usr/bin/env bash
# exit on error
set -o errexit

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🎨 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️  Running migrations..."
python manage.py migrate

echo "📊 Loading initial data and violations..."
python setup_render_data.py || echo "⚠️  Data loading had issues, continuing..."

echo "✅ Build completed successfully!"
