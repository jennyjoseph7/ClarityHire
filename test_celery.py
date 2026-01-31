import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.celery_app import celery_app

print("Testing Celery connection...")
print("Broker URL:", celery_app.conf.broker_url[:30] + "...")

try:
    inspect = celery_app.control.inspect()
    active = inspect.active()
    
    if active:
        print("WORKERS FOUND:", list(active.keys()))
    else:
        print("NO WORKERS - Celery worker is NOT running or NOT connected to Redis")
        
    registered = inspect.registered()
    if registered:
        print("REGISTERED TASKS:")
        for worker, tasks in registered.items():
            print(f"  {worker}:")
            for t in tasks:
                print(f"    - {t}")
    else:
        print("NO REGISTERED TASKS")
        
except Exception as e:
    print(f"ERROR: {e}")
    print("Celery cannot connect to broker (Redis)")
