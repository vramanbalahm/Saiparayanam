from django.db import connections
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

class Weekchapters(models.Model):
    id = models.AutoField(primary_key=True)
    rollnumber = models.IntegerField()
    currentchapters = models.CharField(db_column='CurrentChapters', max_length=50)  # Field name made lowercase. 
    parayandate = models.DateField(db_column='Parayandate')  # Field name made lowercase.
    house = models.CharField(db_column='House', max_length=10)  # Field name made lowercase.
    genstatus = models.IntegerField(db_column='Genstatus')  # Field name made lowercase.
    gendate = models.DateTimeField(db_column='Gendate')  # Field name made lowercase.

    class Meta:
        db_table = 'weekchapters'




class Testchapters(models.Model):
    rollnumber = models.IntegerField()
    currentchapters = models.CharField(db_column='CurrentChapters', max_length=50)  # Field name made lowercase.
    parayandate = models.DateField(db_column='Parayandate')  # Field name made lowercase.
    house = models.CharField(db_column='House', max_length=10)  # Field name made lowercase.
    genstatus = models.IntegerField(db_column='Genstatus')  # Field name made lowercase.
    gendate = models.DateTimeField(db_column='Gendate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'testchapters'




class Location(models.Model):
    locname = models.CharField("Location Name",max_length=100,null=False)

    def __str__(self):
        return self.locname





class Teacher(models.Model):
    TeacherID = models.AutoField('ID',primary_key=True,auto_created=True,unique=True)
    TeacherName = models.CharField('Name',max_length=100,null=False)
    TeacherEmail = models.EmailField('E-Mail')
    TeacherPhone = models.IntegerField('Phone Number',serialize=False,null=False)
    # TeacherLocation = models.CharField('Location',max_length=100)
    TeacherLocation = models.ForeignKey(Location, on_delete=models.PROTECT, null=False, verbose_name='Location')
    StatusList = (('A','Active'),('I','Inactive'))
    TeacherStatus = models.CharField('Status',choices=StatusList,max_length=10,default='Active')


    def __str__(self):
        return (str(self.TeacherID) + ' - ' + self.TeacherName)





# on creating a teacher, create a user record with the email as the login name and password.
# signal (trigger) created for the same here.

@receiver(signals.post_save, sender=Teacher)
def create_teacher_user(sender,instance,**kwargs):

    # check if the teacher already exists as a user
    # user1 = User.objects.get_by_natural_key(instance.TeacherEmail)

    user1 = authenticate(username=instance.TeacherEmail, password=instance.TeacherEmail)

    if user1 is None:
        if instance.TeacherStatus == 'A':
            user1 = User.objects.create_user(username=instance.TeacherEmail, password = instance.TeacherEmail, email= instance.TeacherEmail,
                                         first_name = instance.TeacherName,is_superuser = False,is_staff = True,is_active = True)

            TeacherGroup = Group.objects.get(name='Teacher')
            TeacherGroup.user_set.add(user1)

    else:
        # check if the status of the teacher has been changed.
        # if the teacher has been made inactive, delete the corresponding user record only if there are no parayan groups belonging to the teacher. If not, dont allow the teacher to be made inactive
        # if the teacher has been made active from inactive, new user is created above.


        if instance.TeacherStatus == 'I':
            # dont allow a teacher to be made 'inactive' if the teacher belongs to any parayan group.

            if ((ParayanGroup.objects.filter(GrpTeacher = instance)).count()) == 0:
                user1 = User.objects.get_by_natural_key(instance.TeacherEmail)
                user1.delete()
            else:
                # raise ValidationError("Teacher has been assigned to 1 or more parayan groups. Teacher cannot be made inactive.")
                instance.TeacherStatus = 'A'
                instance.save()


@receiver(signals.post_delete, sender=Teacher)
def delete_teacher_user(sender,instance,**kwargs):
    # when a teacher is deleted, delete the corresponding user record as well.
    user1 = User.objects.get_by_natural_key(instance.TeacherEmail)
    user1.delete()




class ParayanGroup(models.Model):
    GrpID = models.CharField('ID',max_length=20,null=False)
    GrpName = models.CharField('Name',max_length=100,null=False)
    GrpTeacher = models.ForeignKey(Teacher,on_delete=models.PROTECT,null=False,limit_choices_to={'TeacherStatus':'A'})

    def __str__(self):
        return str(self.GrpID) + ' - ' + self.GrpName + ' - ' + self.GrpTeacher.TeacherName




class devotee(models.Model):
    # devID = models.IntegerField('ID',primary_key=True,null=False)
    GrpID = models.ForeignKey(ParayanGroup,verbose_name='Parayan Group',on_delete=models.PROTECT,null=False)
    DevName = models.CharField('Name',max_length=100,null=False)
    Devconname = models.CharField('Contact Name',max_length=100,null=False)
    RollNumber = models.IntegerField("Roll No.",null=False, validators=[MinValueValidator(1), MaxValueValidator(48)])
    #Location = models.CharField('Location',max_length=50,null=False)
    Location = models.ForeignKey(Location,on_delete=models.PROTECT,null=False)
    Language = models.CharField('Language',max_length=25,null=False)
    house_choices = (('Red','Red'),('Yellow','Yellow'),('Blue','Blue'),('Green','Green'))
    House = models.CharField('House',choices=house_choices,max_length=10,default='Red')
    # Status = models.SmallIntegerField(null=False)
    StatusList = (('A','Active'),('I','Inactive'))
    Status = models.CharField('Status',choices=StatusList,max_length=10,default='Active')

    phonenumber = models.IntegerField('Phone Number',serialize=False,null=False)
    email = models.EmailField('E-Mail')
    createddate = models.DateField('Created Date',auto_now=True)

    def __str__(self):
        return str(self.RollNumber) + ' - ' + self.DevName

    class Meta:
        db_table = 'devotee'
        unique_together = ['GrpID','RollNumber']






class Registrationdetails(models.Model):
    TeacherName = models.CharField('Name', max_length=100, null=False)
    TeacherEmail = models.EmailField('E-Mail', max_length=100, null=False)
    TeacherPhone = models.IntegerField('Phone Number', null=False)
    TeacherLocation = models.CharField('Location', max_length=100,null=False)
    GroupID = models.CharField('Parayan Group ID', max_length=50, null=False)
    GroupName = models.CharField('Parayan Group Name', max_length=100, null=False)





class volunteer(models.Model):
    volName = models.CharField('Name',max_length=100,null=False)
    # location = models.CharField('Location',max_length=50,null=False)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, null=False)
    language = models.CharField('Language',max_length=25,null=False)
    phonenumber = models.IntegerField('Phone Number',serialize=False,null=False)
    email = models.EmailField('E-Mail')
    createddate = models.DateField('Created Date',auto_now=True)

    def __str__(self):
        return str(self.volName) + ' - ' + self.location

    class Meta:
        db_table = 'volunteer'





