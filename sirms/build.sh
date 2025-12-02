#!/usr/bin/env bash
# exit on error
set -o errexit

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🎨 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️  Running migrations..."
python manage.py migrate

echo "📊 Loading initial data (if needed)..."
# Run data loading in background to avoid timeout
timeout 30 python setup_render_data.py 2>&1 | head -n 20 || echo "⚠️  Data loading skipped or timed out (this is OK if data exists)"

echo "👥 Creating staff accounts (Guidance, DO, ESP Teachers)..."
python manage.py create_staff_accounts || echo "⚠️  Staff accounts may already exist"

echo "✅ Build completed successfully!"
