import cv2
import matplotlib.pyplot as plt

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

SIZE_MM = 40    # black square; ~28 px on a 640x480 webcam at ~0.7 px/mm, go 50 if detection flickers
BORDER_MM = 8   # white quiet zone, must be >= one marker cell (40/6 mm)

# name, id -- ids must match src/aruco_track.py
markers = [
    ("anchor_left", 10),
    ("anchor_right", 11),
    ("crank_left", 0),
    ("crank_right", 1),
    ("end_effector", 2),
]

# A4 page in mm; the PDF keeps physical size, so print at 100% / "actual size"
fig = plt.figure(figsize=(210 / 25.4, 297 / 25.4))
ax = fig.add_axes([0, 0, 1, 1])
cell = SIZE_MM + 2 * BORDER_MM
for k, (name, marker_id) in enumerate(markers):
    x, y = 25 + (k % 2) * (cell + 30), 25 + (k // 2) * (cell + 25)
    ax.add_patch(plt.Rectangle((x, y), cell, cell, fill=False, lw=0.3, ec="0.6"))  # cut line
    img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, 600)  # 15 px/mm
    png = cv2.copyMakeBorder(img, 120, 120, 120, 120, cv2.BORDER_CONSTANT, value=255)  # 8 mm border
    plt.imsave(f"markers/{name}_{SIZE_MM}mm.png", png, cmap="gray", dpi=15 * 25.4)  # dpi tag: prints at true size
    s = x + BORDER_MM, y + BORDER_MM
    ax.imshow(img, cmap="gray", interpolation="nearest",
              extent=(s[0], s[0] + SIZE_MM, s[1] + SIZE_MM, s[1]))
    ax.text(x, y + cell + 6, f"{name}  id {marker_id}  {SIZE_MM} mm", fontsize=7)
ax.set_xlim(0, 210)
ax.set_ylim(297, 0)
ax.axis("off")
fig.savefig("markers/markers_A4.pdf")
