import numpy as np
import matplotlib.pyplot as plt

class TwoLinkArm:
    def __init__(self, joint_angles=(0, 0), link_lengths=(1, 1)):
        self.link_lengths = np.array(link_lengths)
        self.joint_angles = np.array(joint_angles)

    def forward_kinematics(self):
        theta1, theta2 = np.deg2rad(self.joint_angles)  # convert to radians
        link1_x = self.link_lengths[0] * np.cos(theta1)
        link1_y = self.link_lengths[0] * np.sin(theta1)
        link2_x = link1_x + self.link_lengths[1] * np.cos(theta1 + theta2)
        link2_y = link1_y + self.link_lengths[1] * np.sin(theta1 + theta2)
        return link1_x, link1_y, link2_x, link2_y

    def plot(self):
        link1_x, link1_y, link2_x, link2_y = self.forward_kinematics()
        plt.plot([0, link1_x, link2_x], [0, link1_y, link2_y])
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        plt.show()

arm = TwoLinkArm((45, 45))
arm.plot()
