from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGeneretor(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        
        return ( 
            str(user.is_active) + str(user.pk) + str(timestamp)
        )
    