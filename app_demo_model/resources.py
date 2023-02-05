from import_export import resources
from .models import AppliedScience, HealthScience, PureScience

class AppliedSciResource(resources.ModelResource):
    class Meta:
        model = AppliedScience
        

class HealthSciResource(resources.ModelResource):
    class Meta:
        model = HealthScience
        
        
class PureSciResource(resources.ModelResource):
    class Meta:
        model = PureScience
        