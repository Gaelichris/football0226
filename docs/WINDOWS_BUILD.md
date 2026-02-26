# Windows 安装包自动构建指南

本项目已配置 GitHub Actions 自动构建 Windows 安装包。

## 自动构建触发条件

| 触发条件 | 说明 |
|---------|------|
| Push 到 main/master | 自动构建，生成 artifact |
| 创建 v* 标签 | 自动构建并创建 Release |
| Pull Request | 自动构建用于验证 |
| 手动触发 | 在 Actions 页面点击 "Run workflow" |

## 使用方法

### 方法一：从 Release 下载（推荐）

1. 前往仓库的 [Releases](../../releases) 页面
2. 下载最新的 `GFootball_Setup.exe`
3. 运行安装程序

### 方法二：从 Actions 下载

1. 前往仓库的 [Actions](../../actions) 页面
2. 点击最新的 "Build Windows Installer" workflow
3. 在 Artifacts 区域下载 `GFootball-Windows-Installer`

### 方法三：手动触发构建

1. 前往 [Actions](../../actions) 页面
2. 选择 "Build Windows Installer" workflow
3. 点击 "Run workflow"
4. 可选择是否创建 Release
5. 点击绿色 "Run workflow" 按钮

## 构建产物

| 文件 | 说明 |
|------|------|
| `GFootball_Setup.exe` | Windows 安装程序（推荐） |
| `GFootball_Portable.zip` | 便携版（解压即用） |

## 创建新版本 Release

```bash
# 打标签并推送
git tag v2.10.3
git push origin v2.10.3
```

这会自动触发构建并创建 GitHub Release。

## 本地构建（可选）

如果您想在本地 Windows 机器上构建，请参考 `gfootball_windows_installer.zip` 中的脚本。

## 游戏控制

- **方向键**: 移动球员
- **S**: 短传（进攻）/ 逼抢（防守）
- **A**: 高空球（进攻）/ 铲球（防守）
- **D**: 射门（进攻）/ 协防（防守）
- **W**: 长传
- **Q**: 切换球员
- **C**: 盘带
- **E**: 冲刺
- **Ctrl+C**: 退出游戏

## 故障排除

### 构建失败
- 检查 Actions 日志中的错误信息
- 确保 vcpkg 依赖正确安装

### 安装后无法运行
- 确保安装了 Visual C++ Redistributable
- 尝试以管理员身份运行

### 游戏黑屏
- 更新显卡驱动
- 尝试使用兼容模式运行
