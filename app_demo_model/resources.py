from import_export import resources
from .models import Grades
 
class GradesResource(resources.ModelResource):
    class Meta:
        model = Grades