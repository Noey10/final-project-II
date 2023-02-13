from django.db import models

# Create your models here.
class UserPredict(models.Model):
    CHOICES = [
        ('bio', 'สาขาชีววิทยา'),
        ('microBio', 'สาขาจุลชีววิทยา'),
        ('math', 'สาขาคณิตศาสตร์'),
        ('chemi', 'สาขาเคมี'),
        ('enviSci', 'สาขาวิทยศาสตร์สิ่งแวดล้อม'),
        ('safety', 'สาขาอนามัยสิ่งแวดล้อมและความปลอดภัย'),
        ('physics', 'สาขาฟิสิกส์'),
        ('physics', 'สาขาฟิสิกส์ทางการแพทย์'),
        ('physics', 'สาขาฟิสิกส์อุตสาหกรรม'),
        ('ICT', 'สาขาเทคโนโลยีสารสนเทศหรือสาขาเทคโนโลยีและการสื่อสาร'),
        ('DSSI', 'สาขาวิทยาการคอมพิวเตอร์หรือสาขาวิทยาการข้อมูลและนวัตกรรมซอฟต์แวร์'),
        ('polymer', 'สาขาเทคโนโลยีการยางและพอลิเมอร์')
    ]
    
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
    user = models.ForeignKey('app_users.CustomUser', on_delete=models.PROTECT, related_name="user_grade_set")

    def __str__(self):
        return self.major