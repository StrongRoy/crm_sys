from django.db import models


# Create your models here.


class UserInfo(models.Model):
    """
    管理员
    """
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class StudentGroup(models.Model):
    """
    班级
    """
    title = models.CharField('班级名称', max_length=64)
    count = models.IntegerField('班级人数')

    def __str__(self):
        return self.title


class Student(models.Model):
    """
    学生
    """
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    group = models.ForeignKey(to=StudentGroup, verbose_name='学生班级')


class Questionnaire(models.Model):
    caption = models.CharField('问卷名称', max_length=64)
    user = models.ForeignKey(to=UserInfo, verbose_name='创建问卷的用户')
    group = models.ForeignKey(to=StudentGroup, verbose_name='学生班级')


class Question(models.Model):
    title = models.CharField('题目', max_length=64)
    q_type = models.IntegerField('类型', choices=((1, '单选'), (2, '建议'), (3, '打分(1~10分)'),))
    questionnaire = models.ForeignKey(to=Questionnaire, verbose_name='问卷')


class RadioQuestion(models.Model):
    content = models.CharField('内容', max_length=64)
    score = models.IntegerField('分值')
    question = models.ForeignKey(to=Question, verbose_name='问题')


class Answer(models.Model):
    """
    回答
    """
    student = models.ForeignKey(to=Student)
    question = models.ForeignKey(to=Question)

    score = models.IntegerField(null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)
    option = models.ForeignKey(to=RadioQuestion, null=True, blank=True)


class Room(models.Model):
    name = models.CharField('会议室名', max_length=32, )
    address = models.CharField('会议室地址', max_length=64)

    def __str__(self):
        return self.name

class Space(models.Model):
    content = models.CharField(max_length=32,verbose_name='时间段')
    def __str__(self):
        return self.content
class MeetingRoom(models.Model):
    date = models.DateTimeField('预定日期')
    user = models.ForeignKey(to=UserInfo, verbose_name='用户')
    room = models.ManyToManyField(to=Room, verbose_name='会议室')
    space = models.ManyToManyField(to=Space,verbose_name='时间段')
    def __str__(self):
        return self.user.name

