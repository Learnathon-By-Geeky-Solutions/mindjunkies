# yourapp/signals.py
from django.dispatch import Signal, receiver
from django.core.cache import cache

# Define the custom signal
course_updated = Signal()

@receiver(course_updated)
def clear_user_cache(sender, instance, user, **kwargs):
    cache_key = f"popular_courses"
    cache.delete(cache_key)
    print(f"Cache cleared for key: {cache_key}")

    cache_key = f"new_courses"
    cache.delete(cache_key)
    print(f"Cache cleared for key: {cache_key}")
