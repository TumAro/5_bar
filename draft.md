# 5-bar draft

Source: `transcripts/*.txt` (whisper medium). Sections follow `questions.md`. Recordings 8, 11 and 19 do not exist. See flags.md.

## 1. Why the 5-bar, after the 6-DOF arm was cancelled

Initially, I had chosen the 6DOF serial arm, particularly the AR3, Delta, or the one from Hugging Space [CHECK: "Hugging Space"]. What I thought would be fun is that I would not have to fabricate the whole arm, the hardware and everything. There is the open source firmware, the software, the whole bill of parts and bill of mechanics, whatever exists. I could just build it after buying the parts and just start working on the simulation and the software and everything. To be honest, I had a rough idea what I would do, but I did not know totally, as I was also just starting.

Then it was cancelled because we could not buy the parts, and printing the rigid things would take like 2-3 months. It was a lot of tedious and very costly process, so we had to cancel it, and I was low key sad. Every time I ever had the opportunity to make anything, because of my own personal constraints, it could always be a live or a robot or a Bluetooth robot, the cliches.

But after talking with Professor Dr. Anirban Nath, he advised me to get the 5 bar made. What made me excited for that was for the 5UF [CHECK: "5UF"], I was supposed to design the whole thing. Initially I was thinking that I would not make the hardware and would work on something pre-existing. This was a huge thing because it wasn't only a parallel manipulator, it transcended the serial manipulator easiness. There was a new challenge: I have to solve for those coupled mechanisms, those coupled equations, so many passive angles and everything. So I can use a lot of math, which is my expertise, not hardware. Software is also my expertise.

After a while, I was supposed to design the whole CAD, the whole trajectory. I had to make the BOA [CHECK: "BOA", probably BOM] myself, the firmware and software myself. That gave me a more exciting idea: if I make all of that, I can make my whole project open source, the list of materials, the mechanism, the math, the software, everything. There are a lot of arms, because the arm is a very popular thing, but there are not much parallel manipulator projects. There are, but not the beginner friendly ones. If I was making that, somebody who is new to this can fork my project and make it their own. Since I face the hard problems, I know what to make easy, like mechanisms and maths and everything. Somebody learning for the first time can find the easy thing, they don't have to go through the hard and complex things like I had to go. So that made me excited. Plus, it was a full full stack project.

## 2. Why start with shopping, not equations

To be honest, I'm not sure. I decided that I would need a strong saddle [CHECK: "saddle"], I would need an Arduino, I would need wires, the obvious stuff. Then I thought, I have arms, right, and what is the most rigid arms? I should have went for 3D printed, but aluminium extrusions were the most prominent thing in my eyes. Then I realized I want this and this size, and of course maybe I'll be having smaller sizes of the links, so I might as well cut them off, so let's just buy them. That's what I thought. A little bit later I did do some equations to find the necessary torque.

What I expected to be hard was the whole project, like how the software and the same tutorial would happen. What I did not realize was that the whole hardware fabrication was supposed to be so hard. The precision it needed. The system can be wobbly, which would not be the same in the designs. Real life has some little gaps, precision, it hurts. I cannot find this and that part, I cannot have this and that thing cut off. Some parts are not available, I have to wait days or maybe go to shops in remote places to find them. Sometimes things would work in hypothesis, in theory, but not at all work in hardware when I have physically applied them. So the hardware thing was the hardest, as for fabrication.

[IMG: `specs/parts.md` first commit `f8c9670`]

## 3. CAD, from no experience to custom STLs

What I needed was some basic 3D prints. I thought, let me not just go into deep CAD and the whole engineering design thing, and let me just do simple thing with Tinker CAD. Tinker CAD is like toying with a child's toy. It was very easy and obvious to use, but from my point of view as a beginner, it was taking too much time. I need one corner, I have to make a cylinder, I have to make a second corner, I need another cylinder. It was so weird, but I still spent a day.

