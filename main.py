from env import NginxEnv

env = NginxEnv()

episodes = 1
for episode in range(1, episodes + 1):
    state = env.reset()
    done = False
    score = 0

    while not done:
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        print(f"Reward: {reward}")
        score += reward

    print(f"Episode: {episode} Score: {score}")
