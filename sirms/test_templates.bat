@echo off
echo Running Template Tests...
pytest tests/test_templates.py -v --tb=short
pause
