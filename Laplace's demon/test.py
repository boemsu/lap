import numpy as np
import random

# world = np.random.randint(0, 4, (4, 10, 10))
# cloud  = random.randrange(20, 101)
# for point_z in range(4):
#     for j in range(cloud):
#         point_x = random.randrange(10)
#         point_y = random.randrange(10)
#         if world[point_z][point_y][point_x] == 0:
#             world[point_z][point_y][point_x] = 2
#         elif world[point_z][point_y][point_x] == 1:
#             world[point_z][point_y][point_x] = 3

# print(world)

# cloud_point_g =[(z,y,x) for x in range(10) for y in range(10) for z in range(4) if world[z][y][x] == 2]
# cloud_point_w =[(z,y,x) for x in range(10) for y in range(10) for z in range(4) if world[z][y][x] == 3]
# cloud_point = cloud_point_w + cloud_point_g


# print(cloud_point)

# dx=[0,1,-1]
# dy=[0,1,-1]
# for idx, point in enumerate(cloud_point):
#     cloud_point[idx] = (point[0], point[1] + random.choice(dy), point[2] + random.choice(dx))
# print(cloud_point)

# class t():
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#         self.world = np.random.randint(0, 2, (10, 10))
#         self.surface_point_ground =[(y, x) for x in range(width) for y in range(height) if self.world[y][x]==0]
#         self.surface_point_water =[(y, x) for x in range(width) for y in range(height) if self.world[y][x]==1]
#     def history_state(self):
#         self.surface_point_ground =[(y, x) for x in range(self.width) for y in range(self.height) if self.world[y][x]==0]
#         self.surface_point_water =[(y, x) for x in range(self.width) for y in range(self.height) if self.world[y][x]==1]

# world = t(10,10)
# print(world.surface_point_ground)
# world.world = np.random.randint(0, 2, (10, 10))
# world.history_state()
# print(world.surface_point_ground)
# print([(y, x) for x in range(10) for y in range(10) if world.world[y][x]==0])

import os, sys
sys.path.append(os.pardir)
from GridWorld import *
import cv2

world = World(100, 100)
print(world.world)
world.history_state()
# tem_world = world.move_surface(world.world.water_point)
# tem_world = world.move_cloud(world.cloud_point, tem_world)
# print(tem_world)
for i in range(6):
    print(world.move_surface(world.water_point))
    print('======================================')
world.history_state()
print(world.world)

for i in range(6):
    world.history_state()
    tem_surface = world.move_surface(world.water_point)
    tem_cloud = world.move_cloud(world.cloud_point, tem_surface)
    # world.play(tem_surface, tem_cloud)

world.history_state()
print(len(world.cloud_point))

print_world = np.zeros([6,100,100,3])

for i in world.surface_point_ground:
    print_world[i[0]][i[2]][i[1]] = [19, 69, 139] #갈색
for i in world.surface_point_water:
    print_world[i[0]][i[2]][i[1]] = [255, 51, 0] #파란색
for i in world.cloud_point_ground:
    print_world[i[0]][i[2]][i[1]] = [255, 255, 255] #흰 + 갈색
for i in  world.cloud_point_water:
    print_world[i[0]][i[2]][i[1]] = [255, 255, 204] #흰 + 파란색


print_world = np.array(print_world, dtype=np.uint8)
print_world = cv2.resize(print_world[0], dsize=(1000,1000), interpolation=cv2.INTER_LINEAR)

cv2.imshow("image", print_world)
cv2.waitKey()
cv2.destroyAllWindows()


dx=[0,1,-1]
dy=[0,1,-1]

for i in range(3):
    for j in range(3):
        dx[i]