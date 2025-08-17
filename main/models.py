from moviepy import VideoFileClip
from django.db import models
from django.conf import settings
import os
import re


class NazariyMavzular(models.Model):
    mavzu = models.CharField(max_length=255)
    tartib_raqami = models.PositiveIntegerField()
    word_file = models.FileField(upload_to='nazariy_mavzular/word_fayllar/')
    html_file = models.FileField(upload_to='nazariy_mavzular/html/')

    @property
    def file_url(self):
        if self.html_file:
            return self.html_file.url
        return ''

    def __str__(self):
        return f"{self.tartib_raqami}. {self.mavzu}"

    def save(self, *args, **kwargs):
        try:
            old_file = NazariyMavzular.objects.get(pk=self.pk).html_file
            if old_file and old_file != self.html_file:
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)
        except NazariyMavzular.DoesNotExist:
            pass
        super().save(*args, **kwargs)


class AmaliyMavzular(models.Model):
    nazariy_mavzu = models.ForeignKey('NazariyMavzular', on_delete=models.SET_NULL, null=True, blank=True, related_name='amaliy_mavzular')
    mavzu = models.CharField(max_length=255)
    tartib_raqami = models.PositiveIntegerField()
    word_file = models.FileField(upload_to='amaliy_mavzular/word_fayllar/')
    html_file = models.FileField(upload_to='amaliy_mavzular/html/')


    def __str__(self):
        return f"{self.tartib_raqami}. {self.mavzu}"

    def save(self, *args, **kwargs):
        try:
            old_file = AmaliyMavzular.objects.get(pk=self.pk).html_file
            if old_file and old_file != self.html_file:
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)
        except AmaliyMavzular.DoesNotExist:
            pass
        super().save(*args, **kwargs)


class Masalalar(models.Model):
    mavzu = models.CharField(max_length=255)
    tartib_raqami = models.PositiveIntegerField()
    word_file = models.FileField(upload_to='masalalar/word_fayllar/')
    html_file = models.FileField(upload_to='masalalar/html/')

    @property
    def file_url(self):
        if self.html_file:
            return self.html_file.url
        return ''

    def __str__(self):
        return f"{self.tartib_raqami}. {self.mavzu}"

    def save(self, *args, **kwargs):
        try:
            old_file = NazariyMavzular.objects.get(pk=self.pk).html_file
            if old_file and old_file != self.html_file:
                if os.path.isfile(old_file.path):
                    os.remove(old_file.path)
        except NazariyMavzular.DoesNotExist:
            pass
        super().save(*args, **kwargs)



from django.db import models

class Videolar(models.Model):
    sarlavha = models.CharField(max_length=255)
    tartib_raqami = models.PositiveIntegerField()

    # Endi fayl emas, faqat havola (Google Drive link)
    video_url = models.URLField(
        help_text="Google Drive link: https://drive.google.com/file/d/FILE_ID/view?usp=sharing"
    )

    yakunlangan_vaqt = models.DateTimeField(auto_now_add=True)

    nazariy_mavzu = models.ForeignKey(
        'NazariyMavzular',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='videolar'
    )

    @property
    def direct_video_url(self):
        """
        Google Drive share linkdan to'g'ridan-to'g'ri (direct) video link yaratadi.
        """
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', self.video_url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        return self.video_url  # noto‘g‘ri format bo‘lsa, asl linkni qaytaradi


    def __str__(self):
        return f"{self.tartib_raqami}. {self.sarlavha} - {self.yakunlangan_vaqt}"

    class Meta:
        ordering = ['tartib_raqami']



class Test(models.Model):
    sarlavha = models.CharField(max_length=255)
    tartib_raqami = models.PositiveIntegerField()
    nazariy_mavzu = models.ForeignKey('NazariyMavzular', on_delete=models.CASCADE, related_name='testlar')

    def __str__(self):
        return f"{self.tartib_raqami}. {self.sarlavha}"

    class Meta:
        ordering = ['tartib_raqami']


class TestSavol(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='savollar')
    savol_matni = models.TextField()
    variant_a = models.TextField(max_length=255)
    variant_b = models.TextField(max_length=255)
    variant_c = models.TextField(max_length=255)
    variant_d = models.TextField(max_length=255)
    togri_javob = models.CharField(
        max_length=1,
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D')
        ]
    )

    class Meta:
        ordering = ['id']


    def __str__(self):
        return f"{self.test.sarlavha} - {self.savol_matni[:50]}"


class TestNatija(models.Model):
    foydalanuvchi = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='test_natijalari')
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='natijalar')
    togri_savollar_soni = models.PositiveIntegerField()
    jami_savollar_soni = models.PositiveIntegerField()
    no_togri_savollar_soni = models.PositiveIntegerField()
    foiz = models.FloatField()
    grade = models.CharField(max_length=20)
    yakunlangan_vaqt = models.DateTimeField(auto_now_add=True)

    def get_status(self):
        if self.foiz >= 90:
            return "A'lo"
        elif self.foiz >= 70:
            return "Yaxshi"
        elif self.foiz >= 50:
            return "Qoniqarli"
        else:
            return "Qoniqarsiz"


    def __str__(self):
        return f"{self.foydalanuvchi.username} - {self.test.sarlavha} - {self.foiz}%"
