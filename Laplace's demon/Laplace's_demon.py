import os, sys
sys.path.append(os.pardir)
from GridWorld import *
import torch
import torch.nn as nn
from collections import defaultdict
from utils import greedy_probs
import cv2
import gridworld_render as render_helper


class Agent():
    def __init__(self): 
        self.gamma = 0.9
        self.action_size = 25

        #0:1/9*0.8+1*0.2*1/9 = 1/9  1,3,5,7:1/9*0.8+6/9*0.2*1/9 = 14/135  2,4,6,8:1/9*0.8+4/9*0.2*1/9 = 40/405
        #9:3/9*0.2*1/9 = 1/135  #10:2/9*0.2*1/9 = 2/405  #11:1/9*0.2*1/9 = 1/405
        actions = {0:1/9, 1:14/135, 2:8/81, 
                  3:14/135, 4:8/81, 5:14/135,
                  6:8/81, 7:14/135, 8:8/81,
                  9:1/135, 10:2/405, 11:1/405, 12:2/405,
                  13:1/135, 14:2/405, 15:1/405, 16:2/405,
                  17:1/135, 18:2/405, 19:1/405, 20:2/405,
                  21:1/135, 22:2/405, 23:1/405, 24:2/405}
        self.pi = defaultdict(lambda: actions)
        self.V = defaultdict(lambda: 0)
        self.cnts = defaultdict(lambda: 0)
        self.memory = []

    def get_action(self, state):
        action_probs = self.pi[state]
        actions = list(action_probs.keys())
        probs = list(action_probs.values())
        return np.random.choice(actions, p=probs)
 
    def add(self, state, action, reward):
        data = (state, action, reward)
        self.memory.append(data)

    def reset(self):
        self.memory.clear()

    def update(self):
        G = 0
        for data in reversed(self.memory):
            state, action, reward = data
            G = self.gamma * G + reward
            key = (state, action)
            self.cnts[key] += 1
            self.Q[key] += (G - self.Q[key]) / self.cnts[key]
            self.Q[key] += (G - self.Q[key]) * self.alpha
            self.pi[state] = greedy_probs(self.Q, state, self.epsilon)

    def eval(self):
        G = 0
        for data in reversed(self.memory):  # 역방향으로(reserved) 따라가기
            state, action, reward = data
            G = self.gamma * G + reward
            self.cnts[state] += 1
            self.V[state] += (G - self.V[state]) / self.cnts[state]

    def render_v(self, v=None, policy=None, print_value=True):
        renderer = render_helper.Renderer(world.world, self.goal_state,
                                          self.wall_state)
        renderer.render_v(v, policy, print_value)

    def render_q(self, q=None, print_value=True):
        renderer = render_helper.Renderer(self.reward_map, self.goal_state,
                                          self.wall_state)
        renderer.render_q(q, print_value)

world = World(100, 100)
agent = Agent()

history = []
history_cloud = []

for i in range(10):
    world.history_state()
    history_cloud.append(world.cloud_point)
    history.append(world.world)
    tem_surface = world.move_surface(world.water_point)
    world.move_cloud(world.cloud_point, tem_surface)

episodes = 10
for episode in range(episodes):  # 에피소드 1000번 수행
    for idx, point in enumerate(history_cloud[episode]):
            state = point
            agent.reset()

            action = agent.get_action(state)             # 행동 선택
            reward = world.step(action)  # 행동 수행

            agent.add(state, action, reward)  # (상태, 행동, 보상) 저장
    agent.eval()  # 몬테카를로법으로 가치 함수 갱신
    print(episode)
    print(agent.V)

# # [그림 5-12] 몬테카를로법으로 얻은 가치 함수
# Agent.render_v(agent.V)
# print(agent.memory)

world.history_state()

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
# cv2.imwrite("world2.jpg", print_world)
cv2.waitKey()
cv2.destroyAllWindows()

