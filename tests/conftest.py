import pytest


@pytest.fixture(autouse=True)
def patch_piface(monkeypatch):
    class FakePiFace:
        outputs = 0

        def read_outputs(self):
            return self.outputs

        def write(self, data):
            self.outputs = data

    monkeypatch.setattr("pifaceio.PiFace", FakePiFace)
