import attrs


@attrs.define(frozen=True)
class BodyDimensions:
    height: float
    sh_height: float
    hip_to_ankle: float
    hip_to_knee: float
    shoulder_to_wrist: float
    arm_len: float
    tor_len: float
    low_leg: float
    up_leg: float