Then I found a video and saw that CAD is even easier than Tinker CAD. I just have to draw and then extrude the shapes and that's it. Maybe starting from Tinker CAD helped because I understood how the shapes go with each other properly. Then I dived to the engineering drawing stuff, and because of my little bit of geometry practices I knew what constraints are, what kind of constraint effects, and different degrees of freedom. So it did help me. I would not lie, it took me a lot of iterations of prints and tolerances and a lot of things. By the end of it, what I came to realize is it's just drawing a very, I don't know what to say.

[IMG: `specs/endcap_1.stl`, `specs/endcap_2.stl`, `specs/brackets.stl` (commit `3693869`)]

## 4. Forward kinematics: Mathematica, then Python

Forward kinematics equations are significantly harder. By harder I mean the systems are very complex for parallel manipulator closed systems, because the loop closure equations are coupled, and to solve coupled equations with a lot of variables it becomes very tedious. On top of that there are passive angles and the velocity derivatives of passive angles, so the calculation becomes very complicated really fast.

To fight with that, I did some of the maths by hand, but only to get the gist. When I finalized that okay, equations of vectors, I know what it is supposed to be, I went to Mathematica because of its reliability for complex calculations underneath the machinery. For Python, I thought maybe I can work with SinPy [CHECK: SymPy] and transfer the symbolic equations to a Python function and quickly calculate the torques and the trajectories and everything. Little did I know SinPy and the whole calculation is very computationally heavy, and I am talking about without simplifying the trigonometric components and identities. That is why I used and stayed with Mathematica, for the reliability of the symbolic math for fast analysis.

[IMG: `notebooks/forward_eqns.nb` (commit `b6bff29`)]

## 5. Why I picked the elbow position I did

For FK, we have two arms decoupled from the end effector, so there are two circle intersections for each of the arms. That is two solutions for each of the arms for a fixed end effector position. So there are technically four solutions, not two. When I say four, what I mean is left elbow out, left elbow in, right elbow out, right elbow in, and the combination of that.

Why did I choose the one I did? Since it is an independent project with a lot of moving machinery and parts, like jumper wires and stuff, it would be safe to have an elbow outside position, because there is a lot of empty space on my table. If something goes bad, the wires get jumbled up. For the working process it's not necessary to move between the modes, and the two modes do not really make any huge changes. So sticking with any of them is okay.

## 6. Raising an error instead of clamping the acos

At a point it has the value of zero, and in our equations for tan or r tan [CHECK: "r tan", acos in `src/ik.py`?], it silently blows up the equation into a NAND's output [CHECK: "NAND's", probably NaN]. Instead of suppressing that and eventually finding a bad solution and scratching our heads, with the solution not working, it's better to just throw an error to understand that the point is going outside of our workspace.

## 7. Escaping the singularity (JOINT_SOFT)

The joint's [CHECK: "The joints of is the steepness value for the joint", is this `JOINT_SOFT = 2.9`?] steepness value for the joint. Before, what was happening in the simulation with a little bit of acceleration in the servo was that the whole thing was moving round and round, a merry-go-round. Obviously there were singularity points at the outer line of the workspace, at the points where the elbow joints make 90 degrees and get perpendicular to each other. We could not let the whole thing just move through the singularity points randomly. That is also not a viable thing in real-life solutions, because joints are not that smooth and buttery. That's why we had to increase the joint softness.

## 8. Min-jerk in joint space

[GAP: no recording for Q8 (why min-jerk in joint space, task-space straight line test)]

## 9. Euler-Lagrange twice (SymPy, then Mathematica)

I made the Python notebook to calculate the Euler Lagrange symbolically using SymPy. That was in an early stage of the project, when calculating torque. The worst mistake in there was I totally forgot to add the I omega square, the angular momentum, in the Hamiltonian. So, sorry, the Lagrange, we are not in Hamiltonian [CHECK: "I omega square" is rotational kinetic energy, "angular momentum"/"Hamiltonian" as said; see commit `80bd3a3` "updated the kinetic energy equation"]. The calculation was a bit huge off. By the time I came around to fix it, it was just very difficult to work in Python, because the equations were complicated and the computation takes too much time in symbolic Python. That's why I just moved to Mathematica, which was quick to code the whole math, analyze the math and fix everything.

[IMG: `notebooks/euler_lagrange.ipynb` (`94004b1`), `notebooks/dynamics.nb` (`ed762f0`)]

