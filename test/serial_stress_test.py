import random
import time

from src.serial_link import open_link

N = 30         # random moves (~1 min)
SETTLE = 0.8   # s; 0.8 was too short for full-range moves on the left servo
TOL = 15       # counts (~5 deg) allowed between commanded and measured position


def expected(deg: float) -> float:
    # pot calibration from the lab: 0 deg -> ~605 counts, 180 deg -> ~58
    return 605 - 3.04 * deg


def move(ser, d1: float, d2: float):
    ser.write(f"{d1},{d2}\n".encode())
    time.sleep(SETTLE)
    stale = ser.read(ser.in_waiting)
    if b"boot" in stale:
        raise RuntimeError("Arduino reset during move (power/ground problem)")
    # the reply is sampled before the servo moves, so resend to read the settled position
    ser.write(f"{d1},{d2}\n".encode())
    a0, a1 = ser.readline().decode().strip().split(",")
    return int(a0), int(a1)


if __name__ == "__main__":
    ser = open_link()
    ser.reset_input_buffer()
    worst_l = worst_r = 0.0
    fails = 0
    t0 = time.time()
    for i in range(N):
        d1, d2 = random.randint(30, 150), random.randint(30, 150)  # inside the sketch L_/R_ limits
        a0, a1 = move(ser, d1, d2)
        err_l, err_r = abs(a0 - expected(d1)), abs(a1 - expected(d2))
        worst_l, worst_r = max(worst_l, err_l), max(worst_r, err_r)
        if err_l > TOL or err_r > TOL:
            fails += 1
            print(f"#{i} cmd {d1},{d2} read {a0},{a1} err {err_l:.0f},{err_r:.0f}  FAIL")
    move(ser, 95, 95)
    ser.close()
    print(f"{N} moves in {time.time() - t0:.0f}s, {fails} fails, "
          f"worst err L {worst_l:.0f} R {worst_r:.0f} counts (~{max(worst_l, worst_r) / 3.04:.1f} deg)")
