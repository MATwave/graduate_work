find_film_request = {
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
    "message_id": 3,
    "session_id": "c4e13b65-9141-428a-bfcb-66d85135923b",
    "skill_id": "f86c4216-5140-4051-86e3-be5807d11442",
    "user": {
      "user_id": "F24F5E1D43DC903F7050EB6E8E61B4AB97662AB6DC236A4D91F0CAEDEFCDD77D"
    },
    "application": {
      "application_id": "83B5736F22E082DA0025A79C87AA2D1E773EB3F61322181AE799287E1D77ED68"
    },
    "new": False,
    "user_id": "83B5736F22E082DA0025A79C87AA2D1E773EB3F61322181AE799287E1D77ED68"
  },
  "request": {
    "command": "найди фильм стар трек",
    "original_utterance": "найди фильм стар трек",
    "nlu": {
      "tokens": [
        "найди",
        "фильм",
        "стар",
        "трек"
      ],
      "entities": [],
      "intents": {
        "YANDEX.BOOK.SEARCH": {
          "slots": {
            "book": {
              "type": "string",
              "tokens": {
                "start": 1,
                "end": 4
              },
              "value": "фильм стар трек"
            }
          }
        },
        "film_search": {
          "slots": {
            "Film": {
              "type": "YANDEX.STRING",
              "tokens": {
                "start": 2,
                "end": 4
              },
              "value": "стар трек"
            }
          }
        }
      }
    },
    "markup": {
      "dangerous_context": False
    },
    "type": "SimpleUtterance"
  },
  "state": {
    "session": {},
    "user": {},
    "application": {}
  },
  "version": "1.0"
}

find_film_response = {
  "version": "1.0",
  "session": {
    "message_id": 3,
    "session_id": "c4e13b65-9141-428a-bfcb-66d85135923b",
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
    "text": "Билли Стар",
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
      "page[number]": 1,
      "sort": "-imdb_rating",
      "query": "стар трек",
      "film_data": {
        "id": "8f9b0988-cddf-4af4-a876-2eee16fe402f",
        "title": "Билли Стар",
        "imdb_rating": 7.2,
        "genre": [
          "Драма",
          "Короткий",
          "Музыка",
          "Роман"
        ],
        "description": "Фильм American Boy Band Brockhampton, сопровождающий свою трилогию альбома \"Pateration\".",
        "director": [],
        "actors_names": [],
        "writers_names": [],
        "actors": [],
        "writers": [
          {
            "id": "2a5b4bd1-3352-4d30-aa5a-f604c5dc2da6",
            "name": "Алекс Рассел"
          },
          {
            "id": "a662453b-2498-4d93-85a9-7395400107a9",
            "name": "Кевин Аннотация"
          }
        ]
      }
    }
  }
}