from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Student(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Имя',
        null=False,
        blank=False
    )

    surname = models.CharField(
        max_length=30,
        verbose_name='Фамилия',
        null=False,
        blank=False
    )

    course = models.ManyToManyField(
        to='Course',
        verbose_name='Курсы',
        blank=True
    )

    def __str__(self):
        return f'{self.name} {self.surname}'
    
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        indexes = [models.Index(fields=['surname'])]
        ordering = ['surname']

class Course(models.Model):
    lang = [('py','Python'),('js','JavaScript'),('c','C')]

    name = models.CharField(
        choices=lang,
        max_length=30,
        verbose_name='Курсы'  
    )
    
    course_num = models.SmallIntegerField(
        default=1, 
        verbose_name="Номер курса", 
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    ) 
    
    start_date = models.DateField(
        verbose_name = 'Начало курса',
        null=True
    )
    
    end_date = models.DateField(
        verbose_name = 'Окончание курса',
        null=True
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )

    def __str__(self):
        return f'{self.get_name_display()}'

    class Meta:
        unique_together = [['name', 'course_num']]
        verbose_name = "Курс"
        verbose_name_plural = "Курсы" 
        ordering = ['name', 'course_num']

class Grade(models.Model):
    person = models.ForeignKey(
            Student, 
            on_delete=models.CASCADE,
            related_name="grades",
            verbose_name = 'Чья оценка')
    
    grade = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name = 'Оценка'
    )
    
    course = models.ForeignKey(
            Course, 
            null=True,
            on_delete=models.CASCADE,
            verbose_name = 'Курс')
    
    date = models.DateField(
        verbose_name = 'Дата оценки',
        null=True)
    
    
    date_add = models.DateField(
            auto_now_add=True, 
            null=True,
            verbose_name = 'Дата добавления'
        )
    
    date_update = models.DateField(
            auto_now=True,
            null=True,
            verbose_name = 'Дата изменения'
        )

    def __str__(self):
        return f'{self.person} {self.grade}'

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"   