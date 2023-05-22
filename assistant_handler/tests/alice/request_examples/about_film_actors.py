actors_request = {
  "meta": {
    "locale": "ru-RU",
    "timezone": "UTC",
    "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
    "interfaces": {
      "screen": {},
      "payments": {},
      "account_linking": {}
    }
  },
  "session": {
    "message_id": 4,
    "session_id": "04e10702-40c6-4805-8544-45bec2566dac",
    "skill_id": "f86c4216-5140-4051-86e3-be5807d11442",
    "user": {
      "user_id": "F24F5E1D43DC903F7050EB6E8E61B4AB97662AB6DC236A4D91F0CAEDEFCDD77D"
    },
    "application": {
      "application_id": "83B5736F22E082DA0025A79C87AA2D1E773EB3F61322181AE799287E1D77ED68"
    },
    "user_id": "83B5736F22E082DA0025A79C87AA2D1E773EB3F61322181AE799287E1D77ED68",
    "new": False
  },
  "request": {
    "command": "кто играет",
    "original_utterance": "кто играет",
    "nlu": {
      "tokens": [
        "кто",
        "играет"
      ],
      "entities": [],
      "intents": {
        "about_film_context_actor": {
          "slots": {}
        }
      }
    },
    "markup": {
      "dangerous_context": False
    },
    "type": "SimpleUtterance"
  },
  "state": {
    "session": {
      "get_film": {
        "page[size]": 1,
        "page[number]": 20,
        "sort": "-imdb_rating",
        "film_data": {
          "id": "53d660a1-be2b-4b53-9761-0a315a693789",
          "title": "Kinect Star Wars: дуэль",
          "imdb_rating": 8.8,
          "genre": [
            "Научная фантастика"
          ],
          "description": "Телевизионный фильм, основанный на Kinect Star Wars.",
          "director": [],
          "actors_names": [],
          "writers_names": [],
          "actors": [
            {
              "id": "02225011-c43e-45c1-bac1-ea34307b377e",
              "name": "Томас Морли"
            },
            {
              "id": "61a42440-4197-4566-926d-9b05ebe61f44",
              "name": "Крис Пратт"
            },
            {
              "id": "d0ce62b0-c102-4d00-9728-c84c6625a69b",
              "name": "Шон Томпсон"
            },
            {
              "id": "eed4a0b3-be4a-4c1f-a8be-12e97fd0b8f4",
              "name": "Майкл Бендер"
            }
          ],
          "writers": []
        }
      }
    },
    "user": {},
    "application": {}
  },
  "version": "1.0"
}

actors_response = {
  "version": "1.0",
  "session": {
    "message_id": 4,
    "session_id": "04e10702-40c6-4805-8544-45bec2566dac",
    "skill_id": "f86c4216-5140-4051-86e3-be5807d11442",
    "user": {
      "user_id": "F24F5E1D43DC903F7050EB6E8E61B4AB97662AB6DC236A4D91F0CAEDEFCDD77D"
    },
    "application": {
      "application_id": "83B5736F22E082DA0025A79C87AA2D1E773EB3F61322181AE799287E1D77ED68"
    },
    "user_id": "83B5736F22E082DA0025A79C87AA2D1E773EB3F61322181AE799287E1D77ED68",
    "new": False
  },
  "response": {
    "end_session": False,
    "text": "Томас Морли, Крис Пратт, Шон Томпсон, Майкл Бендер",
    "buttons": [
      {
        "title": "спасибо",
        "hide": True
      }
    ]
  },
  "session_state": {
    "get_film": {
      "page[size]": 1,
      "page[number]": 20,
      "sort": "-imdb_rating",
      "film_data": {
        "id": "53d660a1-be2b-4b53-9761-0a315a693789",
        "title": "Kinect Star Wars: дуэль",
        "imdb_rating": 8.8,
        "genre": [
          "Научная фантастика"
        ],
        "description": "Телевизионный фильм, основанный на Kinect Star Wars.",
        "director": [],
        "actors_names": [],
        "writers_names": [],
        "actors": [
          {
            "id": "02225011-c43e-45c1-bac1-ea34307b377e",
            "name": "Томас Морли"
          },
          {
            "id": "61a42440-4197-4566-926d-9b05ebe61f44",
            "name": "Крис Пратт"
          },
          {
            "id": "d0ce62b0-c102-4d00-9728-c84c6625a69b",
            "name": "Шон Томпсон"
          },
          {
            "id": "eed4a0b3-be4a-4c1f-a8be-12e97fd0b8f4",
            "name": "Майкл Бендер"
          }
        ],
        "writers": []
      }
    }
  }
}