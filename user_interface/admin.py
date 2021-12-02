from django.contrib import admin
from .models import ( User,
                      InformationModel,
                      EducationModel,
                      MessageModel,
                      ProjectModel,
                      SkillsetModel,
                      ExperienceModel )

# Register your models here.

admin.site.register(User)
admin.site.register(InformationModel)
admin.site.register(EducationModel)
admin.site.register(MessageModel)
admin.site.register(ProjectModel)
admin.site.register(SkillsetModel)
admin.site.register(ExperienceModel)
