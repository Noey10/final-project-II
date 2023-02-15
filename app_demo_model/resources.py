from import_export import resources
from .models import *

#อันเก่าไม่ใช้แล้ว
class AppliedSciResource(resources.ModelResource):
    class Meta:
        model = AppliedScience
        
class HealthSciResource(resources.ModelResource):
    class Meta:
        model = HealthScience
          
class PureSciResource(resources.ModelResource):
    class Meta:
        model = PureScience

#อันใหม่
class DssiResource(resources.ModelResource):
    class Meta:
        model = DSSI
        
class IctResource(resources.ModelResource):
    class Meta:
        model = ICT
        
class BioResource(resources.ModelResource):
    class Meta:
        model = BIO
        
class ChemiResource(resources.ModelResource):
    class Meta:
        model = CHEMI