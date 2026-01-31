"""
Test if Celery can connect to Redis and if it's receiving tasks
"""
from app.core.celery_app import celery_app
from app.worker import parse_resume_task

print("=" * 60)
print("CELERY DIAGNOSTICS")
print("=" * 60)

# Check broker connection
try:
    inspect = celery_app.control.inspect()
    
    print("\n1. Checking active workers...")
    active = inspect.active()
    if active:
        print(f"✅ Active workers: {list(active.keys())}")
        for worker, tasks in active.items():
            print(f"   Worker: {worker}")
            print(f"   Active tasks: {len(tasks) if tasks else 0}")
            if tasks:
                for task in tasks:
                    print(f"     - {task.get('name')} (ID: {task.get('id')})")
    else:
        print("❌ No active workers found!")
    
    print("\n2. Checking registered tasks...")
    registered = inspect.registered()
    if registered:
        for worker, tasks in registered.items():
            print(f"✅ Worker {worker}:")
            for task in tasks:
                if 'parse_resume' in task:
                    print(f"   ✅ {task}")
    else:
        print("❌ No registered tasks found!")
    
    print("\n3. Checking stats...")
    stats = inspect.stats()
    if stats:
        for worker, stat in stats.items():
            print(f"✅ Worker: {worker}")
            print(f"   Broker: {stat.get('broker', {})}")
            print(f"   Pool: {stat.get('pool', {})}")
    else:
        print("❌ No stats available!")
        
except Exception as e:
    print(f"\n❌ CELERY CONNECTION ERROR: {e}")
    print("\nThis usually means:")
    print("  1. Redis is not running")
    print("  2. Celery worker is not running")
    print("  3. Redis connection string is incorrect")

print("\n" + "=" * 60)
