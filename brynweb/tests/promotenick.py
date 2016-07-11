from django.contrib.auth.models import User

u = User.objects.get(email='n.j.loman@bham.ac.uk')
u.is_superuser = True
u.is_staff = True
u.save()
