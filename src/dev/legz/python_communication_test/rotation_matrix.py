# from scipy.spatial.transform import Rotation as R

import numpy as np
# import math

from transforms3d.euler import euler2mat



# r = R.from_euler("yxz",[yaw, pitch, roll])
# (Coordinates_in_rod_sys - CMS)*inv(Rotation_matrix) = Coordinates_in_global_sys

# print(r.as_rotvec())

half_length = 5

orientation_vector = np.array([-0.0003372974803296021, -0.0009397567447154057, -3.1373493946770354])
# orientation_vector = np.array([0,np.pi/2,0])
CMS = np.array([-0.003782952911371401, 1.9664315117124704, -3.746689267649598])
# CMS = np.array([-5,0,0])
end_point_local1 = np.array([0,0,half_length])
end_point_local2 = np.array([0,0,-half_length])


yaw,pitch,roll = orientation_vector

rot_mat = np.matrix(euler2mat(yaw, pitch, roll, 'syxz'))
print(rot_mat)

print("end_point1 in local coordinate system", end_point_local1)
print("end_point2 in local coordinate system", end_point_local2)


end_point_world1 = rot_mat.dot(end_point_local1) + CMS
end_point_world2 = rot_mat.dot(end_point_local2) + CMS


print("end_point1 in world coordinate system", end_point_world1)
print("end_point2 in world coordinate system", end_point_world2)

print("CMS back", (end_point_world1+end_point_world2)/2)


# or

CMS = np.array([1,2,3])

