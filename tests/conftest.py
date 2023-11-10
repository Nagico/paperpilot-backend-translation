import os

import django
import pytest
from django.core import management


# region startup
def pytest_addoption(parser):
    parser.addoption(
        "--staticfiles",
        action="store_true",
        default=False,
        help="Run tests with static files collection, using manifest "
        "staticfiles storage. Used for testing the distribution.",
    )


def pytest_configure(config):
    os.environ["DJANGO_ENV"] = "test"
    os.environ["DJANGO_SECRET_KEY"] = "secret"
    os.environ["DJANGO_SETTINGS_MODULE"] = "server.settings"

    os.environ["CACHE_URL"] = "locmem://"

    django.setup()

    if config.getoption("--staticfiles"):
        management.call_command("collectstatic", verbosity=0, interactive=False)


@pytest.fixture
def mock_translation_api(mocker):
    def _mock_translation_api(*args, **kwargs):
        mock_response_content = {
            "from": "en",
            "to": "zh",
            "trans_result": [{"dst": "试验内容", "src": "test-content"}],
        }
        mock_response = mocker.Mock()
        mock_response.json.return_value = mock_response_content
        mock_post = mocker.patch(
            "aiohttp.ClientSession.post", return_value=mock_response
        )
        return mock_post

    return _mock_translation_api


# endregion
