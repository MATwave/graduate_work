hello_request = {"meta": {
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
        "message_id": 0,
        "session_id": "eed833bc-b92f-4a8b-bcc7-399abc0685b4",
        "skill_id": "f86c4216-5140-4051-86e3-be5807d11442",
        "user": {
            "user_id": "F24F5E1D43DC903F7050EB6E8E61B4AB97662AB6DC236A4D91F0CAEDEFCDD77D"
        },
        "application": {
            "application_id": "83B5736F22E082DA0025A79C87AA2D1E773EB3F61322181AE799287E1D77ED68"
        },
        "new": True,
        "user_id": "83B5736F22E082DA0025A79C87AA2D1E773EB3F61322181AE799287E1D77ED68"
    },
    "request": {
        "command": "",
        "original_utterance": "",
        "nlu": {
            "tokens": [],
            "entities": [],
            "intents": {}
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

hello_response = {
    "version": "1.0",
    "session": {
        "message_id": 0,
        "session_id": "eed833bc-b92f-4a8b-bcc7-399abc0685b4",
        "skill_id": "f86c4216-5140-4051-86e3-be5807d11442",
        "user": {
            "user_id": "F24F5E1D43DC903F7050EB6E8E61B4AB97662AB6DC236A4D91F0CAEDEFCDD77D"
        },
        "application": {
            "application_id": "83B5736F22E082DA0025A79C87AA2D1E773EB3F61322181AE799287E1D77ED68"
        },
        "user_id": "83B5736F22E082DA0025A79C87AA2D1E773EB3F61322181AE799287E1D77ED68",
        "new": True
    },
    "response": {
        "end_session": False,
        "text": "Добро пожаловать в навык \"Практикум\". Чем я могу Вам помочь?",
        "buttons": [
            {
                "title": "спасибо",
                "hide": True
            }
        ]
    },
    "session_state": {}
}
