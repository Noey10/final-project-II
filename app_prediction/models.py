from django.db import models

# Create your models here.
class UserPredict(models.Model):
    CHOICES = [
        ('DSSI', 'วิทยาการคอมพิวเตอร์'),
        ('DSSI', 'วิทยาการข้อมูลและนวัตกรรมซอฟต์แวร์'),
        ('ICT', 'เทคโนโลยีสารสนเทศ'),
        ('ICT', 'เทคโนโลยีและการสื่อสาร'),
        ('chemi', 'เคมี'),
        ('bio', 'ชีววิทยา'),
    ]
    student_id = models.CharField(max_length=50, null=True)
    major = models.CharField(choices=CHOICES, max_length=100)
    admission_grade = models.FloatField(max_length=10)
    gpa_year_1 = models.FloatField(max_length=10)
    thai = models.FloatField(max_length=10)
    math = models.FloatField(max_length=10)
    sci = models.FloatField(max_length=10)
    society = models.FloatField(max_length=10)
    hygiene = models.FloatField(max_length=10)
    art = models.FloatField(max_length=10)
    career = models.FloatField(max_length=10)
    langues = models.FloatField(max_length=10)
    status = models.CharField(max_length=10)
    predict_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('app_users.CustomUser', default=2, on_delete=models.PROTECT, related_name="user_grade_set")

    def __str__(self):
        return self.major