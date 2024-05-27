import numpy as np
import random

#1: 땅
#2: 물
#3: 구름&땅
#4: 구름&물

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dim_page = [[[0,3,0],
                         [4,0,5],
                         [0,1,0]], 
                        [[0,0,0],
                         [4,1,5],
                         [0,2,0]],
                        [[0,1,0],
                         [4,2,5],
                         [0,3,0]],
                        [[0,2,0],
                         [4,3,5],
                         [0,0,0]],
                        [[0,0,0],
                         [3,4,1],
                         [0,2,0]],
                        [[0,0,0],
                         [1,5,3],
                         [0,2,0]]]
        # world = np.random.randint(1, 3, (6, height, width))
        world = np.ones((6, height, width))
        # [world[z][y][x] for z in range(6) for y in range(height) for x in range(width) if all(all(y>=30,y<=70), all(x>=30,x<=70))]
        # for i in range(6):
        # np.pad(world, ((30,30),(30,30),(0,0)), constant_values=0)
        for z in range(6):
            for y in range(height):
                for x in range(width):
                    if (y<=30 or y>=70) or (x<=30 or x>=70):
                        world[z][y][x] = 2
        cloud  = random.randrange(9000, 10001)
        for point_z in range(6):
            for i in range(cloud):
                point_x = random.randrange(width)
                point_y = random.randrange(height)
                if world[point_z][point_y][point_x] == 1:
                    world[point_z][point_y][point_x] = 3
                elif world[point_z][point_y][point_x] == 2:
                    world[point_z][point_y][point_x] = 4
        self.world = world

    def move_cloud(self, cloud_point, tem_surface):
        dx=[0,1,-1]
        dy=[0,1,-1]
        for idx, point in enumerate(cloud_point):

            # if tem_surface[cloud_point[idx][0]][cloud_point[idx][1]][cloud_point[idx][2]] == 3:
            #     tem_surface[cloud_point[idx][0]][cloud_point[idx][1]][cloud_point[idx][2]] = 1
            # elif tem_surface[cloud_point[idx][0]][cloud_point[idx][1]][cloud_point[idx][2]] == 4:
            #     tem_surface[cloud_point[idx][0]][cloud_point[idx][1]][cloud_point[idx][2]] = 2

            point = (point[0], point[1] + random.choice(dy), point[2] + random.choice(dx))

            if point[1] >= self.height:
                point = (self.dim_page[point[0]][2][1], point[1] - self.height, point[2])
            if point[1] <= -1:
                point = (self.dim_page[point[0]][0][1], point[1] + self.height, point[2])
            if point[2] >= self.width:
                point = (self.dim_page[point[0]][1][2], point[1], point[2] - self.width)
            if point[2] <= -1:
                point = (self.dim_page[point[0]][1][0], point[1], point[2] + self.width)

            cloud_point[idx] = (point[0], point[1], point[2])

            if random.random() <= 0.2:
                point = (point[0], point[1] + random.choice(dy), point[2] + random.choice(dx))

                if point[1] >= self.height:
                    point = (self.dim_page[point[0]][2][1], point[1] - self.height, point[2])
                if point[1] <= -1:
                    point = (self.dim_page[point[0]][0][1], point[1] + self.height, point[2])
                if point[2] >= self.width:
                    point = (self.dim_page[point[0]][1][2], point[1], point[2] - self.width)
                if point[2] <= -1:
                    point = (self.dim_page[point[0]][1][0], point[1], point[2] + self.width)

                cloud_point[idx] = (point[0], point[1], point[2])

            if tem_surface[cloud_point[idx][0]][cloud_point[idx][1]][cloud_point[idx][2]] == 1:
                tem_surface[cloud_point[idx][0]][cloud_point[idx][1]][cloud_point[idx][2]] = 3
            elif tem_surface[cloud_point[idx][0]][cloud_point[idx][1]][cloud_point[idx][2]] == 2:
                tem_surface[cloud_point[idx][0]][cloud_point[idx][1]][cloud_point[idx][2]] = 4

        self.world = tem_surface

        tem_cloud_point_ground =[(z, y, x) for x in range(self.width) for y in range(self.height) for z in range(6) if self.world[z][y][x]==3]
        tem_cloud_point_water =[(z, y, x) for x in range(self.width) for y in range(self.height) for z in range(6) if self.world[z][y][x]==4]
        tem_cloud = tem_cloud_point_ground + tem_cloud_point_water

        return tem_cloud
        
    def move_surface(self, water_point):
        dx=[0,1,-1]
        dy=[0,1,-1]

        tem_dx = []
        tem_dy = []

        tem_world = np.ones((6, self.height, self.width))

        for idx, point in enumerate(water_point):

            tem_world[water_point[idx][0]][water_point[idx][1]][water_point[idx][2]] = 2

            if random.random() <= 0.1:

                tem_dx = random.choice(dx)
                tem_dy = random.choice(dy)

                point = (point[0], point[1] + tem_dy, point[2] + tem_dx)

                if point[1] >= self.height:
                    point = (self.dim_page[point[0]][2][1], point[1] - self.height, point[2])
                if point[1] <= -1:
                    point = (self.dim_page[point[0]][0][1], point[1] + self.height, point[2])
                if point[2] >= self.width:
                    point = (self.dim_page[point[0]][1][2], point[1], point[2] - self.width)
                if point[2] <= -1:
                    point = (self.dim_page[point[0]][1][0], point[1], point[2] + self.width)

                water_point[idx] = (point[0], point[1], point[2])
                tem_world[water_point[idx][0]][water_point[idx][1]][water_point[idx][2]] = 2
                
        ground_point = [(z, y, x) for x in range(self.width) for y in range(self.height) for z in range(6) if tem_world[z][y][x]==1]

        for idx, point in enumerate(ground_point):

            tem_dx = random.choice(dx)
            tem_dy = random.choice(dy)

            tem_point = (point[0], point[1] + tem_dy, point[2] + tem_dx)

            if tem_point[1] >= self.height:
                tem_point = (self.dim_page[tem_point[0]][2][1], tem_point[1] - self.height, tem_point[2])
            if tem_point[1] <= -1:
                tem_point = (self.dim_page[tem_point[0]][0][1], tem_point[1] + self.height, tem_point[2])
            if tem_point[2] >= self.width:
                tem_point = (self.dim_page[tem_point[0]][1][2], tem_point[1], tem_point[2] - self.width)
            if tem_point[2] <= -1:
                tem_point = (self.dim_page[tem_point[0]][1][0], tem_point[1], tem_point[2] + self.width)

            ground_point[idx] = (point[0], point[1], point[2])
            tem_ground_point = (tem_point[0], tem_point[1], tem_point[2])
            
            if tem_world[tem_ground_point[0]][tem_ground_point[1]][tem_ground_point[2]] == 2:
                if random.random() <= 0.05:
                    if random.random() <= 0.01:
                        tem_world[ground_point[idx][0]][ground_point[idx][1]][ground_point[idx][2]] = 1
                    else:
                        tem_world[ground_point[idx][0]][ground_point[idx][1]][ground_point[idx][2]] = 2
                tem_world[tem_ground_point[0]][tem_ground_point[1]][tem_ground_point[2]] = 1

        return tem_world

    def history_state(self):
        self.surface_point_ground =[(z, y, x) for x in range(self.width) for y in range(self.height) for z in range(6) if self.world[z][y][x]==1]
        self.surface_point_water =[(z, y, x) for x in range(self.width) for y in range(self.height) for z in range(6) if self.world[z][y][x]==2]
        self.cloud_point_ground =[(z, y, x) for x in range(self.width) for y in range(self.height) for z in range(6) if self.world[z][y][x]==3]
        self.cloud_point_water =[(z, y, x) for x in range(self.width) for y in range(self.height) for z in range(6) if self.world[z][y][x]==4]
        self.water_point = self.surface_point_water + self.cloud_point_water
        self.ground_point =  self.surface_point_ground + self.cloud_point_ground
        self.cloud_point = self.cloud_point_ground + self.cloud_point_water

    def step(self, action):
        score = 0
        action_move_map = [(0,0),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),
                           (2,0),(2,1),(2,2),(1,2),(0,2),(-1,2),(-2,2),(-2,1),(-2,0),
                           (-2,-1),(-2,-2),(-1,-2),(0,-2),(1,-2),(2,-2),(2,-1)]
        move = action_move_map[action]
        for idx, point in enumerate(self.cloud_point):
            self.cloud_point[idx] = (point[0], point[1] + move[0], point[2] + move[1])

            if self.cloud_point[idx][1] >= self.height:
                self.cloud_point[idx] = (self.dim_page[self.cloud_point[idx][0]][2][1], self.cloud_point[idx][1] - self.height, self.cloud_point[idx][2])
            if self.cloud_point[idx][1] <= -1:
                self.cloud_point[idx] = (self.dim_page[self.cloud_point[idx][0]][0][1], self.cloud_point[idx][1] + self.height, self.cloud_point[idx][2])
            if self.cloud_point[idx][2] >= self.width:
                self.cloud_point[idx] = (self.dim_page[self.cloud_point[idx][0]][1][2], self.cloud_point[idx][1], self.cloud_point[idx][2] - self.width)
            if self.cloud_point[idx][2] <= -1:
                self.cloud_point[idx] = (self.dim_page[self.cloud_point[idx][0]][1][0], self.cloud_point[idx][1], self.cloud_point[idx][2] + self.width)

            if self.world[self.cloud_point[idx]] == 3 or 4:
                score += 1

        return score

    
            
            



        
        
        
        
            



        




