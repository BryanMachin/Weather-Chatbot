import pytest
from app.app import *
from streamlit.testing.v1 import AppTest

@pytest.mark.parametrize(
    "payload",
    [
        ({"question": "Was it more humid in Boulder, CO on this day last year than it is today?"}),
        ({"question": "How is the weather in havana right now?"}),
        ({"question": "How is the weather in New York right now?"})
    ]
)
def test_query(payload):
    assert 'sessionId' in query(payload)   #Questions are answered.



@pytest.mark.parametrize(
    "payload",
    [
        ({"question": "How is the weather in New York right now?"})
    ]
)
def test_viewChatMessage(payload):
    _sessionId = query(payload)['sessionId']
    assert len(viewChatMessage(_sessionId)) != 0   #The message was loaded correctly.



@pytest.mark.parametrize(
    "payload",
    [
        ({"question": "Was it more humid in Boulder, CO on this day last year than it is today?"})
    ]
)
def test_deleteChatMessage(payload):
    _sessionId = query(payload)['sessionId']
    assert deleteChatMessage(_sessionId).status_code == 200   #There was no error deleting the message.


def test_view():
    at = AppTest.from_file("./app/app.py").run()
    assert at.title[0].value == 'Weather Chatbot'
    assert at.caption[0].value == 'A Chatbot Powered by Print AI.'
    assert at.title[1].value == 'Hello, you must log-in to start your session in WeatherBot.'
    assert at.text_input[0].label == 'Enter E-mail:'
    assert at.text_input[1].label == 'Enter password:'



def test_incorrect_login():
    at = AppTest.from_file("./app/app.py").run()
    at.text_input[0].input('username@gmail.com').run()
    at.run()
    assert len(at.warning) == 1   #Displays a warning.
    assert len(at.success) == 0   #The login was not successful.
    assert at.chat_input[0].disabled == True   #Chat input is disabled.



def test_correct_login():
    at = AppTest.from_file("./app/app.py").run()
    at.text_input[0].input('username@gmail.com').run()
    at.text_input[1].input('1234').run()
    at.run()
    assert len(at.warning) == 0   #Does not display warnings.
    assert len(at.success) == 1   #Successfully logged in.
    assert at.chat_input[0].disabled == False   #Chat input is no longer disabled.