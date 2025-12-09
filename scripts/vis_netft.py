import argparse

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

from netft_py import NetFT


def vis_netft(ip: str, tare: bool = False):
    # ------------------------------------------------------------------
    # wrench-sensor Python API
    # ------------------------------------------------------------------
    netft = NetFT(ip)
    if tare:
        netft.tare()
        print("Taring complete!")
    netft.startStreaming()

    def get_wrench():
        return netft.measurement()

    # ===============================================
    # CONFIG
    # ===============================================
    WINDOW_SIZE = 300  # Number of time steps to display
    UPDATE_RATE = 50  # ms between updates
    CHANNEL_NAMES = ["Fx", "Fy", "Fz", "Tx", "Ty", "Tz"]

    # Create sliding window buffers for each of 6 signals
    buffers = [deque(maxlen=WINDOW_SIZE) for _ in range(6)]

    # Initialize with zeros
    for buf in buffers:
        buf.extend([0] * WINDOW_SIZE)

    # ===============================================
    # FIGURE SETUP
    # ===============================================
    fig, axes = plt.subplots(6, 1, figsize=(10, 10), sharex=True)
    lines = []

    for ax, name in zip(axes, CHANNEL_NAMES):
        line, = ax.plot([], [], lw=1.5)
        lines.append(line)
        ax.set_ylabel(name)
        ax.grid(True)

    axes[-1].set_xlabel("Time Step")

    # ===============================================
    # UPDATE FUNCTION FOR ANIMATION
    # ===============================================
    def update(frame):
        # Read the newest wrench vector
        wrench = get_wrench()

        # Append new values to buffers
        for i in range(6):
            buffers[i].append(wrench[i])
            lines[i].set_data(range(len(buffers[i])), buffers[i])

            # Autoscale Y but keep X fixed
            axes[i].set_xlim(0, WINDOW_SIZE)
            axes[i].set_ylim(min(buffers[i]) * 1.1, max(buffers[i]) * 1.1)

        return lines

    # ===============================================
    # RUN
    # ===============================================
    ani = FuncAnimation(
        fig,
        update,
        interval=UPDATE_RATE,
        blit=False,
        cache_frame_data=False,
    )

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Visualize NetFT feedback.")
    parser.add_argument("ip", type=str, help="IP address for NetFT sensor.")
    parser.add_argument("--tare", action="store_true", help="Tare the sensor before starting visualization.")
    parser.set_defaults(tare=False)
    args = parser.parse_args()

    vis_netft(args.ip, args.tare)
