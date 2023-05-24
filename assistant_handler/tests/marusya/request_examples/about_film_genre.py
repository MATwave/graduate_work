genre_request = {
  "meta": {
    "client_id": "MailRu-VC/1.0",
    "locale": "ru_RU",
    "timezone": "Asia/Barnaul",
    "interfaces": {
      "screen": {},
      "audio_player": {}
    },
    "_city_ru": "Барнаул"
  },
  "request": {
    "command": "какой жанр у этого фильма",
    "original_utterance": "какой жанр у этого фильма",
    "type": "SimpleUtterance",
    "nlu": {
      "tokens": [
        "какой",
        "жанр",
        "у",
        "этого",
        "фильма"
      ],
      "entities": []
    }
  },
  "session": {
    "session_id": "ea660359-9a97-49b3-a043-15546672ea48",
    "user_id": "b17c7c4bb3278a07147c323fe3d6863cfd75f7a492da1358d92c7f7eaa859e53",
    "skill_id": "52401ef1-935a-49ef-bd57-1f3f83ac3447",
    "new": False,
    "message_id": 5,
    "user": {
      "user_id": "af11d9c8-1683-4e40-bbff-a48b057cea6a"
    },
    "application": {
      "application_id": "b17c7c4bb3278a07147c323fe3d6863cfd75f7a492da1358d92c7f7eaa859e53",
      "application_type": "vk"
    },
    "auth_token": "636d5f7d6fb18e1aff48bb161ab82de12012fec213a0bf2e9a9efd8b7825c69c"
  },
  "state": {
    "session": {
      "id": "05d7341e-e367-4e2e-acf5-4652a8435f93",
      "title": "Секретный мир Джеффри Стар",
      "imdb_rating": 9.5,
      "genre": [
        "Документальный"
      ],
      "description": "Шейн Доусон проводит интервью и проводит день с одним из самых интересных и противоречивых людей в Интернете, Джеффри Стар, в серии из пяти частей.",
      "actors": [
        {
          "id": "901595ba-4278-4224-b04c-974c28428a08",
          "name": "Шейн Доусон"
        },
        {
          "id": "99a9ef8f-c45d-44b3-ab09-e39685e011f5",
          "name": "Джеффри Стар"
        }
      ],
      "writers": [],
      "directors": []
    },
    "user": {}
  },
  "version": "1.0"
}

genre_response = {
  "response": {
    "text": "Документальный",
    "end_session": False
  },
  "session": {
    "session_id": "ea660359-9a97-49b3-a043-15546672ea48",
    "user_id": "b17c7c4bb3278a07147c323fe3d6863cfd75f7a492da1358d92c7f7eaa859e53",
    "message_id": 5
  },
  "session_state": {
    "id": "05d7341e-e367-4e2e-acf5-4652a8435f93",
    "title": "Секретный мир Джеффри Стар",
    "imdb_rating": 9.5,
    "genre": [
      "Документальный"
    ],
    "description": "Шейн Доусон проводит интервью и проводит день с одним из самых интересных и противоречивых людей в Интернете, Джеффри Стар, в серии из пяти частей.",
    "actors": [
      {
        "id": "901595ba-4278-4224-b04c-974c28428a08",
        "name": "Шейн Доусон"
      },
      {
        "id": "99a9ef8f-c45d-44b3-ab09-e39685e011f5",
        "name": "Джеффри Стар"
      }
    ],
    "writers": [],
    "directors": []
  },
  "version": "1.0"
}