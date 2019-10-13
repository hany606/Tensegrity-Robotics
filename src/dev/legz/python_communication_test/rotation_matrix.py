# from scipy.spatial.transform import Rotation as R

import numpy as np
# import math

from transforms3d.euler import euler2mat



# r = R.from_euler("yxz",[yaw, pitch, roll])

# print(r.as_rotvec())

half_length = 5

orientation_vector = np.array([0,2,0])
end_point_local1 = np.array([0,half_length,0])
end_point_local2 = np.array([0,-half_length,0])


yaw,pitch,roll = orientation_vector

rot_mat = np.matrix(euler2mat(yaw, pitch, roll, 'syxz'))
print(rot_mat)

print("end_point1 in local coordinate system", end_point_local1)
print("end_point2 in local coordinate system", end_point_local2)


end_point_world1 = rot_mat.transpose().dot(end_point_local1)
end_point_world2 = rot_mat.transpose().dot(end_point_local2)


print("end_point1 in world coordinate system", end_point_world1)
print("end_point2 in world coordinate system", end_point_world2)


# or

CMS = np.array([1,2,3])

