from email.mime import base
from re import A

import matplotlib.pyplot as plt

plt.style.use("ggplot")
plt.figure(figsize=(13, 12))
_, ax = plt.subplots(dpi=00)
# plt.grid(axis="x", color="#E5E5E5")
plt.xscale("log", base=2)
plt.yscale("log", base=2)

# plot horizontal line at 4 FLOPS/cycle
ax.axhline(y=4, color="purple", linestyle="--",
           linewidth=1.5, label="Peak Performance")

# plot vertical line at 0.5 FLOP/byte
ax.axvline(x=0.5, color="black", linestyle="-",
           linewidth=0.5, label="Memory Bound")

# plot line with slope 8 and intercept 4
x = [0.03125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16]
y = [0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128]
ax.plot(x, y, color="red", linestyle="-",
        linewidth=1.5, label="Roofline")

ax.set(xlabel='Operational Intensity (FLOPS/byte)',
       ylabel='Performance (FLOPS/cycle)', title='Roofline Plot')


filename: str = f"roofline.svg"
plt.savefig(filename, format='svg', dpi=1200,
            bbox_inches="tight", pad_inches=0.1)