## 10. Why the link lengths changed

The length of the geometry was too ambitious, because the weight in the final diagram was not managed realistically. That's why the lengths were 220, 300, and 150 millimeters. Then I needed to make it realistic based on the length of the link and how much of the model could fit around. Since it's a cantilever situation, I cannot have too many lengths, and that is why I had to minimize something and maximize other things to escape singularity in the fabrication and make the robot work. After a lot of, I had to realize the final conflict length [CHECK: "final conflict length", comfort? compromise?]. That is the final length for now.

[GAP: final lengths not stated. `config.toml` at `38979a8` has PROXIMAL=150, DISTAL=250, BASE=230]

[IMG: `38979a8` diff of `config.toml` / `five_bar.xml`]

## 11. Servos

We needed a high torque servo, possibly a measuring gear [CHECK: "measuring gear", metal gear?], so we tried to find it, but we could not find that in the series 958 in the stores or Robo or any website [CHECK: "Robo", robu.in?]. So we had to go with an option, whichever is available on the online aspect. While we were on the find, we could not see anything near 23, and the nearest possible torque was 35 kmph [CHECK: "35 kmph", kg·cm? wiki says OT5325M, 25 kg·cm]. So we got that, the OT, yada yada yada, I forgot the servo name, I have to see it now.

[Note: this text came from recording `12.ogg`, matched to Q11 by content. See flags.md]

## 12 and 13. The wooden base, the resin base, the endcaps

We faced a lot of issues. First, I thought that we did the endcaps. The whole designing process was very complicated. There was a whole session on designing the endcap for the anchored side. There was a whole session on designing the endcap for the pivot side in the passive joints, the joints connecting the distal and the proximal lengths. And the end effectors were off by some centimeters. So to make them parallel, or they have to meet each other at a point, I had to design that in some way. There are pictures for each of them and STLs, a lot of iterations.

Anyhow, the wood was very unstable. For the CNC cutting machine, we took a plywood and cut the plywood with that CNC and nailed it. That was the worst situation we could ever face. The design, I'll provide again, had a lot of flaw. The nails were not rigid. The plywood was like a sandwich of smaller thinner plates, so it would just get open and it was very wobbly. It was a reverse cantilever, where the servo rotation axis was facing downwards, so the cantilever was very unstable. The issue was that the CG, the center of gravity of all the X-links [CHECK: "X-links"], was very far from the CG of the base. Every move, the servo would also produce some initial jerk movement which would really un-stabilize the whole thing.

So we had to totally purge the wooden board. We had to go design a solid base. That also happened in iterations. Just for the solid base, we could not spare a lot of materials, so we went for resin printing because of the 100% infill. That supported the weight by a lot. Because we had to change to the resin printing, we could not make the servos face downwards anymore, because the base would clamp the servos facing upwards. That also gave us more ease, because I made some holes in the end cap of the pivot joints, and that helped me pass a larger extrusion rod, which would cancel out the cantilever force of the whole system. There was a lot of moving process while making the whole base and the whole system work stable.

[IMG: `specs/base.dxf` / `specs/base.svg` (`806450f`) for the plywood CNC design. `specs/endcap_horn slot.stl` (`4756462`). Photos of the wooden and resin bases are not in the repo.]

## 14. Mass and center of mass

Not really. The CoM [CHECK: "POM"] and the center of mass and the mass calculation did not really surprise me. It was more like to find the center of the axis, center of the link from an axis to axis point of view. I did the calculation for something. Right now I forgot what. Oh yeah, maybe it was for the precision calculation for the mass and the center of mass points, to make a proper calculation for the trajectory. It did not end up proper obviously, but we tried that.

[IMG: `specs/system.md`]

## 15. The gap from July 28 to September 22

[CHECK: "Around the world", probably "Around that time"] I had a lot of things going on. The first thing was I had to prepare the assignment. The last date of my assignments was September 30th. I could not just rush and use statistics, I had to learn and understand the math topics. So the assignments and writing them down, then getting a little bit of hardware ready. When I said I was getting the endcaps and the base design ready, I had to wait for one iteration to complete, get the room cleared, and get the printed, some screws going to fit. There was the wiggle room. I had to go to Tanzania [CHECK: "Tanzania"] to buy the screws. All of this was happening, handling with those and my assignments. Other times, errands had me one month. When everything was done properly, I hooked up the Arduino and started testing the smoke test to see if the hardware was working or not. That is why the Arduino commits.

