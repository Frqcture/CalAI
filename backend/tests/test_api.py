from fastapi.testclient import TestClient

from app.main import app, state


client = TestClient(app)


def setup_function() -> None:
    state.documents.clear()
    state.tokens.clear()


def test_login_success() -> None:
    response = client.post("/api/auth/login", json={"username": "engineer", "password": "calai"})
    assert response.status_code == 200
    assert response.json()["access_token"].startswith("token-")


def auth_headers() -> dict[str, str]:
    response = client.post("/api/auth/login", json={"username": "engineer", "password": "calai"})
    token = response.json()["access_token"]
    return {"Authorization": " ".join(["Bearer", token])}


def test_upload_and_chat_flow() -> None:
    headers = auth_headers()
    upload = client.post(
        "/api/documents/upload",
        files={"file": ("fuel.txt", b"Signal: LPSys_pSet\nDTC: P0087\nCal: FRP_TARGET_MIN")},
        headers=headers,
    )
    assert upload.status_code == 200

    ask = client.post("/api/chat/ask", json={"question": "What enables P0087?"}, headers=headers)
    assert ask.status_code == 200
    data = ask.json()
    assert data["sources"]
    assert data["confidence"] > 0


def test_parse_ehb_extension_validation() -> None:
    response = client.post("/api/ehb/parse", files={"file": ("bad.txt", b"Function:Fuel")})
    assert response.status_code == 400


def test_signal_dependencies_defaults() -> None:
    response = client.get("/api/signals/LPSys_pSet/dependencies", headers=auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["signal"] == "LPSYS_PSET"
    assert data["uses"]
