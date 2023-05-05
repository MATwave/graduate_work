# Проектная работа: Голосовой Ассистент
> [Ссылка на проект](https://github.com/MATwave/graduate_work)

__Цели проекта__ - интеграция между сервисом поиска фильмов и голосовым помощником. Функционал упростит и ускорит получение информации о фильме (актерах, режиссерах и тому подобному) в сравнении с вводом запроса через пульт ДУ/клавиатуру

---
### Схема проекта
__Сценарий__: по запросу пользователя голосовой ассистент обращается в сервис API, который взаимодействует с ES, получает ответ и зачитывает его. 
> Если вариантов несколько, то зачитывается первый вариант.

![схема](/scheme/схума.png)

Варианты взаимодействия с помощником:
- «Кто автор фильма Х?»
- «Сколько фильмов выпустил автор Y?»
- «Сколько длится фильм Z?»
- Связки вопросов.

---
### Локальный запуск/остановка

- запуск
  ```makefile
  make up
  ```
  поднимаются сервисы:
  - nginx
  - django (admin panel) (доступен по [ссылке]())
  - psql
  - etl
  - elasticsearch
  - fastapi (доступен по [ссылке]())
  - redis
  
- остановка  
  ```makefile
  make down
  ```


___
#### Над проектом работали:

- [Антон Калужин](https://github.com/AnswerKAS)
- [Станислав Матвеев](https://github.com/MATwave)
