# Interview questions — 5-bar blog

Answer aloud, 1–2 min each. ⭐ = deep-dive (richest answers expected).
Evidence in brackets. Wiki = `cele-life/wiki`.

## 1. Hook

1. Wiki says you eliminated a 6-DOF serial arm and an AR3/delta before the 5-bar, after a prof showed a 3D-printed demo that wasn't rigid. What did you *feel* when the bigger arm got killed — relief, disappointment? What made 5-bar feel like "the one"? [wiki `summer-school/project` VERDICT table; 2026-06-20 pivot]
2. ⭐ The first commits are a parts list (`f8c9670`, `17fdeb1`) before any math. Why start with shopping, not equations? What did you expect to be hard — and what actually was? [git 2026-06-22→24]
3. You had never done CAD (wiki: "Tumin has no CAD experience"), yet by August you had a CNC base DXF and custom STLs. When did that flip, and who or what pushed you? [wiki VERDICT; `806450f`, `3693869`]

## 2. The math wall

4. Forward kinematics went to Mathematica first (`b6bff29`), then to Python (`6cb6267`). Why Mathematica for FK and not by hand/sympy? Was there a moment the loop-closure quadratic "clicked"? [`notebooks/forward_eqns.nb`, `src/fk.py`]
5. FK returns two solutions (two working modes). Why did you pick the one you did, and did you ever consider letting the robot cross between modes? What would a professor want to know about that choice? [`src/fk.py` `y_sol`; report.tex §Kinematics]
6. ⭐ `1904184` "fix: clamp in acos" was replaced days later (`03b48a2`) by raising `ValueError` for out-of-workspace points. You first hid the problem, then made it loud. What bug or surprise made you change your mind? [`src/ik.py` history, `src/utils.py` `clamp`]
7. `03b48a2` is titled "software config to escape singularity" and adds `JOINT_SOFT = 2.9`. Was this a real singularity you hit in sim, or a precaution? What did the robot do when it got there? [`config.toml`, `fk.py`, `ik.py`]
8. Trajectories are min-jerk in *joint space*, and you added `unwrap` for angle jumps. Why joint space over Cartesian? Did you test a straight line in task space and see it curve? [`94004b1`, `src/trajectory.py`, `src/utils.py`]
9. You derived dynamics twice: Euler-Lagrange in Python (`118d715`, `euler_lagrange.ipynb`) and again in Mathematica (`ed762f0`, 13,956 lines). Why redo it? Did they agree? And why was the kinetic energy still being fixed on Sep 1 (`80bd3a3`)? [git]

## 3. Fabrication

10. ⭐ Wiki locks all links at 200 mm equal, with 150 mm base, and says 150 mm links were "too small". Code went 220/300/150 → 150/200/120 → 150/250/230 (`38979a8`). What actually forced the final geometry? Which of your earlier design reasons turned out wrong? [wiki `project` "Equal link lengths"; `config.toml` history; `specs/system.md` says 150/200/150]
11. Wiki picked MG958 servos with a torque calc (~23 kg·cm peak), then switched to a 25 kg·cm OT5325M. `parts.md` still lists MG958. Which servos are really on the robot, and what happened to the torque margin in practice? [wiki; `specs/parts.md`]
12. A 3D printer broke, a mount broke, and the base had a "CG-instability" problem (wiki log Aug 5/10). The final base is a CNC DXF (`806450f`), not "wood + nail". Tell the story of the base: what failed, and what did it teach you about moving a design from sim to wood? [wiki `log.md` 2026-08-10; `specs/base.dxf`]
13. The `4756462` commit adds an "endcap for horn slot" STL. What was wrong with the earlier endcaps, and how did you find out — by it breaking, or by it wobbling? [`specs/endcap_*.stl`]
14. Wiki plan: weigh each link and find CoM by the balance-point method. `system.md` has CoM and masses (cranker 133 g, coupler 175 g). How did the balance-point measurement go? Did the numbers surprise you vs. the thin-rod guess? [wiki 2026-07-20; `specs/system.md`]

## 4. Struggle

15. ⭐ Commit gap: `3693869` (Jul 28) → `4756462` (Aug 31), then `bb1f16a` (Sep 22). A month of silence, then a burst of Arduino commits. What was actually happening in those weeks, and what finally got you moving again? [git log dates; wiki log Aug 5 "touched daily, small"]
16. `aa1bcd0` "90 deg offset fix", plus per-side servo offsets 5° / 8° (`38979a8` changed R from 5 to 8). What did a 90° error look like on the desk the first time? Was anything scary — a link slamming into a limit? [`config.toml` `[servo]`, `src/serial_link.py`]
17. ⭐ ILC "converged" in sim at 20% gain (`b0a95f7`, `842b96e`), but your wiki log says it was "diverging in sim" on Aug 10. Which is the truth, and what did you change? How did it feel to see the convergence plot, then doubt it? [`controller.py`; `ilc_analysis.ipynb`; wiki log 2026-07-19 vs 2026-08-10]
18. ArUco markers went from 15/30 mm (`b9eb0d5`) to 40 mm (`fcf2d48`), and wiki says "pivots not stationary, servos face up" made marker placement unsolved. How did you solve where the markers go? What was the dumbest thing that broke detection? [`markers/`, `aruco_track.py`, wiki 2026-08-10]
19. `report.tex` has an open `\todo` about base length 120 vs 150 mm: "Not reconciled yet." Did that mismatch bite you on hardware? Was a sim/real discrepancy hiding in plain sight? [`report/report.tex` §2.1; later `38979a8`]

## 5. Status

20. ⭐ Last commit `f448efc`: "all aruco and hardware smoke test and calibration working fine". Walk me through the moment the camera first reported the real crank angle and it matched the servo command. What did you do right after — and what still doesn't work? [`test/aruco_calibrate.py`, `config.toml` THETA_OFFSET_L/R]
21. The wiki's plan hinged on "one real sim-vs-real gap number". Do you have it yet? If the first number were large, what would you conclude: bad model, backlash, or camera? Which would hurt your pride most? [wiki `project` critical path; `circle.py`, `serial_stress_test.py`]

## 6. Next

22. Gripper and pick-and-place were the original goal (wiki: compliant gripper, ArUco on object). Nothing gripper-related is in the repo. Dropped or deferred? Was that a hard call? [wiki `project` WHAT; `parts.md` gripper]
23. README says the STLs aren't uploaded and the blog is a TODO. Why does publishing feel like the last step? What would you want a professor reading this to tell you about the ILC-on-hardware step? [`README.md` TODO]
24. If you rebuilt the robot from scratch tomorrow, what *one* decision from week one would you reverse?
