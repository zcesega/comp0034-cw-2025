from fleet_mix_app import create_app


def test_home_page_loads():
    """GIVEN a client WHEN home is requested THEN status is 200."""
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Fleet Mix Shift Inspector" in response.data
