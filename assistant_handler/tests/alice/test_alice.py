import pytest
from tests.alice.request_examples import hello

@pytest.mark.parametrize(
    "request_data, expected_response",
    [
        (
            hello.hello_request, hello.hello_response
        ),
    ]
)
def test_get_data_assistant(test_client, request_data, expected_response):
    response = test_client.post("api/v1/assistants/voice", json=request_data)
    print(response.request.url)
    assert response.status_code == 200
    assert response.json() == expected_response