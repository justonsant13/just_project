from django.shortcuts import render
import requests
import json
import time
import os
from main.models import Graph
from main.dop_func import getting_salary

def get_vacancies(): #Функция для получения вакансий
    vacancy_name = '"project manager"' + ' OR "менеджер проект"' + ' OR "менеджер it проект"' + 'OR "менеджер ит проект"' + 'OR "менеджер интернет проект"' + 'OR "проджект менеджер"' + 'OR "проект менеджер"' + 'OR "проектный менеджер"' + 'OR "менеджер по проект"' + 'OR "менеджер по сопровождению проект"' + 'OR "управление проект"' + 'OR "управлению проект"' + 'OR "project менедж"' + 'OR "администратор проект"' + 'OR "менеджер проектів"' + 'OR "менеджер it продукт"' + 'OR "менеджер it product"'
    req = requests.get(f'https://api.hh.ru/vacancies?text={vacancy_name}'
                       f'&area=113'
                       f'&page=0'
                       f'&per_page=10'
                       f'&date_from=2022-12-21'
                       f'&date_to=2022-12-22')
    #Запрос для получения данных по вакансиям
    data = req.content.decode("utf-8")
    req.close()
    response = json.loads(data)

    getting_vacancies = []

    for vac in response['items']:
        project_manager = {}
        project_manager['name'] = vac['name']
        #Описание вакансии

        descriptionOfVacancies = ""
        descriptionOfVacancies += f"Тип Вакансии: {vac['type']['name']}\n"
        descriptionOfVacancies += vac.get("snippet", {}).get("responsibility", "")
        descriptionOfVacancies = descriptionOfVacancies.replace("<highlighttext>", " ")
        descriptionOfVacancies = descriptionOfVacancies.replace("</highlighttext>", " ")
        project_manager['description'] = descriptionOfVacancies
        project_manager['skills'] = vac['snippet']['requirement'] or "Нет"
        #Работадатель
        employer = f'Название: {vac.get("employer", {}).get("name", "")}\n' + f'Сайт: {vac.get("employer", {}).get("alternate_url", "")}\n' + f'Доверенный: {"да" if vac.get("employer", {}).get("trusted", "") else "нет"}\n'

        project_manager['employer'] = employer
        #Зарплата
        salary = ""
        if vac.get("salary", {}):
            salary = getting_salary(vac, salary)
        else:
            salary += "Не указана"
        project_manager['salary'] = salary
        project_manager['region'] = vac['area']['name']
        project_manager['published_at'] = vac['published_at']

        getting_vacancies.append(project_manager)

    return getting_vacancies


def index(request):
    graphs = Graph.objects.filter(page__exact="Главная страница")

    return render(request, "main/index.html", {"graphs": graphs})

def needable(request):

    graphs = Graph.objects.filter(page__exact="Cтраница Востребованности")

    return render(request, "main/needable.html", {"graphs": graphs})

def geography(request):

    graphs = Graph.objects.filter(page__exact="Страница Географии")

    return render(request, "main/geography.html", {"graphs": graphs})

def skills(request):

    graphs = Graph.objects.filter(page__exact="Страница Навыков")

    return render(request, "main/skills.html", {"graphs": graphs})

def vacancies(request):

    graphs = Graph.objects.filter(page__exact="Страница Вакансий")
    #Получение вакансий
    vacancies = get_vacancies()

    return render(request, "main/vacancies.html", {"graphs": м, "vacancies": vacancies})
