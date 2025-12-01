#!/usr/bin/env python3
"""Force deployment to Render"""
import subprocess
import sys

def run_command(cmd):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='.')
        print(f"Command: {cmd}")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    print("=" * 60)
    print("FORCING RENDER DEPLOYMENT")
    print("=" * 60)
    
    # Check current status
    print("\n1. Checking git status...")
    run_command("git status --short")
    
    # Add all changes
    print("\n2. Adding all changes...")
    run_command("git add .")
    
    # Create empty commit to trigger deployment
    print("\n3. Creating deployment commit...")
    if run_command('git commit --allow-empty -m "Force Render deployment - Dec 2, 2025"'):
        print("✅ Commit created successfully")
    else:
        print("⚠️ Commit may already exist or no changes")
    
    # Push to origin
    print("\n4. Pushing to GitHub...")
    if run_command("git push origin main"):
        print("✅ Successfully pushed to GitHub!")
        print("\n" + "=" * 60)
        print("DEPLOYMENT TRIGGERED!")
        print("=" * 60)
        print("\n📦 Render will now automatically deploy your changes")
        print("⏱️  Expected time: 8-12 minutes")
        print("🌐 URL: https://sirmsportal.onrender.com")
        print("\n✅ Check Render dashboard for build progress")
    else:
        print("❌ Failed to push to GitHub")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
