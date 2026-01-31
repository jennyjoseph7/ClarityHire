"""
Quick test to check if we can create and dispatch a Celery task manually
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.worker import parse_resume_task
import asyncio

print("Testing Celery task dispatch...")

# Try to dispatch a dummy task
try:
    result = parse_resume_task.delay("test-id", "test-path.pdf")
    print(f"✓ Task dispatched successfully!")
    print(f"  Task ID: {result.id}")
    print(f"  Task status: {result.status}")
    print("\nNow check your Celery worker terminal - you should see an error about the test file not existing, but that's OK!")
    print("The important thing is that the task was RECEIVED by the worker.")
except Exception as e:
    print(f"✗ Failed to dispatch task: {e}")
    print("\nThis means Celery cannot communicate with Redis properly.")
