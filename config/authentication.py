from rest_framework.authentication import BaseAuthentication

# 일단 BaseAuthentication를 상속받은 클래스의 authenticate 함수를 통해 user를 리턴하기만 하면 인증이 완료 된다.
class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, request):
        
        return None