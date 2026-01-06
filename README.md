# DNS 双栈解析对比测试工具 🌐

一个轻量级可视化 DNS 测试工具，专注于对比阿里云 DNS 与谷歌 DNS 的 IPv4/IPv6 双栈解析能力。
http://47.100.32.213:88/
## ✨ 核心功能

- **双栈解析对比**: 同时测试 IPv4 (A) 和 IPv6 (AAAA) 记录解析
- **性能可视化**: 柱状图直观展示解析耗时对比
- **一键测试**: 输入域名即可自动对比阿里云 DNS vs 谷歌 DNS
- **客观分析**: 基于实际测试数据进行性能对比

## 🚀 快速开始

### 环境要求

- **推荐**: Python 3.8+
- **最低要求**: Python 3.6+ (使用 `requirements_3.6.txt`)
- 支持 IPv4/IPv6 网络环境

### 关于虚拟环境

本项目推荐使用 Python 虚拟环境来管理依赖，这样可以：

- **隔离依赖**: 避免与其他项目的依赖冲突
- **版本控制**: 为项目锁定特定的包版本
- **环境清洁**: 便于项目的部署和分发
- **开发友好**: 不同项目可以使用不同版本的相同包

### 环境准备

#### 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv dns_test_env

# 激活虚拟环境
# Windows:
dns_test_env\Scripts\activate
# Linux/Mac:
source dns_test_env/bin/activate
```

#### 安装依赖

**Python 3.8+ (推荐):**
```bash
pip install -r requirements.txt
```

**Python 3.6 (兼容版本):**
```bash
pip install -r requirements_3.6.txt
```
> ⚠️ **注意**: Python 3.6 已于 2021 年停止官方支持，建议升级到 Python 3.8+ 以获得更好的性能和安全性。Python 3.6 版本使用最小化依赖配置，完全避免编译问题，适合生产环境快速部署。

### 运行工具

```bash
# 确保虚拟环境已激活
streamlit run app.py
```

工具将在浏览器中自动打开，默认地址: http://localhost:8501

### 退出虚拟环境

```bash
deactivate
```

## 📊 测试说明

### 支持的 DNS 服务器

- **阿里 DNS**: 223.5.5.5 - 国内主流公共 DNS 服务
- **Google DNS**: 8.8.8.8 - 国际知名公共 DNS 服务

### 测试内容

1. **IPv4 解析**: A 记录查询
2. **IPv6 解析**: AAAA 记录查询
3. **性能指标**: 解析耗时 (毫秒)
4. **TTL 值**: 记录生存时间

## 🎯 测试分析

工具将自动分析并对比两个 DNS 服务在以下方面的表现：

- **IPv4/IPv6 解析成功率**: 统计各类型记录的解析成功情况
- **响应速度**: 精确测量 DNS 查询耗时
- **TTL 值**: 显示记录缓存时间
- **性能对比**: 客观展示两者在不同场景下的表现差异

## 🔧 配置说明

### DNS 服务器配置

在 `app.py` 中的 `DNS_SERVERS` 字典中可以修改测试的 DNS 服务器：

```python
DNS_SERVERS = {
    '阿里 DNS': '223.5.5.5',
    'Google DNS': '8.8.8.8'
}
```

如需添加更多 DNS 服务器进行对比测试，可以在此字典中添加新的条目。

## 📈 输出结果

- **实时结果展示**: 测试完成后立即显示各 DNS 服务器的解析结果
- **可视化图表**: Plotly 柱状图展示解析耗时对比
- **性能分析**: 自动分析并客观对比阿里云 DNS vs 谷歌 DNS 的性能差异
- **成功率统计**: IPv4/IPv6 解析成功率统计

## 🏗️ 技术架构

- **前端界面**: Streamlit
- **DNS 查询**: dnspython
- **数据可视化**: Plotly

## 📝 使用示例

1. 激活虚拟环境: `dns_test_env\Scripts\activate` (Windows) 或 `source dns_test_env/bin/activate` (Linux/Mac)
2. 启动工具: `streamlit run app.py`
3. 在输入框中输入域名，如: `www.baidu.com`
4. 点击"开始测试"按钮
5. 等待测试完成，查看结果和图表分析
6. 测试完成后退出虚拟环境: `deactivate`

## 🔍 故障排除

- **连接超时**: 检查网络连接和 DNS 服务器可达性
- **IPv6 解析失败**: 确认网络环境支持 IPv6
- **部分解析失败**: 某些域名可能不支持 IPv6 或某些 DNS 服务不可用

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具。

## 📄 许可证

本项目仅用于技术演示和测试目的。
