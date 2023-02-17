from import_export import resources
from .models import *

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