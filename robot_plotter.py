import math
from typing import List

import matplotlib.pyplot as plt
import yaml

# Huge thanks to ChatGPT


class RobotData:
    def __init__(self, name, rob_pose: list, footprint: list):
        self.name = name
        self.center = tuple(rob_pose)
        self.outer_shape = self.__covert_footprint_to_shape(
            rob_pose, footprint)
        self.rotation_radius = self.__calculate_rotation_radius(footprint)
        self.heading = self.__find_heading(self.outer_shape)

    def __covert_footprint_to_shape(self, rob_pose: list, fp: list) -> List[tuple]:
        """
        Convert footprint (LW, RW, FL, BL) (relative to pose) to shape positions (relative to world)
        """
        rob_x = rob_pose[0]
        rob_y = rob_pose[1]
        rob_theta = rob_pose[2]

        LW = fp[0]  # Left Width
        RW = fp[1]  # Right Width
        FL = fp[2]  # Front Length
        BL = fp[3]  # Back length

        left_front = (rob_x + FL*math.cos(rob_theta) - LW*math.sin(rob_theta),
                      rob_y + FL*math.sin(rob_theta) + LW*math.cos(rob_theta))
        right_front = (rob_x + FL*math.cos(rob_theta) + RW*math.sin(rob_theta),
                       rob_y + FL*math.sin(rob_theta) - RW*math.cos(rob_theta))
        right_back = (rob_x - BL*math.cos(rob_theta) + RW*math.sin(rob_theta),
                      rob_y - BL*math.sin(rob_theta) - RW*math.cos(rob_theta))
        left_back = (rob_x - BL*math.cos(rob_theta) - LW*math.sin(rob_theta),
                     rob_y - BL*math.sin(rob_theta) + LW*math.cos(rob_theta))

        return [left_front, right_front, right_back, left_back]

    def __calculate_rotation_radius(self, footprint: list):
        """
        Using LW and FL of footprint (LW, RW, FL, BL) to calculate rotation radius
        """
        return math.sqrt(math.pow(footprint[0], 2) + math.pow(footprint[2], 2))

    def __find_heading(self, outer_shape: list):
        """
        return a list of three points [head, left, right] to form heading sign
        """
        head = ((outer_shape[0][0]+outer_shape[1][0])/2,
                (outer_shape[0][1]+outer_shape[1][1])/2)

        left_mid = ((outer_shape[0][0]+outer_shape[3][0])/2,
                    (outer_shape[0][1]+outer_shape[3][1])/2)
        left = ((outer_shape[0][0]+left_mid[0])/2,
                (outer_shape[0][1]+left_mid[1])/2)

        right_mid = ((outer_shape[1][0]+outer_shape[2][0])/2,
                     (outer_shape[1][1]+outer_shape[2][1])/2)
        right = ((outer_shape[1][0]+right_mid[0])/2,
                 (outer_shape[1][1]+right_mid[1])/2)

        return [head, left, right]


def plot_robot(robot: RobotData):
    x_center, y_center, theta_center = robot.center

    # Extract x and y coordinates of outer shape
    x_outer, y_outer = zip(*robot.outer_shape)

    # Plot center point
    plt.plot(x_center, y_center, 'ro')  # 'ro' for red circles
    plt.text(x_center, y_center,
             f'{robot.name}({x_center:.3f}, {y_center:.3f}, {theta_center:.3f})')

    # Plot outer shape
    plt.plot(x_outer + (x_outer[0],), y_outer +
             (y_outer[0],), 'c-')  # 'c-' for cyan lines

    # Plot robot heading
    x_heading, y_heading = zip(*robot.heading)
    plt.plot(x_heading + (x_heading[0],), y_heading + (y_heading[0],), 'c-')

    # Plot rotation footprint
    rotate_circle = plt.Circle(
        (x_center, y_center), robot.rotation_radius, fill=False, color='y', linestyle='--')
    print(
        f'Rotation radius of robot [{robot.name}]: {robot.rotation_radius} m')

    plt.gca().add_patch(rotate_circle)


def main():

    print("===== version 1 =====")

    # read input.yaml
    with open("input.yaml", "r") as f:
        input_data = yaml.load(f, Loader=yaml.FullLoader)

    # parsing input data
    robot_list = []
    for rob in input_data.get("data", []):
        robot_list.append(RobotData(rob.get("robot_name", ""), rob.get(
            "pose", [0, 0, 0]), rob.get("footprint", [0, 0, 0, 0])))

    for rob in robot_list:
        plot_robot(rob)

    # Set plot title and labels
    plt.title('Footprint of Robots')
    plt.xlabel('X(m)')
    plt.ylabel('Y(m)')

    # Set aspect ratio to equal for better visualization
    plt.gca().set_aspect('equal', adjustable='box')

    # Show plot
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
