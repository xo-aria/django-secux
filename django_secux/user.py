from .models import UserSession
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def create_session(user, session_key, ip=None, user_agent=None):
    return UserSession.objects.create(
        user=user,
        session_key=session_key,
        ip_address=ip,
        user_agent=user_agent
    )

def check_user_session(user, session_key):
    try:
        UserSession.objects.get(user=user, session_key=session_key)
        return True
    except ObjectDoesNotExist:
        return False

def get_user_sessions(user):
    return UserSession.objects.filter(user=user)

def get_all_sessions():
    return UserSession.objects.all()

def terminate_session(user, session_key):
    deleted = UserSession.objects.filter(user=user, session_key=session_key).delete()
    Session.objects.filter(session_key=session_key).delete()
    return deleted

def is_session_active(session_key):
    return Session.objects.filter(session_key=session_key, expire_date__gt=timezone.now()).exists()
