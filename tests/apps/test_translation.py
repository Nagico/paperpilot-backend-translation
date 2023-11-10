import paperpilot_common.protobuf.translation.translation_pb2
import pytest


class TestTranslationPublic:
    @pytest.fixture
    def api(self, mock_translation_api):
        from server.apps.translation.urls import TranslationPublicController

        return TranslationPublicController()

    @pytest.mark.asyncio
    async def test_translate(self, api, context):
        response = await api.translate(
            paperpilot_common.protobuf.translation.translation_pb2.TranslationRequest(
                content="test-content",
                source_language="en",
                target_language="zh",
            ),
            context,
        )
        assert response.result == "试验内容"
