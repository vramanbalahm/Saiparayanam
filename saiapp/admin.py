from django.contrib import admin
from .models import *

#
# class FilterTeacheradmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         # For Django < 1.6, override queryset instead of get_queryset
#         qs = super(FilterTeacheradmin, self).get_queryset(request)
#         return qs.filter(TeacherEmail=request.user)
#
# class FilterParayanGroupadmin(FilterTeacheradmin):
#     def get_queryset(self, request):
#         # For Django < 1.6, override queryset instead of get_queryset
#         qs = super(FilterParayanGroupadmin, self).get_queryset(request)
#         return qs.filter(GrpTeacher=FilterTeacheradmin)


class Teacheradmin(admin.ModelAdmin):
    list_display = ['TeacherID', 'TeacherName', 'TeacherLocation','TeacherStatus']
    list_filter = ["TeacherLocation",'TeacherStatus']
    search_fields = ['TeacherID']



class ParayanGroupadmin(admin.ModelAdmin):
    list_filter = ["GrpTeacher"]
    list_display = ['GrpID', 'GrpName', 'GrpTeacher']


#
# class Filterdevoteeadmin(FilterParayanGroupadmin):
#     def get_queryset(self, request):
#         # For Django < 1.6, override queryset instead of get_queryset
#         qs = super(Filterdevoteeadmin, self).get_queryset(request)
#         return qs.filter(GrpID_id=FilterParayanGroupadmin)

    #
    # def queryset(self, request):
    #     qs = super(devoteeadmin, self).queryset(request)
    #     #qs = admin.ModelAdmin.queryset(self, request)
    #     if request.user.is_superuser:
    #         return qs
    #     else:
    #         return qs.filter('GrpID.GrpTeacher' = request.user)


class devoteeadmin(admin.ModelAdmin):

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(devoteeadmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields['GrpID'].queryset = ParayanGroup.objects.filter(GrpTeacher=(Teacher.objects.filter(TeacherEmail=request.user)))
    #     return form

    list_filter = ['GrpID','House']
    list_display = ['RollNumber','DevName','House','GrpID']





class Locationadmin(admin.ModelAdmin):
    ordering = ['locname']



# Register your models here.
admin.site.register(Teacher,Teacheradmin)
admin.site.register(ParayanGroup,ParayanGroupadmin)
admin.site.register(devotee,devoteeadmin)
admin.site.register(Location,Locationadmin)
