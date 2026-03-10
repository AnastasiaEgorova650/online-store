from django.contrib.auth.models import User

for user in User.objects.filter(username__startswith="buyer"):
    user.set_password("123456")
    user.save()
