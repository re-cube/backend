from enum import Enum


class Facet(Enum):
    """
    ```text
                  Back
              +--------+     z ^   y
             /        /|       |  /
            /        / |       | /
           /  Top   /  |       |/
          /        /   |       *--------> x
         +--------+ Ri-|
         |        | ght+
    Left | Front  |   /
         |        |  /
         |        | /
         |        |/
         +--------+
           Bottom
    ```
    """

    FRONT = "front"
    BACK = "back"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
