from django.contrib import admin
from .models import Register_User,Auto_generate,OTP
from django.contrib.auth.models import Group,User
from django.contrib.auth.admin import GroupAdmin
# Register your models here.
admin.site.register(Register_User)
admin.site.register(Auto_generate)
admin.site.register(OTP)

# Create or get groups
admin.site.unregister(Group)
## Doctor Group
class Doctor_Group(GroupAdmin):
    list_display = ('name','number_of_users')
    search_fields = ('name',)
    list_filter = ('name',)

    def number_of_users(self,obj):
        return obj.user_set.count()
    number_of_users.short_description = 'Number of Users'
admin.site.register(Group , Doctor_Group)
Doctor_group, created = Group.objects.get_or_create(name='Doctor') ## create Doctors group
doctor_users = Register_User.objects.filter(user_type='4') # Filter users by user_type = 'doctor'
doctor_user_list = doctor_users.values_list('user_id', flat=True) 
for user in doctor_user_list:
    doctor = User.objects.get(id=user)
    if doctor.is_active == True:
        doctor.groups.add(Doctor_group)  # Add the user to the Doctor group
        doctor.save()

admin.site.unregister(Group)
## Staff Group
class Staff_Group(GroupAdmin):
    list_display = ('name','number_of_users')
    search_fields = ('name',)
    list_filter = ('name',)

    def number_of_users(self,obj):
        return obj.user_set.count()
    number_of_users.short_description = 'Number of Users'
admin.site.register(Group , Staff_Group)
Staff_group, created = Group.objects.get_or_create(name='Staff') ## Filter users by user_type = 'staff'
staff_users = Register_User.objects.filter(user_type='3') # Filter users by user_type = 'staff'
staff_user_list = staff_users.values_list('user_id', flat=True) 
for user in staff_user_list:
    staff = User.objects.get(id=user)
    if staff.is_active == True:
        staff.groups.add(Staff_group)  # Add the user to the Doctor group
        staff.save()

admin.site.unregister(Group)
# admin.site.unregister(Group)
class User_Approval_Request_Group(GroupAdmin):
    list_display = ('name','number_of_users')
    search_fields = ('name',)
    list_filter = ('name',)

    def number_of_users(self,obj):
        return obj.user_set.count()
    number_of_users.short_description = 'Number of Users'
admin.site.register(Group , User_Approval_Request_Group)
Approval_group, created = Group.objects.get_or_create(name='User Approval Request')
request_users = User.objects.filter(is_active=False)
for request_user in request_users:
    request_user.groups.add(Approval_group)
    request_user.save()


