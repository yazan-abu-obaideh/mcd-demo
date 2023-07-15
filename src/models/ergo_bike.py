import attrs


@attrs.define(frozen=True)
class ErgoBike:
    seat_x: float
    seat_y: float
    handle_bar_x: float
    handle_bar_y: float
    crank_length: float
