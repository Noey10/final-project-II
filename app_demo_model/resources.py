from import_export import resources
from .models import *

class DataResource(resources.ModelResource):
    class Meta:
        model = TrainingData
        