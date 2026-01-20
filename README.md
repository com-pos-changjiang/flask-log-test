# Flask 实时日志监控系统

基于 Flask-SocketIO 的实时日志推送与显示案例。

## 功能特性

✨ **实时推送** - 后端日志实时推送到前端，无需刷新页面  
🎨 **美观界面** - 现代化 UI 设计，支持深色日志显示  
📊 **日志统计** - 实时统计 INFO、WARNING、ERROR 日志数量  
🚀 **批量测试** - 支持批量日志发送，方便测试实时效果  
🔌 **WebSocket 连接** - 基于 SocketIO 的双向通信

## 技术栈

- **后端**: Flask + Flask-SocketIO + Python logging
- **前端**: HTML + CSS + JavaScript + Socket.IO Client
- **通信**: WebSocket (SocketIO)

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问: `http://127.0.0.1:5000`

## 使用方法

### 触发日志

在页面中点击以下按钮触发不同级别的日志：

1. **发送 INFO 日志** - 发送一条 INFO 级别的日志
2. **发送 WARNING 日志** - 发送一条 WARNING 级别的日志
3. **发送 ERROR 日志** - 发送一条 ERROR 级别的日志
4. **批量日志测试** - 批量发送多条日志，测试实时效果
5. **清除日志** - 清除前端日志显示区域

### API 接口

- `GET /` - 主页，显示日志监控界面
- `GET /trigger-info` - 触发 INFO 日志
- `GET /trigger-warning` - 触发 WARNING 日志
- `GET /trigger-error` - 触发 ERROR 日志
- `GET /batch-logs` - 批量发送日志
- `GET /clear-logs` - 清除前端日志

## 核心实现

### 后端 - 自定义日志处理器

```python
class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        socketio.emit('log_message', {'data': log_entry})
```

这个自定义 Handler 将 Python 的 logging 模块与 SocketIO 连接起来，每次调用 `app.logger.info()` 等方法时，日志会自动推送到前端。

### 前端 - SocketIO 监听

```javascript
const socket = io();
socket.on('log_message', (msg) => {
    const data = msg.data;
    // 显示日志
});
```

前端监听 `log_message` 事件，实时接收并显示日志。

## 项目结构

```
web-log-test/
├── app.py                 # Flask 后端应用
├── requirements.txt       # 依赖列表
├── templates/
│   └── index.html        # 前端页面
├── Gemini.md             # 原始需求文档
└── README.md             # 使用说明（本文件）
```

## 使用场景

- 📋 实时监控系统运行状态
- 🐛 调试和问题排查
- 📊 数据处理过程可视化
- 🔄 长时间任务进度跟踪
- 💬 实时日志分析和监控

## 注意事项

1. 确保防火墙允许 5000 端口访问
2. 建议使用 Chrome 或 Firefox 等现代浏览器
3. 批量日志测试会有短暂的延迟，以展示实时效果
4. 日志容器会自动滚动到最新日志

## 扩展建议

- 🗃️ 添加日志持久化功能（保存到数据库或文件）
- 🔍 添加日志搜索和过滤功能
- 📈 添加日志图表分析
- 🔐 添加用户认证和权限控制
- 🌐 支持多客户端同时监听日志

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎反馈。
