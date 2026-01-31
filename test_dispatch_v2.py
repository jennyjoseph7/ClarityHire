"""
Better test to see what's happening with task dispatch
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("1. Importing celery_app...")
from app.core.celery_app import celery_app
print(f"   Broker: {celery_app.conf.broker_url[:40]}...")

print("\n2. Importing parse_resume_task...")
from app.worker import parse_resume_task
print(f"   Task name: {parse_resume_task.name}")
print(f"   Task registered: {parse_resume_task.name in celery_app.tasks}")

print("\n3. Attempting to dispatch task...")
try:
    result = parse_resume_task.delay("test-resume-id", "/fake/path.pdf")
    print(f"   SUCCESS! Task ID: {result.id}")
    print(f"   \nCheck your Celery worker terminal for task execution!")
except Exception as e:
    print(f"   FAILED: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
