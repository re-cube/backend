import io
import logging

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from PIL import Image, ImageDraw

from type import Facet

app = FastAPI(title="Re-cube")


def read_poster(x, y, z, facet):
    filename = f"storage/{x}.{y}.{z}.{facet}/poster.png"
    try:
        with open(filename, "rb") as f:
            return f.read()
    except FileNotFoundError:
        logging.info(f"File {filename} not found")
        with open("assets/blank-cude-edge.png", "rb") as f:
            return f.read()


def read_poster_image(x, y, z, facet, poster_res):
    data = read_poster(x, y, z, facet)
    img = bytes2image(data).resize((poster_res, poster_res))
    img = add_coordinate_to_poster(img, x, y, z)
    return img


def add_coordinate_to_poster(img, x, y, z):
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), f"{x}.{y}.{z}", fill="white", size=10)
    return img


def bytes2image(data):
    return Image.open(io.BytesIO(data))


def image2bytes(img):
    with io.BytesIO() as output:
        img.save(output, format="GIF")
        return output.getvalue()


def hposter_image(x1, y1, z1, x2, y2, z2, facet, poster_res) -> Image.Image:
    """create new image from several posters as a tile"""
    assert x1 <= x2 and y1 <= y2 and z1 <= z2, "x1 <= x2 and y1 <= y2 and z1 <= z2"
    match facet:
        case Facet.FRONT | Facet.BACK:
            assert y1 == y2, "for front and back facet y1 == y2"
            hposter = Image.new(
                "RGB", (poster_res * (x2 - x1 + 1), poster_res * (z2 - z1 + 1))
            )
            for x in range(x1, x2 + 1):
                for z in range(z2, z1 - 1, -1):
                    poster = read_poster_image(x, y1, z, facet, poster_res)
                    hposter.paste(
                        poster, (poster_res * (x - x1), poster_res * (z2 - z))
                    )
            return hposter

        case Facet.LEFT | Facet.RIGHT:
            assert x1 == x2, "for left and right facet x1 == x2"
            hposter = Image.new(
                "RGB", (poster_res * (y2 - y1 + 1), poster_res * (z2 - z1 + 1))
            )
            for y in range(y1, y2 + 1):
                for z in range(z2, z1 - 1, -1):
                    poster = read_poster_image(x1, y, z, facet, poster_res)
                    hposter.paste(
                        poster, (poster_res * (y - y1), poster_res * (z2 - z))
                    )
            return hposter
        case Facet.TOP | Facet.BOTTOM:
            assert z1 == z2, "for top and bottom facet z1 == z2"
            hposter = Image.new(
                "RGB", (poster_res * (x2 - x1 + 1), poster_res * (y2 - y1 + 1))
            )
            for x in range(x1, x2 + 1):
                for y in range(y2, y1 - 1, -1):
                    poster = read_poster_image(x, y, z1, facet, poster_res)
                    hposter.paste(
                        poster, (poster_res * (x - x1), poster_res * (y2 - y))
                    )
            return hposter
    raise ValueError(f"Invalid facet {facet}")


# Routes


@app.get(
    "/poster/{x}.{y}.{z}/{facet}",
    responses={200: {"content": {"image/png": {}}}},
    response_class=FileResponse,
)
def poster(x: int, y: int, z: int, facet: Facet, poster_res=256):
    img = read_poster(x, y, z, facet)
    return Response(content=img, media_type="image/png")


@app.get(
    "/hposter/{x1}.{y1}.{z1}/{x2}.{y2}.{z2}/{facet}",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
def hposter(
    x1: int,
    y1: int,
    z1: int,
    x2: int,
    y2: int,
    z2: int,
    facet: Facet,
    poster_res: int = 64,
):
    img = hposter_image(x1, y1, z1, x2, y2, z2, facet, poster_res)
    return Response(content=image2bytes(img), media_type="image/png")
