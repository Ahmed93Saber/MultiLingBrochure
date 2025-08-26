from types import SimpleNamespace
from brochure_app.llm import stream_gpt

class FakeStream:
    def __iter__(self):
        chunks = [
            SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="Hello"))]),
            SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=" world"))]),
            SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="!"))]),
        ]
        for c in chunks:
            yield c

class FakeChat:
    def completions(self):
        raise NotImplementedError
    def create(self, **kwargs):
        return FakeStream()

class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))
    def _create(self, **kwargs):
        assert kwargs.get("stream", False) is True
        return FakeStream()

def test_stream_gpt_with_fake_client():
    client = FakeClient()
    out = []
    for partial in stream_gpt("Say hello", system_prompt="sys", model="fake", client=client):
        out.append(partial)
    assert out[-1] == "Hello world!"
    assert out[0] == "Hello"
