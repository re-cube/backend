import app


def test_poster():
    response = app.poster(0, 0, 0, app.Facet.FRONT)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    # TODO: golden tests


def test_hposter():
    response = app.hposter(1, 1, 1, 5, 1, 5, app.Facet.FRONT)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    # TODO: golden tests
    # app.bytes2image(response.body).show()
