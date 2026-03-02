from fleet_mix_app import create_app


def create_client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_home_page_contains_intro():
    client = create_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Fleet Mix Shift Inspector" in response.data


def test_comparison_get_renders_form():
    client = create_client()

    response = client.get("/comparison")

    assert response.status_code == 200
    assert b"Fleet mix comparison" in response.data


def test_comparison_post_valid_years():
    client = create_client()

    response = client.post(
        "/comparison",
        data={"year1": 2005, "year2": 2006},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Mix Shift Score" in response.data


def test_manufacturers_post_valid_year():
    client = create_client()

    response = client.post(
        "/manufacturers",
        data={"year": 2005},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Top manufacturers in 2005" in response.data
