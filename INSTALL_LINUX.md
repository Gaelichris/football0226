# Google Research Football - Linux 安装指南

本文档介绍如何在 Linux 系统上编译和安装 Google Research Football 游戏环境。

## 系统要求

- **操作系统**: Ubuntu 18.04+ / Debian 10+ / 其他主流 Linux 发行版
- **Python**: 3.6 - 3.10
- **内存**: 建议 4GB+
- **磁盘空间**: 约 500MB

## 一、安装系统依赖

### Ubuntu / Debian

```bash
sudo apt-get update
sudo apt-get install -y \
    cmake \
    build-essential \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-ttf-dev \
    libsdl2-gfx-dev \
    libboost-all-dev \
    libegl1-mesa-dev \
    python3-dev \
    python3-pip
```

### CentOS / RHEL / Fedora

```bash
sudo dnf install -y \
    cmake \
    gcc-c++ \
    SDL2-devel \
    SDL2_image-devel \
    SDL2_ttf-devel \
    SDL2_gfx-devel \
    boost-devel \
    mesa-libEGL-devel \
    python3-devel \
    python3-pip
```

### Arch Linux

```bash
sudo pacman -S \
    cmake \
    base-devel \
    sdl2 \
    sdl2_image \
    sdl2_ttf \
    sdl2_gfx \
    boost \
    mesa \
    python \
    python-pip
```

## 二、安装 Python 依赖

```bash
pip3 install psutil numpy pygame opencv-python gym==0.21.0 absl-py wheel
```

## 三、编译游戏引擎

### 方式一：使用安装脚本（推荐）

```bash
cd /path/to/football0226

# 编译游戏引擎
bash gfootball/build_game_engine.sh

# 安装 Python 包
pip3 install -e .
```

### 方式二：手动编译

```bash
cd /path/to/football0226/third_party/gfootball_engine

# 清理旧的构建缓存
rm -f CMakeCache.txt

# 配置 CMake
cmake .

# 编译（-j 参数指定并行编译线程数）
make -j$(nproc)

# 创建符号链接
ln -sf libgame.so _gameplayfootball.so

# 返回项目根目录并安装
cd ../..
pip3 install -e .
```

## 四、验证安装

```bash
# 测试导入
python3 -c "import gfootball; print('gfootball 导入成功!')"

# 运行简单测试
python3 -c "
import gfootball.env as football_env
env = football_env.create_environment(env_name='academy_empty_goal_close', render=False)
obs = env.reset()
print('环境创建成功! 观测空间:', obs.shape)
env.close()
"
```

## 五、使用方法

### 1. 键盘玩游戏

```bash
# 需要图形环境
python3 -m gfootball.play_game --players "keyboard:left_players=1"
```

**键盘控制**:
- 方向键: 移动
- A: 短传
- S: 射门
- D: 长传
- W: 高球
- Q: 切换球员
- E: 冲刺

### 2. 作为强化学习环境

```python
import gfootball.env as football_env

# 创建环境
env = football_env.create_environment(
    env_name='11_vs_11_stochastic',  # 场景名
    stacked=False,                    # 是否堆叠帧
    representation='extracted',       # 观测表示
    rewards='scoring,checkpoints',    # 奖励类型
    render=False                      # 是否渲染
)

# 使用 gym 标准接口
obs = env.reset()
for _ in range(1000):
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    if done:
        obs = env.reset()

env.close()
```

### 3. 训练强化学习 Agent

```bash
# 使用 PPO2 训练（需要额外安装 TensorFlow 和 baselines）
pip3 install tensorflow==1.15.0 stable-baselines

python3 -m gfootball.examples.run_ppo2 \
    --level=academy_empty_goal_close \
    --num_timesteps=1000000
```

## 六、无头服务器运行

如果在没有图形界面的服务器上运行，使用 xvfb：

```bash
# 安装 xvfb
sudo apt-get install -y xvfb

# 使用 xvfb-run 运行
xvfb-run -a python3 your_script.py
```

或在代码中禁用渲染：

```python
env = football_env.create_environment(
    env_name='11_vs_11_stochastic',
    render=False  # 禁用渲染
)
```

## 七、常见场景列表

| 场景名称 | 描述 |
|---------|------|
| `11_vs_11_stochastic` | 完整 11v11 比赛（随机） |
| `11_vs_11_easy_stochastic` | 11v11 简单难度 |
| `11_vs_11_hard_stochastic` | 11v11 困难难度 |
| `5_vs_5` | 5v5 小场比赛 |
| `1_vs_1_easy` | 1v1 简单 |
| `academy_empty_goal` | 空门射门 |
| `academy_empty_goal_close` | 近距离空门 |
| `academy_run_to_score` | 带球跑动射门 |
| `academy_run_to_score_with_keeper` | 带球射门（有守门员） |
| `academy_pass_and_shoot_with_keeper` | 传球射门 |
| `academy_3_vs_1_with_keeper` | 3v1 进攻 |
| `academy_corner` | 角球 |
| `academy_counterattack_easy` | 反击（简单） |
| `academy_counterattack_hard` | 反击（困难） |

## 八、常见问题

### Q1: 编译时找不到 Boost.Python

```bash
# 检查 boost-python 包名
apt-cache search boost | grep python

# Ubuntu 20.04+ 通常是：
sudo apt-get install libboost-python-dev
```

### Q2: OpenGL 相关错误

```bash
# 设置 Mesa 环境变量
export MESA_GL_VERSION_OVERRIDE=3.2
export MESA_GLSL_VERSION_OVERRIDE=150
```

### Q3: 导入时报错 "libgame.so not found"

确保编译完成后创建了符号链接：

```bash
cd third_party/gfootball_engine
ln -sf libgame.so _gameplayfootball.so
```

### Q4: pygame 初始化失败

```bash
# 安装音频依赖
sudo apt-get install -y libsdl2-mixer-dev pulseaudio

# 或禁用音频
export SDL_AUDIODRIVER=dummy
```

## 九、编译产物

编译成功后会生成以下文件：

```
third_party/gfootball_engine/
├── libgame.so              # 游戏引擎主库（约 60MB）
├── _gameplayfootball.so    # 符号链接，指向 libgame.so
└── ...
```

## 十、卸载

```bash
pip3 uninstall gfootball

# 清理编译产物
cd third_party/gfootball_engine
rm -f libgame.so _gameplayfootball.so CMakeCache.txt
rm -rf CMakeFiles/
```

## 参考链接

- [GitHub 仓库](https://github.com/google-research/football)
- [官方文档](https://github.com/google-research/football/blob/master/gfootball/doc/compile_engine.md)
- [OpenAI Gym 文档](https://gym.openai.com/)

---

*文档版本: 1.0*  
*最后更新: 2026-02-27*
