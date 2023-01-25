from django.db import models
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage() #Для хранения картинок




class Graph(models.Model): #Модель графика с описанием и страницой куда он подгружается
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    page = models.CharField(max_length=100)
    image = models.ImageField(storage=fs, upload_to="graphs")

    def __str__(self):
        return f"График - {self.name}"
