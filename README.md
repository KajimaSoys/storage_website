# storage_website
___

## Инструкция по установке и запуску системы
### 1. Требования
```Python 3.8+```

```PostgreSQL 12+```

___
### 2. Настройка проекта
#### 1. Склонируйте репозиторий на свою машину
```shell
git clone https://github.com/KajimaSoys/storage_website.git
```
#### 2. Создайте БД в PostgreSQL
```shell
psql -U postgres -d postgres
```

```postgres-psql
CREATE DATABASE storage_db;
```

#### 3. Укажите соответствующие настройки в файле ```.env```
#### 4. Создайте виртуальное окружение
```shell
python -m venv venv
```
#### 5. Установите необходимые библиотеки
```shell
pip install -r req.txt
```
___
### 3. Запуск проекта
#### 1. Запуск виртуального окружения
```shell
 .\venv\Scripts\activate
```
#### 2. Запуск сервера
```shell
uvicorn main:app --reload
```
#### 3*. Выключение проекта
Выключаем сервер
```shell
CTRL + C
```
Выходим из окружения
```shell
deactivate
```
