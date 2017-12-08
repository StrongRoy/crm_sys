from django.contrib import admin
from .models import Room,MeetingRoom,UserInfo,Space
# Register your models here.


admin.site.register(UserInfo)
admin.site.register(Room)
admin.site.register(Space)
admin.site.register(MeetingRoom)

