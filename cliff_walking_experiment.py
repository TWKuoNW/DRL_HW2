"""
HW2：Q-learning 與 SARSA 演算法之比較研究
Cliff Walking 強化學習實驗

環境描述：
- 網格大小：4 列 × 12 行（共 48 個狀態）
- 起點（Start）：左下角座標 (3, 0)
- 終點（Goal）：右下角座標 (3, 11)
- 懸崖（Cliff）：底部列中間區域 (3,1) 至 (3,10)，共 10 格

獎勵機制：
- 一般移動：-1
- 掉入懸崖：-100（回到起點）
- 抵達終點：-1（回合結束）

實驗參數：
- 探索率 ε (epsilon) = 0.1
- 學習率 α (alpha) = 0.5
- 折扣因子 γ (gamma) = 0.9
- 訓練回合數 Episodes = 500
- 重複執行次數 Runs = 50（取平均）
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ============================================================
# 環境設定
# ============================================================
ROWS = 4
COLS = 12
START = (3, 0)
GOAL = (3, 11)
CLIFF = [(3, c) for c in range(1, 11)]  # (3,1) ~ (3,10)

# 動作定義：0=上, 1=下, 2=左, 3=右
ACTIONS = [0, 1, 2, 3]
ACTION_NAMES = ['↑', '↓', '←', '→']
ACTION_DELTAS = {
    0: (-1, 0),  # 上
    1: (1, 0),   # 下
    2: (0, -1),  # 左
    3: (0, 1),   # 右
}


def step(state, action):
    """
    執行一步動作，返回 (next_state, reward, done)。
    """
    row, col = state
    dr, dc = ACTION_DELTAS[action]
    new_row = max(0, min(ROWS - 1, row + dr))
    new_col = max(0, min(COLS - 1, col + dc))
    next_state = (new_row, new_col)

    # 掉入懸崖
    if next_state in CLIFF:
        return START, -100, False

    # 抵達終點
    if next_state == GOAL:
        return GOAL, -1, True

    # 一般移動
    return next_state, -1, False


def epsilon_greedy(Q, state, epsilon):
    """
    ε-greedy 策略：以 ε 機率隨機探索，否則選擇最大 Q 值的動作。
    """
    if np.random.random() < epsilon:
        return np.random.choice(ACTIONS)
    else:
        return np.argmax(Q[state])


# ============================================================
# 3.1 Q-learning（離策略方法）
# ============================================================
# Q-learning (Off-policy TD control)
def q_learning(episodes=500, alpha=0.5, gamma=0.9, epsilon=0.1):
    Q = np.zeros((ROWS, COLS, 4))  # Initialize Q-table
    rewards_per_episode = []
    for ep in range(episodes):
        state = START
        total_reward = 0
        while True:
            # Choose action using epsilon-greedy
            action = epsilon_greedy(Q, state, epsilon)
            next_state, reward, done = step(state, action)
            total_reward += reward
            # Off-policy update: use max Q of next state
            best_next_q = np.max(Q[next_state])
            Q[state][action] += alpha * (
                reward + gamma * best_next_q - Q[state][action]
            )
            state = next_state
            if done:
                break
        rewards_per_episode.append(total_reward)
    return Q, rewards_per_episode


# ============================================================
# 3.2 SARSA（同策略方法）
# ============================================================
# SARSA (On-policy TD control)
def sarsa(episodes=500, alpha=0.5, gamma=0.9, epsilon=0.1):
    Q = np.zeros((ROWS, COLS, 4))  # Initialize Q-table
    rewards_per_episode = []
    for ep in range(episodes):
        state = START
        action = epsilon_greedy(Q, state, epsilon)  # Choose first action
        total_reward = 0
        while True:
            next_state, reward, done = step(state, action)
            total_reward += reward
            # On-policy update: use actual next action taken
            next_action = epsilon_greedy(Q, next_state, epsilon)
            Q[state][action] += alpha * (
                reward + gamma * Q[next_state][next_action] - Q[state][action]
            )
            state, action = next_state, next_action
            if done:
                break
        rewards_per_episode.append(total_reward)
    return Q, rewards_per_episode


# ============================================================
# 實驗執行：多次運行取平均
# ============================================================
def run_experiments(num_runs=50, episodes=500, alpha=0.5, gamma=0.9, epsilon=0.1):
    """
    執行多次實驗，取平均學習曲線。
    """
    q_all_rewards = np.zeros((num_runs, episodes))
    s_all_rewards = np.zeros((num_runs, episodes))

    q_final_Q = None
    s_final_Q = None

    for run in range(num_runs):
        print(f"\r執行第 {run + 1}/{num_runs} 次...", end="")
        Q_q, rewards_q = q_learning(episodes, alpha, gamma, epsilon)
        Q_s, rewards_s = sarsa(episodes, alpha, gamma, epsilon)
        q_all_rewards[run] = rewards_q
        s_all_rewards[run] = rewards_s
        q_final_Q = Q_q  # 保留最後一次的 Q-table 用於策略視覺化
        s_final_Q = Q_s

    print("\n實驗完成！")
    return q_all_rewards, s_all_rewards, q_final_Q, s_final_Q


# ============================================================
# 4.1 學習曲線（累積獎勵）
# ============================================================
def plot_learning_curves(q_all_rewards, s_all_rewards):
    """
    繪製 Q-learning 與 SARSA 的學習曲線。
    圖 4.1：Q-learning 與 SARSA 在 Cliff Walking 上的學習曲線
    （50 次執行平均，ε=0.1, α=0.5, γ=0.9）
    """
    q_mean = np.mean(q_all_rewards, axis=0)
    s_mean = np.mean(s_all_rewards, axis=0)
    q_std = np.std(q_all_rewards, axis=0)
    s_std = np.std(s_all_rewards, axis=0)

    episodes = np.arange(1, len(q_mean) + 1)

    plt.figure(figsize=(12, 6))
    plt.plot(episodes, q_mean, label='Q-learning', color='#e74c3c', alpha=0.9)
    plt.fill_between(episodes, q_mean - q_std, q_mean + q_std, color='#e74c3c', alpha=0.15)
    plt.plot(episodes, s_mean, label='SARSA', color='#3498db', alpha=0.9)
    plt.fill_between(episodes, s_mean - s_std, s_mean + s_std, color='#3498db', alpha=0.15)

    plt.xlabel('Episode', fontsize=12)
    plt.ylabel('Sum of Rewards During Episode', fontsize=12)
    plt.title('Fig 4.1: Q-learning vs SARSA Learning Curves\n(Averaged over 50 runs, epsilon=0.1, alpha=0.5, gamma=0.9)',
              fontsize=13)
    plt.legend(fontsize=12, loc='lower right')
    plt.ylim(-200, 0)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('fig4_1_learning_curves.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("已儲存：fig4_1_learning_curves.png")


# ============================================================
# 4.2 策略視覺化
# ============================================================
def plot_policy(Q, title, ax):
    """
    在指定的 axes 上繪製策略（箭頭方向代表貪婪動作）。
    """
    # 箭頭方向對應
    arrow_dx = {0: 0, 1: 0, 2: -0.3, 3: 0.3}
    arrow_dy = {0: 0.3, 1: -0.3, 2: 0, 3: 0}

    # 繪製網格
    for r in range(ROWS):
        for c in range(COLS):
            # 背景顏色
            if (r, c) == START:
                ax.add_patch(plt.Rectangle((c - 0.5, ROWS - 1 - r - 0.5), 1, 1,
                                           color='#2ecc71', alpha=0.5))
                ax.text(c, ROWS - 1 - r, 'S', ha='center', va='center',
                        fontsize=10, fontweight='bold', color='#27ae60')
            elif (r, c) == GOAL:
                ax.add_patch(plt.Rectangle((c - 0.5, ROWS - 1 - r - 0.5), 1, 1,
                                           color='#f1c40f', alpha=0.5))
                ax.text(c, ROWS - 1 - r, 'G', ha='center', va='center',
                        fontsize=10, fontweight='bold', color='#f39c12')
            elif (r, c) in CLIFF:
                ax.add_patch(plt.Rectangle((c - 0.5, ROWS - 1 - r - 0.5), 1, 1,
                                           color='#e74c3c', alpha=0.5))
                ax.text(c, ROWS - 1 - r, 'X', ha='center', va='center',
                        fontsize=10, fontweight='bold', color='#c0392b')
            else:
                # 繪製策略箭頭
                best_action = np.argmax(Q[r, c])
                dx = arrow_dx[best_action]
                dy = arrow_dy[best_action]
                ax.annotate('', xy=(c + dx, ROWS - 1 - r + dy),
                            xytext=(c, ROWS - 1 - r),
                            arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=1.5))

    ax.set_xlim(-0.5, COLS - 0.5)
    ax.set_ylim(-0.5, ROWS - 0.5)
    ax.set_xticks(range(COLS))
    ax.set_yticks(range(ROWS))
    ax.set_yticklabels(reversed(range(ROWS)))
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(title, fontsize=12, fontweight='bold')


def plot_policies(q_Q, s_Q):
    """
    繪製 Q-learning 與 SARSA 的最終策略。
    圖 4.2：Q-learning（左）與 SARSA（右）學習到的最終策略
    """
    fig, axes = plt.subplots(1, 2, figsize=(20, 5))
    plot_policy(q_Q, 'Q-learning Policy', axes[0])
    plot_policy(s_Q, 'SARSA Policy', axes[1])
    fig.suptitle('Fig 4.2: Learned Policies of Q-learning (Left) and SARSA (Right)\n'
                 '(Arrow direction represents greedy action)', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('fig4_2_policies.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("已儲存：fig4_2_policies.png")


# ============================================================
# 4.3 收斂速度比較 & 4.4 穩定性分析
# ============================================================
def print_statistics(q_all_rewards, s_all_rewards):
    """
    輸出收斂速度與穩定性的統計數據。
    """
    q_mean = np.mean(q_all_rewards, axis=0)
    s_mean = np.mean(s_all_rewards, axis=0)

    # 初始收斂回合（平均獎勵 ≥ -60）
    q_converge = np.argmax(q_mean >= -60) + 1 if np.any(q_mean >= -60) else "未收斂"
    s_converge = np.argmax(s_mean >= -60) + 1 if np.any(s_mean >= -60) else "未收斂"

    # 後期統計（最後 100 回合）
    q_last100 = q_all_rewards[:, -100:]
    s_last100 = s_all_rewards[:, -100:]
    q_last100_mean = np.mean(q_last100)
    s_last100_mean = np.mean(s_last100)
    q_last100_std = np.std(np.mean(q_last100, axis=0))
    s_last100_std = np.std(np.mean(s_last100, axis=0))

    print("=" * 60)
    print("4.3 收斂速度比較")
    print("=" * 60)
    print(f"{'指標':<25} {'Q-learning':<15} {'SARSA':<15}")
    print("-" * 60)
    print(f"{'初始收斂回合（≥ -60）':<20} ≈ 第 {q_converge} 回合     ≈ 第 {s_converge} 回合")
    print(f"{'後期均值（最後100回合）':<20} {q_last100_mean:<15.2f} {s_last100_mean:<15.2f}")
    print(f"{'後期標準差':<22} {q_last100_std:<15.2f} {s_last100_std:<15.2f}")
    print()
    print("=" * 60)
    print("4.4 穩定性分析")
    print("=" * 60)
    print(f"Q-learning 後期標準差: {q_last100_std:.2f}")
    print(f"SARSA 後期標準差: {s_last100_std:.2f}")
    if q_last100_std > s_last100_std:
        print("→ Q-learning 的波動幅度較大，訓練過程較不穩定。")
        print("→ SARSA 的穩定性更佳，策略與執行一致，減少意外懲罰。")
    else:
        print("→ SARSA 的波動幅度較大。")
    print()


# ============================================================
# 主程式
# ============================================================
if __name__ == '__main__':
    # 設定隨機種子以確保可重現
    np.random.seed(42)

    # 實驗參數
    NUM_RUNS = 50
    EPISODES = 500
    ALPHA = 0.5
    GAMMA = 0.9
    EPSILON = 0.1

    print("=" * 60)
    print("HW2：Q-learning 與 SARSA 演算法之比較研究")
    print("Cliff Walking 強化學習實驗")
    print("=" * 60)
    print(f"實驗參數：ε={EPSILON}, α={ALPHA}, γ={GAMMA}")
    print(f"訓練回合數：{EPISODES}, 重複執行次數：{NUM_RUNS}")
    print()

    # 執行實驗
    q_all_rewards, s_all_rewards, q_Q, s_Q = run_experiments(
        num_runs=NUM_RUNS, episodes=EPISODES,
        alpha=ALPHA, gamma=GAMMA, epsilon=EPSILON
    )

    # 輸出統計數據
    print_statistics(q_all_rewards, s_all_rewards)

    # 繪製學習曲線
    plot_learning_curves(q_all_rewards, s_all_rewards)

    # 繪製策略
    plot_policies(q_Q, s_Q)

    print("=" * 60)
    print("所有實驗已完成！")
    print("已產生以下圖片：")
    print("  - fig4_1_learning_curves.png （學習曲線）")
    print("  - fig4_2_policies.png （策略視覺化）")
    print("=" * 60)
