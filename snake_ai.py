import numpy as np
import tensorflow as tf
from tensorflow import keras
from collections import deque
import random
import pygame
import time
from snake import Snake
from fruit import Fruit
from constants import *
from utils import generate_fruit
import matplotlib.pyplot as plt
import os

class SnakeGameEnv:
    """Environment wrapper for the Snake game to be used with RL algorithms"""
    
    def __init__(self, render=False):
        self.render = render
        if render:
            pygame.init()
            self.window = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption('Snake AI Training')
            pygame.font.init()
            self.font = pygame.font.Font(None, FONT_SIZE)
            self.clock = pygame.time.Clock()

    def reset(self):
        """Reset the environment for a new episode"""
        self.snake = Snake([[300, 150], [290, 150], [280, 150]])
        self.fruit = generate_fruit(self.snake.body)
        self.score = 0
        self.steps = 0
        self.max_steps = 100 * len(self.snake.body)  # Limit steps to avoid infinite loops
        self.done = False
        return self._get_state()

    def step(self, action):
        """Take a step in the environment with the given action
        
        Actions: 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
        """
        # Convert action number to direction
        direction_map = {0: 'UP', 1: 'RIGHT', 2: 'DOWN', 3: 'LEFT'}
        direction = direction_map[action]
        
        # Get the current head position
        prev_head = self.snake.body[0].copy()
        
        # Move the snake
        self.snake.move(direction)
        self.steps += 1
        
        # Small penalty for each step
        reward = -0.01
        if self.snake.check_game_over():
            reward = -10  # Negative reward for dying
            self.done = True
        elif self.steps >= self.max_steps:
            reward = -5  # Negative reward for taking too many steps
            self.done = True
        else:
            # Calculate reward based on getting closer or further from fruit
            new_head = self.snake.body[0]
            new_dist = self._manhattan_distance(new_head, self.fruit.position)
            old_dist = self._manhattan_distance(prev_head, self.fruit.position)
            
            # Small reward for getting closer to fruit
            if new_dist < old_dist:
                reward = 0.1
            
            # Check if snake ate the fruit
            if self.snake.check_collision(self.fruit):
                if self.fruit.type == 'NORMAL':  # Reward only for red fruit
                    reward = 5  # Increase reward for eating red fruit
                    self.score += 1
                    self.max_steps += 100  # Extend steps limit when red fruit is eaten
                else:  # No reward for blue or gold fruit
                    reward = 0

                # Generate a new fruit regardless of type
                self.fruit = generate_fruit(self.snake.body)
            else:
                # If not eating fruit, remove the last segment
                self.snake.remove_last_segment()
        
        # Render if needed
        if self.render and hasattr(self, 'window'):
            self._render_frame()
        
        return self._get_state(), reward, self.done, {"score": self.score}

    def _get_state(self):
        """Convert the game state to a vector representation for the AI"""
        head = self.snake.body[0]
        snake_direction = self._get_direction()
        
        # Danger points (positions that would cause immediate death)
        danger_straight = self._is_danger(head, snake_direction)
        danger_right = self._is_danger(head, self._turn_right(snake_direction))
        danger_left = self._is_danger(head, self._turn_left(snake_direction))
        
        # Direction vector (one-hot encoded)
        dir_up = 1 if snake_direction == 'UP' else 0
        dir_right = 1 if snake_direction == 'RIGHT' else 0
        dir_down = 1 if snake_direction == 'DOWN' else 0
        dir_left = 1 if snake_direction == 'LEFT' else 0
        
        # Fruit location relative to head
        fruit_up = 1 if self.fruit.position[1] < head[1] else 0
        fruit_right = 1 if self.fruit.position[0] > head[0] else 0
        fruit_down = 1 if self.fruit.position[1] > head[1] else 0
        fruit_left = 1 if self.fruit.position[0] < head[0] else 0
        
        # Normalize distances
        dist_x = (self.fruit.position[0] - head[0]) / WIDTH
        dist_y = (self.fruit.position[1] - head[1]) / HEIGHT
        
        return np.array([
            danger_straight, danger_right, danger_left,
            dir_up, dir_right, dir_down, dir_left,
            fruit_up, fruit_right, fruit_down, fruit_left,
            dist_x, dist_y
        ])
    
    def _get_direction(self):
        """Get the current direction of the snake based on the first two body segments"""
        if len(self.snake.body) < 2:
            return 'RIGHT'  # Default direction
        
        head = self.snake.body[0]
        neck = self.snake.body[1]
        
        if head[0] > neck[0]:
            return 'RIGHT'
        elif head[0] < neck[0]:
            return 'LEFT'
        elif head[1] < neck[1]:
            return 'UP'
        else:
            return 'DOWN'
    
    def _turn_right(self, direction):
        """Return the direction after turning right"""
        turns = {'UP': 'RIGHT', 'RIGHT': 'DOWN', 'DOWN': 'LEFT', 'LEFT': 'UP'}
        return turns[direction]
    
    def _turn_left(self, direction):
        """Return the direction after turning left"""
        turns = {'UP': 'LEFT', 'LEFT': 'DOWN', 'DOWN': 'RIGHT', 'RIGHT': 'UP'}
        return turns[direction]
    
    def _is_danger(self, head, direction):
        """Check if there's danger in the specified direction"""
        next_pos = head.copy()
        
        if direction == 'UP':
            next_pos[1] -= SNAKE_SIZE
        elif direction == 'RIGHT':
            next_pos[0] += SNAKE_SIZE
        elif direction == 'DOWN':
            next_pos[1] += SNAKE_SIZE
        elif direction == 'LEFT':
            next_pos[0] -= SNAKE_SIZE
        
        # Check wall collision
        if (next_pos[0] < 0 or next_pos[0] >= WIDTH or 
            next_pos[1] < 0 or next_pos[1] >= HEIGHT):
            return 1
        
        # Check self collision
        for segment in self.snake.body[1:]:
            if next_pos[0] == segment[0] and next_pos[1] == segment[1]:
                return 1
        
        return 0
    
    def _manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two points"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def _render_frame(self):
        """Render the current state of the game"""
        # Handle events to keep the window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        self.window.fill(GRAY)
        
        # Draw snake
        for segment in self.snake.body:
            pygame.draw.rect(self.window, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        
        # Draw fruit
        color = RED
        if self.fruit.type == 'SPECIAL':
            color = BLUE
        elif self.fruit.type == 'GOLDEN':
            color = GOLD
        pygame.draw.rect(self.window, color, pygame.Rect(self.fruit.position[0], self.fruit.position[1], SNAKE_SIZE, SNAKE_SIZE))
        
        # Display score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.window.blit(score_text, (10, 10))
        
        pygame.display.update()
        self.clock.tick(30)  # Limit to 30 FPS for visualization

class DQNAgent:
    """Deep Q-Network agent for playing Snake"""
    
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999  # Epsilon decay rate
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
    
    def _build_model(self):
        """Build a neural network model for Q-learning"""
        model = keras.Sequential()
        model.add(keras.layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(keras.layers.Dense(24, activation='relu'))
        model.add(keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model
    
    def update_target_model(self):
        """Copy weights from model to target_model"""
        self.target_model.set_weights(self.model.get_weights())
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in memory"""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state, training=True):
        """Choose an action based on epsilon-greedy policy"""
        if training and np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        
        act_values = self.model.predict(np.array([state]), verbose=0)
        return np.argmax(act_values[0])
    
    def replay(self, batch_size):
        """Train on random batch from memory"""
        if len(self.memory) < batch_size:
            return
        
        minibatch = random.sample(self.memory, batch_size)
        
        states = np.array([experience[0] for experience in minibatch])
        actions = np.array([experience[1] for experience in minibatch])
        rewards = np.array([experience[2] for experience in minibatch])
        next_states = np.array([experience[3] for experience in minibatch])
        dones = np.array([experience[4] for experience in minibatch])
        
        # Calculate target Q values
        targets = self.model.predict(states, verbose=0)
        next_q_values = self.target_model.predict(next_states, verbose=0)
        
        for i in range(batch_size):
            if dones[i]:
                targets[i, actions[i]] = rewards[i]
            else:
                targets[i, actions[i]] = rewards[i] + self.gamma * np.amax(next_q_values[i])
        
        # Train the model
        self.model.fit(states, targets, epochs=1, verbose=0)
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def train_snake_ai(episodes=10000, batch_size=64, render_every=100):
    """Train the Snake AI agent"""
    env = SnakeGameEnv(render=False)
    state_size = 13  # Size of our state representation
    action_size = 4  # UP, RIGHT, DOWN, LEFT
    agent = DQNAgent(state_size, action_size)
    
    scores = []
    total_rewards = []  # Initialize total_rewards to track rewards per episode
    update_target_every = 5
    
    for e in range(episodes):
        # Reset environment for a new episode
        state = env.reset()
        total_reward = 0  # Initialize total_reward for the current episode
        render_this_episode = (e % render_every == 0)
        
        if render_this_episode:
            env.render = True
        
        while True:
            # Agent chooses action
            action = agent.act(state)
            
            # Environment takes a step
            next_state, reward, done, info = env.step(action)
            total_reward += reward
            
            # Store in memory and learn
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            
            if done:
                # Update stats
                scores.append(info["score"])
                total_rewards.append(total_reward)  # Append total reward
                print(f"Episode: {e+1}/{episodes}, Score: {info['score']}, Reward: {total_reward:.2f}, Epsilon: {agent.epsilon:.2f}")
                break
        
        # Turn off rendering for next episode
        env.render = False
        
        # Train the model
        agent.replay(batch_size)
        
        # Update target network
        if e % update_target_every == 0:
            agent.update_target_model()
            print(f"Updated target model at episode {e+1}")
    
        # Save model checkpoints
        if e % 1000 == 0:
            agent.model.save(f'snake_ai_model_grinder_checkpoint_{e}.keras')  # Save in .keras format
            print(f"Checkpoint saved at episode {e}")
    
    # Save the trained model
    agent.model.save('snake_ai_model_grinder.keras')  # Save in .keras format
    
    # Plot learning curve
    plt.figure(figsize=(10, 6))
    plt.plot(scores, label='Score')
    plt.plot(total_rewards, label='Total Reward')  # Add total rewards
    plt.title('Snake AI Learning Curve')
    plt.xlabel('Episode')
    plt.ylabel('Score / Reward')
    plt.legend()
    plt.savefig('learning_curve.png')
    plt.show()
    
    return agent

def watch_ai_play(model_path='snake_ai_model_grinder.keras', games=5):  # Updated default model path
    """Watch the trained AI play Snake"""
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found. Please train the AI first by running the script.")
        return

    model = keras.models.load_model(model_path)  # Load the model in .keras format
    env = SnakeGameEnv(render=True)
    state_size = 13

    for game in range(games):
        state = env.reset()
        done = False

        while not done:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # AI chooses action
            q_values = model.predict(np.array([state]), verbose=0)
            action = np.argmax(q_values[0])

            # Take action
            state, _, done, info = env.step(action)

            # Slow down visualization
            time.sleep(0.1)

        print(f"Game {game+1}: Score = {info['score']}")
        time.sleep(1)  # Pause between games

if __name__ == "__main__":
    # Train the AI
    print("Starting training...")
    agent = train_snake_ai(episodes=10000, batch_size=64, render_every=100)  # Update episodes to 10,000
    
    # Watch the trained AI play
    print("\nWatching trained AI play...")
    watch_ai_play()
