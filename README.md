# Проектная работа: Голосовой Ассистент

> [Ссылка на проект](https://github.com/MATwave/graduate_work)

__Цели проекта__ - интеграция между сервисом поиска фильмов и голосовым помощником. Функционал упростит и ускорит
получение информации о фильме (актерах, режиссерах и тому подобному) в сравнении с вводом запроса через пульт
ДУ/клавиатуру

---

### Схема проекта

__Сценарий__: по запросу пользователя голосовой ассистент обращается в сервис API, который взаимодействует с ES,
получает ответ и зачитывает его.
> Если вариантов несколько, то зачитывается первый вариант.

![схема](/scheme/схума.png)

Варианты взаимодействия с помощником:

- «Кто автор фильма Х?»
- «Сколько фильмов выпустил автор Y?»
- «Сколько длится фильм Z?»
- Связки вопросов.

---

### Локальный запуск/остановка


<details><summary>Запуск admin_panel</summary>

  - Запуск
    ```makefile
    make admin_panel_up
    ```
    - Запускается контейнеры Docker в фоновом режиме
    - выполнение миграций базы данных внутри контейнера
    - собираются статические файлы
    - создастся суперпользователь | логин: `admin`, пароль: `admin`
        > доступ по [ссылке](http://localhost/admin)
    
  - Для первичного наполнения данными
  
      ```makefile
        make admin_panel_fill_db
      ```
      - исполняется скрипт переноса данных из sqlite в psql
      - тестируется полнота переноса
  
  - Тесты
    - полнота переноса данных из sqlite в psql:
      - ```makefile
        make admin_panel_test_fill
        ```
  
  - Остановка
      ```makefile
        make admin_panel_down
      ```
</details>

<details><summary>Запуск async_api</summary>
    
- Запуск
    ```makefile
    make async_api_up
    ```
    - Запускается контейнеры Docker в фоновом режиме (elasticsearch, redis, fastapi, nginx)
        > доступ к апи по [ссылке](http://localhost:81/api/openapi) 

- Тесты
    - Тесты для Postman `APItests.postman_collection.json` находятся в папке tests
    - Запуск и анализ тестов непосредственно в тестовом окружении (*по умолчанию запускаются все тесты из папки tests/funcrional/src*)
      ```commandline
      make async_api_test_up
      ```
      *команда запустит и выведет результат тестов*

- остановка
    ```makefile
    make async_api_down
    ```
</details>

<details><summary>Запуск ETL</summary>
    
- Запуск
    ```makefile
    make etl_up
    ```
    - Создается индекс `movies`,`person`,`genre` (если нет)  в Elasticsearch;
    - Запускается отслеживание изменений в таблицах `film_work`, `person`, `genre`.

- остановка
    ```makefile
    make etl_down
    ```
- тесты:
    - Файл с тестами `ETLTests.json` для Postman находится в корне проекта.

</details>

___

<details><summary>ДЛЯ РАЗРАБОТКИ</summary>
  
  Находясь в корне проекта - включи пре-коммит
  ```commandline
  $ pre-commit install
  $ pre-commit autoupdate
  ```
  Проверь работоспособность 
  ```commandline
  $ pre-commit run --all-files
  ```
</details>

---

#### Над проектом работали:

- [Антон Калужин](https://github.com/AnswerKAS)
- [Станислав Матвеев](https://github.com/MATwave)
