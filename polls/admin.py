from django.contrib import admin
from .models import Room,MeetingRoom,UserInfo,Space,StudentGroup
# Register your models here.


admin.site.register(UserInfo)
admin.site.register(Room)
admin.site.register(Space)
admin.site.register(MeetingRoom)
admin.site.register(StudentGroup)