[IMG: `bb1f16a`, `aa1bcd0` (`src/arduino/five_bar_servo/five_bar_servo.ino`)]

## 16. The 90 degree offset

Nothing was scary. There was a bit of error in precision when the servos were made, so the 90 degrees was not exactly 90 and they were tilted. I had to eyeball at every point from the raw 98, 99, the raw values which I was taking from the pot wipe [CHECK: "pot wipe", potentiometer wiper?], and testing if it was exactly 90 degrees or not. I was also taking the shadows and stuff to see if it was perfectly 90 degrees or not.

Also, more information: I opened up the servos and there was a potentiometer inside the servos, and I manually soldered on the pot wipe to get some output values, which is acting as a kind of feedback loop without any present encoder. So yeah, nothing was slamming into each other.

[IMG: `config.toml` `[servo]` OFFSET_L/OFFSET_R (`aa1bcd0`, `38979a8`)]

## 17. ILC "converged" vs "diverging"

Oh no, the diverging was a different thing. It was the issue when we faced the bad joint PID values, so that was just moving crazily. The ILC converge happened a lot later. The ILC was perfect, there was no issue in that.

[CHECK: "ILC converge happened a lot later". Repo: sim convergence `b0a95f7`, `842b96e` (Jul 19-23). Wiki 2026-08-10 says "ILC implemented and diverging in sim only"]

[IMG: `notebooks/convergence_plot.png`]

## 18. ArUco marker size and placement

The ArUco marker had to increase in size. Remember when the servo was facing down and it was a cantilever, at that time I could just paste the ArUco on the back side of the servo, that is the top portion, and work with it. But now the anchor was moving, so I need a stationary point to put the ArUco in for the anchor position. So what I did instead was, I can show the picture, in the frame and the side I put some rods which were hanging on the side of the servo and I pasted the ArUco there. I had to put the picture to this side exactly. And the size of the ArUco had to increase because the camera was put a little higher, a little bit taller, so the ArUco had to increase in size from 30 millimetre to 40 millimetre.

[IMG: `markers/*_40mm.png` (`fcf2d48`), `markers/markers_A4.pdf`. Photo of the rods is not in the repo.]

## 19. Base-length mismatch (120 vs 150)

[GAP: no recording for Q19]

## 20. Where the hardware stands

Actually, I did not check if the ArUco angles were working properly or not. I have to test that. I was just checking if the ArUco markers were marked properly through the camera. [CHECK: last commit `f448efc` says "all aruco and hardware smoke test and callibration working fine"]

## 21. The sim vs real gap number

I don't have the sim versus real gap number yet. So I cannot conclude the model, what it is, and I am not going to put any creeper [CHECK: "creeper", ILC?] or anything. The project is going to differ at this position of sim to real gap, because the whole thing based on the hardware is so complicated. If I put another creeper and more accuracy, I have to restart from instead of making it as a design problem, I have to work with it as a decision problem.

## 22. Gripper and pick-and-place

[GAP: no recording for Q22]

## 23. Publishing and ILC on hardware

[GAP: no recording for Q23]

## 24. What I would reverse from week one

That answers my last question: from week one, I would not start to just making the whole software hardware and fiber [CHECK: "fiber", firmware?]. Instead, I need to bring some properly [CHECK: unclear, "bring some properly"]. What am I trying to solve? Am I going to make it only move round and round, or am I going to pick and place? Based on what would be the end goal, a lot of things can change, and that also helps in what kind of BOM I need, because apparently in this sector, there does not exist a proper general solution that okay, I make one thing and it can do everything. I won't say it does not, but it is more complicated than what it feels like. I cannot just hook up a lot of rods and everything and expect it to do everything. To make a general solution, it needs a lot of precision control and precision hardware. In a hobby lab like mine, I need to first answer what problem I need to solve. Only then I can start building the BOM and everything. That is what I learned.
