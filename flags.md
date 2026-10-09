# Flags

## Recording coverage
- No recordings for Q8, Q11, Q19, and Q22/Q23 are not covered in `20-24.ogg`.
- `12.ogg` talks about servos (the Q11 topic), `13.ogg` covers endcaps and the base (Q12 and Q13 topics). I placed `12.ogg` under Q11 and `13.ogg` under "12 and 13". Your files may be numbered by a different list. Tell me if it is wrong.
- Q21 and Q24 are in `20-24.ogg`; Q20 start of the recording.

## [GAP] list
- Q8: min-jerk in joint space. No recording.
- Q10: final link lengths not said. Repo: `38979a8` PROXIMAL 150, DISTAL 250, BASE 230.
- Q19: base length 120 vs 150 (`report/report.tex` todo). No recording.
- Q22: gripper. No recording.
- Q23: publishing / ILC on hardware. No recording.
- Between Q15 and Q16: the draft jumps from "Arduino commits" to the offset story. Nothing in your words connects them.

## [CHECK] list (possible mishears)
| Where | Transcript | Evidence |
|---|---|---|
| Q1 | "Hugging Space" | Probably Hugging Face (LeRobot arm). Nothing in repo/wiki. |
| Q1 | "5UF" | Probably "5-bar". |
| Q1 | "BOA" | Probably BOM. |
| Q1 | "it could always be a live or a robot" | Unclear word "live" (LED?). |
| Q2 | "strong saddle" | Unknown. Maybe "strong table"/"soldering"? |
| Q4 | "Onward kinematics" | Fixed to "Forward". `forward_eqns.nb` (`b6bff29`). |
| Q4 | "SinPy" | SymPy. `euler_lagrange.ipynb` uses SymPy. |
| Q6 | "r tan", "NAND's" | Code uses `acos`, not tan (`src/ik.py`). NaN likely. Wiki log/commit `1904184` "clamp in acos". |
| Q7 | "The joints of is the steepness value" | `config.toml` `JOINT_SOFT = 2.9` (`03b48a2`). |
| Q9 | "I omega square", "angular momentum", "Hamiltonian" | Rotational kinetic energy. Commit `80bd3a3` (Sep 1) "updated the kinetic energy equation". |
| Q10 | "final conflict length" | Maybe "comfort" or "compromise". |
| Q11 | "measuring gear", "Robo", "35 kmph", "23" | Wiki: needed ~23 kg·cm peak, MG958 20 kg·cm, bought OT5325M 25 kg·cm. You said 35. `parts.md` still lists MG958. |
| Q12 | "X-links" | Maybe "extrusion links". |
| Q14 | "POM" | CoM. |
| Q15 | "Around the world", "Tanzania" | Probably "Around that time"; Tanzania unclear. |
| Q16 | "pot wipe", "98, 99" | Potentiometer wiper; units unclear (raw ADC?). `config.toml` offsets 5 and 8 deg. |
| Q17 | "ILC converge happened a lot later" | Repo: ILC convergence in sim `b0a95f7`/`842b96e` (Jul 19-23). Wiki 2026-08-10: "ILC implemented and diverging in sim only". Your answer says the divergence was PID. Wiki not matching. |
| Q20 | "I did not check if the ArUco angles were working" | Last commit `f448efc`: "all aruco and hardware smoke test and callibration working fine"; `test/aruco_calibrate.py` writes THETA_OFFSET_L/R. |
| Q21 | "creeper" | Maybe ILC. |
| Q24 | "fiber", "bring some properly" | Maybe "firmware"; second unclear. |
| Q5 | "four solutions" | `src/fk.py` returns two solutions (`y1,y2`), not four. Your count is per-arm (2x2). |

## Hints you dropped (candidate follow-up questions)
- Q1: "I was low key sad because all the time, every time I ever had the opportunity to make anything and because of my own personal constraints". Ask: which constraints, and what was the one you wanted to make?
- Q1: "it transcended the serial manipulator easiness". Ask: what was the first moment you felt that?
- Q1: "somebody who is new to this can fork my project". Ask: is the repo ready for that? README TODO says STLs not uploaded.
- Q2: "I did do some equations to find the necessary of torque". Ask: what did you find, and did it match reality?
- Q2: "some parts are not available, I have to wait days or maybe go to shops in remote places". Ask: which part, which shop?
- Q3: "it took me a lot of iterations of prints and tolerances". Ask: how many prints, what was the worst tolerance mistake?
- Q4: "I did do some of the maths in hand but only to get the idea the gist". Ask: what was the gist?
- Q7: "a merry-go-round". Ask: what did you see in the simulation exactly?
- Q9: "the worst mistake in there was I totally forgot to add the I omega square". Ask: how long before you noticed, how did you find out?
- Q10: "since it's a cantilever situation, I cannot have too many lengths". Ask: which lengths?
- Q12/13: "the end effectors were off by some centimeters". Ask: what did that look like on the table?
- Q12/13: "the servo would produce some initial jerk movement". Ask: was it measured?
- Q12/13: "I made some holes in the end cap of the pivot joints... pass a larger extrusion rod". Ask: how does that cancel the cantilever force, with a picture?
- Q14: "It did not end up proper obviously". Ask: what was not proper, which number?
- Q15: "other times, errands had me one month". Ask: what errands (only if you want it public).
- Q16: "I opened up the servos... manually soldered on the pot wipe... feedback loop without any present encoder". Not asked, and big: ask for the full story (which servo, what you read it with, what it gave you).
- Q17: "the bad joint PID values, so that was just moving crazily". Ask: where (sim or hardware), what fixed it?
- Q18: "the anchor was moving". Ask: when did you realize the anchor moves?
- Q20-24: "instead of making it as a design problem, I have to work with it as a decision problem". Ask: what does that mean concretely for your next build?
- Q20-24: "in a hobby lab like mine". Ask: which constraints?
- Q20-24: "I am not going to put any creeper or anything". Ask: what is the plan for ILC on hardware?
