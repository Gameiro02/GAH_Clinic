import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

SECRET_KEY = settings.SECRET_KEY

User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        
        if not header or not header.startswith('Bearer '):
            return None
        
        token = header.split(' ')[1]
        
        try:
            user_id = decode_token(token)
            user = User.objects.get(pk=user_id)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user')
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

