from django.contrib import admin
from health.models import Register_User,Auto_generate,OTP
# Register your models here.
admin.site.register(Register_User)
admin.site.register(Auto_generate)
admin.site.register(OTP)