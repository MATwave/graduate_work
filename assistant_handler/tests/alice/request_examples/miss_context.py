miss_context_request = {
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
    "session_id": "ca75bd6f-22d6-408f-b685-68e16a83ffef",
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
    "command": "что за жанр",
    "original_utterance": "что за жанр",
    "nlu": {
      "tokens": [
        "что",
        "за",
        "жанр"
      ],
      "entities": [],
      "intents": {
        "about_film_context_genre": {
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
      "get_film": {}
    },
    "user": {},
    "application": {}
  },
  "version": "1.0"
}

miss_context_response = {
  "version": "1.0",
  "session": {
    "message_id": 3,
    "session_id": "ca75bd6f-22d6-408f-b685-68e16a83ffef",
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
    "text": "Не понимаю о каком фильме идет речь!",
    "buttons": [
      {
        "title": "спасибо",
        "hide": True
      }
    ]
  },
  "session_state": {
    "get_film": {
      "get_film": {}
    }
  }
}