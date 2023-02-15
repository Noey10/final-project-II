from django.db import models

# Create your models here.
class AppliedScience(models.Model):
    CHOICES = [
        ('bio', 'ชีววิทยา'),
        ('microBio', 'จุลชีววิทยา'),
        ('math', 'คณิตศาสตร์'),
        ('chemi', 'เคมี'),
        ('enviSci', 'วิทยศาสตร์สิ่งแวดล้อม'),
        ('safety', 'อนามัยสิ่งแวดล้อมและความปลอดภัย'),
        ('physics', 'ฟิสิกส์'),
        ('physics', 'ฟิสิกส์ทางการแพทย์'),
        ('physics', 'ฟิสิกส์อุตสาหกรรม'),
        ('ICT', 'เทคโนโลยีสารสนเทศ'),
        ('ICT', 'เทคโนโลยีและการสื่อสาร'),
        ('DSSI', 'วิทยาการคอมพิวเตอร์'),
        ('DSSI', 'วิทยาการข้อมูลและนวัตกรรมซอฟต์แวร์'),
        ('polymer', 'เทคโนโลยีการยางและพอลิเมอร์')
    ]
    major = models.CharField(choices=CHOICES, default='', max_length=100)
    admission_grade = models.CharField(max_length=20)
    gpa_year_1 = models.CharField(max_length=20)
    thai = models.CharField(max_length=20)
    math = models.CharField(max_length=20)
    sci = models.CharField(max_length=20)
    society = models.CharField(max_length=20)
    hygiene = models.CharField(max_length=20)
    art = models.CharField(max_length=20)
    career = models.CharField(max_length=20)
    langues = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return self.major

class HealthScience(models.Model):
    CHOICES = [
        ('bio', 'ชีววิทยา'),
        ('microBio', 'จุลชีววิทยา'),
        ('math', 'คณิตศาสตร์'),
        ('chemi', 'เคมี'),
        ('enviSci', 'วิทยศาสตร์สิ่งแวดล้อม'),
        ('safety', 'อนามัยสิ่งแวดล้อมและความปลอดภัย'),
        ('physics', 'ฟิสิกส์'),
        ('physics', 'ฟิสิกส์ทางการแพทย์'),
        ('physics', 'ฟิสิกส์อุตสาหกรรม'),
        ('ICT', 'เทคโนโลยีสารสนเทศ'),
        ('ICT', 'เทคโนโลยีและการสื่อสาร'),
        ('DSSI', 'วิทยาการคอมพิวเตอร์'),
        ('DSSI', 'วิทยาการข้อมูลและนวัตกรรมซอฟต์แวร์'),
        ('polymer', 'เทคโนโลยีการยางและพอลิเมอร์')
    ]
    major = models.CharField(choices=CHOICES, default='', max_length=100)
    admission_grade = models.CharField(max_length=20)
    gpa_year_1 = models.CharField(max_length=20)
    thai = models.CharField(max_length=20)
    math = models.CharField(max_length=20)
    sci = models.CharField(max_length=20)
    society = models.CharField(max_length=20)
    hygiene = models.CharField(max_length=20)
    art = models.CharField(max_length=20)
    career = models.CharField(max_length=20)
    langues = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return self.major
    
class PureScience(models.Model):
    CHOICES = [
        ('bio', 'ชีววิทยา'),
        ('microBio', 'จุลชีววิทยา'),
        ('math', 'คณิตศาสตร์'),
        ('chemi', 'เคมี'),
        ('enviSci', 'วิทยศาสตร์สิ่งแวดล้อม'),
        ('safety', 'อนามัยสิ่งแวดล้อมและความปลอดภัย'),
        ('physics', 'ฟิสิกส์'),
        ('physics', 'ฟิสิกส์ทางการแพทย์'),
        ('physics', 'ฟิสิกส์อุตสาหกรรม'),
        ('ICT', 'เทคโนโลยีสารสนเทศ'),
        ('ICT', 'เทคโนโลยีและการสื่อสาร'),
        ('DSSI', 'วิทยาการคอมพิวเตอร์'),
        ('DSSI', 'วิทยาการข้อมูลและนวัตกรรมซอฟต์แวร์'),
        ('polymer', 'เทคโนโลยีการยางและพอลิเมอร์')
    ]
    major = models.CharField(choices=CHOICES, default='', max_length=100)
    admission_grade = models.CharField(max_length=20)
    gpa_year_1 = models.CharField(max_length=20)
    thai = models.CharField(max_length=20)
    math = models.CharField(max_length=20)
    sci = models.CharField(max_length=20)
    society = models.CharField(max_length=20)
    hygiene = models.CharField(max_length=20)
    art = models.CharField(max_length=20)
    career = models.CharField(max_length=20)
    langues = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    
    def __str__(self):
        return self.major
