import pytest
from src.models.alice.response import AliceResponseModel
from tests.alice.request_examples import (hello,
                                          get_film,
                                          bye,
                                          about_film_description,
                                          about_film_actors,
                                          get_same_genre_film,
                                          misunderstanding,
                                          miss_context)


@pytest.mark.parametrize(
    "request_data, expected_response",
    [
        (hello.hello_request, hello.hello_response),
        (bye.bye_request, bye.bye_response),
        (about_film_description.description_request, about_film_description.description_response),
        (about_film_actors.actors_request, about_film_actors.actors_response),
        (misunderstanding.misunderstanding_request, misunderstanding.misunderstanding_response),
        (miss_context.miss_context_request, miss_context.miss_context_response)
    ]
)
def test_get_data_assistant(test_client, request_data, expected_response):
    response = test_client.post("api/v1/assistants/voice", json=request_data)
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "request_data",
    [
        get_film.request,
        get_same_genre_film.request,
    ]
)
def test_get_film(test_client, request_data):
    response = test_client.post("api/v1/assistants/voice", json=request_data)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    # так как ответ каждый раз разный - проверим валидацию модели ответа
    assert AliceResponseModel(**response.json())
