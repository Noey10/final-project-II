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
    admission_grade = models.CharField(max_length=10)
    gpa_year_1 = models.CharField(max_length=10)
    thai = models.CharField(max_length=10)
    math = models.CharField(max_length=10)
    sci = models.CharField(max_length=10)
    society = models.CharField(max_length=10)
    hygiene = models.CharField(max_length=10)
    art = models.CharField(max_length=10)
    career = models.CharField(max_length=10)
    langues = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    predict_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('app_users.CustomUser', on_delete=models.CASCADE)
    
# class UserAnswer(models.Model):
#     status = models.CharField(max_length=45)
#     predict = models.ForeignKey('app_prediction.UserPredict', on_delete=models.CASCADE)
    