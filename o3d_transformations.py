import copy
import math
import os
import numpy as np
import open3d as o3d


# Paths
rob_data_dir = "/home/aliena/Uni/Bachelor_Arbeit/robi_daten_05_12_23/Manuell/Geschlinge1"
rob_pos_path = f"{rob_data_dir}/rob_pos_Geschlinge_manual.xyz"
point_cloud_path = "/home/aliena/Uni/Bachelor_Arbeit/AlgoEval1/Geschlinge1_Result"


def calc_extrinsic_matrix(mesh, camera_pos: list[float]) -> np.ndarray:
    T = np.eye(4)
    T[:3, :3] = mesh.get_rotation_matrix_from_axis_angle(tuple(camera_pos[3:6]))
    T[0, 3], T[1, 3], T[2, 3] = camera_pos[0], camera_pos[1], camera_pos[2]
    return T


def str_to_matrix(matrix_as_str: str) -> np.ndarray:
    as_list = matrix_as_str.split()
    as_list = [float(i) for i in as_list]
    as_list = [as_list[i : i + 4] for i in range(0, 13, 4)]
    T = np.array(as_list)
    return T


def TM_robot_to_groundtruth(cam_i_to_gt: np.ndarray, cam_i_extrinsic: np.ndarray) -> np.ndarray:
    cam_to_robot = cam_i_extrinsic
    robot_to_cam = np.linalg.inv(cam_to_robot)
    return  np.dot(cam_i_to_gt, robot_to_cam)


if __name__ == '__main__':

    # initialize visualizer, render coordinate frame and z-axis vector
    viewer = o3d.visualization.Visualizer()
    viewer.create_window()
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 100, origin=(0, 0, 0))
    viewer.add_geometry(mesh)
    cam_view_vec = o3d.geometry.TriangleMesh.create_arrow(cylinder_radius=1, cone_radius=2, cylinder_height=50, cone_height=20)
    viewer.add_geometry(cam_view_vec)
    
    # setup groundtruth
    point_cloud_groundtruth = o3d.io.read_point_cloud('/home/aliena/Uni/Bachelor_Arbeit/groundtruth.ply')
    viewer.add_geometry(point_cloud_groundtruth)
    cam_i_to_gt = str_to_matrix("0.9522198936138601 -0.0985309635710311 -0.2441780077684151 180.92199083400476 0.15644975476338768 0.9486335467433581 0.22731200006078645 -136.45782403879437 0.2117896372617997 -0.2577579191117918 0.9299242481318638 319.02405726238095 0.0 0.0 0.0 1.0 ")

    with open(rob_pos_path, "r") as rob_pos_file:
        for i, cam in enumerate(rob_pos_file):
            # if i == 0: break
            # Calculate extrinisc matrix of camera position i
            cam_pose_i = [float(x) for x in cam.split()]
            extrinsic_matrix_i = calc_extrinsic_matrix(mesh, cam_pose_i)

            if i == 0:
                robot_to_groundtruth_matrix = TM_robot_to_groundtruth(cam_i_to_gt, extrinsic_matrix_i)
                print(robot_to_groundtruth_matrix)

            # Add Camera
            cam_i = copy.deepcopy(cam_view_vec)
            cam_i.transform(extrinsic_matrix_i)
            cam_i.transform(robot_to_groundtruth_matrix)
            viewer.add_geometry(cam_i)

            # Add pointclouds
            point_cloud_i = o3d.io.read_point_cloud(f'{point_cloud_path}/left_{i:02d}.ply')
            point_cloud_i.transform(extrinsic_matrix_i)
            point_cloud_i.transform(robot_to_groundtruth_matrix)
            # viewer.add_geometry(point_cloud_i.get_axis_aligned_bounding_box())
            viewer.add_geometry(point_cloud_i)

            # Render
            viewer.poll_events()
            viewer.update_renderer()

            # for testing purposes #########################################
            print(f"STM_cam_movement for cam_{i:02d}: ")
            stm_lst = map(str, (extrinsic_matrix_i.flatten().tolist()))
            print(" ".join(stm_lst), "\n")
            ################################################################

        viewer.run()
