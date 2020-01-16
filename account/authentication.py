from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None, password=None):  # 注意这里的username带来的参数不是user的username，而是email，
        # 也可携带其他参数。但是username和password这个参数名称不能变，是为了确保当前后端与验证框架视图直接协同工作。
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):  # check_password()内置的密码验证方法，因为密码已经通过set_password()方法加密
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
