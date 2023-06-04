import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

#inicjalizacja środowiska:
env = gym.make('FrozenLake-v1', desc=None, map_name="8x8", is_slippery=False)
state_size = env.observation_space.n
action_size = env.action_space.n

#paramtetry czasowe:
num_of_ind_runs = 25
num_episodes = 1000
episode_max_time=200

#stan absorbujący:
SUCCESS_POSITION=63

#współczynniki:
beta=0.7
gamma=0.9
epsilon=0.1

env.reset()
env.render()


def base():
    averaged_reward = np.zeros( num_episodes)
    num_of_succeses=0

    for run in range(num_of_ind_runs):
        qtable = np.zeros((state_size, action_size))
        for episode in range(num_episodes):
            state, info = env.reset()
            cur_episode_time = 0
            end=False

            while not end:
                value=np.random.rand(1)[0]
                if (value < epsilon):
                    action = env.action_space.sample()
                else:
                    max_actions = np.flatnonzero(qtable[state] == np.max(qtable[state]))
                    action = np.random.choice(max_actions)

                observation, reward, end, truncated, info = env.step(action) #end=termination (if termination is True then end is True)

                if(observation==SUCCESS_POSITION):
                    num_of_succeses+=1
                
                delta=reward + gamma * np.max(qtable[observation]) - qtable[state, action]
                qtable[state, action] = qtable[state, action] + beta * delta

                state=observation

                #warunek czasowy:
                cur_episode_time+=1
                if(cur_episode_time>=episode_max_time):
                    end=True

            averaged_reward[episode] = averaged_reward[episode] + reward

        
    averaged_reward = averaged_reward/num_of_ind_runs
    print(num_of_succeses/num_of_ind_runs)
    return averaged_reward


def experiment():
    averaged_reward = np.zeros( num_episodes)
    num_of_succeses=0

    for run in range(num_of_ind_runs):
        qtable = np.zeros((state_size, action_size))
        for episode in range(num_episodes):
            state, info = env.reset()
            cur_episode_time = 0
            end=False

            while not end:
                value=np.random.rand(1)[0]
                if (value < epsilon):
                    action = env.action_space.sample()
                else:
                    max_actions = np.flatnonzero(qtable[state] == np.max(qtable[state]))
                    action = np.random.choice(max_actions)

                observation, reward, end, truncated, info = env.step(action) #end=termination (if termination is True then end is True)

                if(observation==SUCCESS_POSITION):
                    num_of_succeses+=1
                
                delta=reward + gamma * np.max(qtable[observation]) - qtable[state, action]
                qtable[state, action] = qtable[state, action] + beta * delta

                if(state==observation and end!=True):
                    reward=-0.25

                state=observation

                #warunek czasowy:
                cur_episode_time+=1
                if(cur_episode_time>=episode_max_time):
                    end=True

            averaged_reward[episode] = averaged_reward[episode] + reward

        
    averaged_reward = averaged_reward/num_of_ind_runs
    print(num_of_succeses/num_of_ind_runs)
    return averaged_reward


averaged_reward_base = base() #niech to będą wyniki bazowe, z którymi będziemy porównywać wyniki dla innych ustawień, czy funkcji oceny
averaged_reward=experiment()

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
plt.plot(averaged_reward_base, 'r')
plt.plot(averaged_reward, 'b')
plt.show()