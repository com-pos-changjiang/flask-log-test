要实现在 Python Flask 后端像调用 `print` 一样发送日志，并让前端实时接收并显示，最成熟且易用的方案是结合 **Python 标准库的 `logging` 模块** 和 **Flask-SocketIO**。

以下是为你推荐的开源工具组合及实现方案：

### 1. 核心工具推荐

- **Flask-SocketIO**: 这是 Flask 生态中最强大的 WebSocket 库，它能实现后端与前端的“双向实时通信”。你可以利用它将日志“推送”给浏览器。
- **Logging Custom Handler**: 利用 Python 自带的 `logging` 模块编写一个自定义 Handler，每当后端触发日志记录时，自动通过 SocketIO 发送。

------

### 2. 实现流程演示

#### 后端实现 (Python)

你可以定义一个 `SocketIOHandler`，将其挂载到 Flask 的应用日志中：

Python

```
import logging
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 自定义日志处理器，将日志推送到前端
class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        # 这里的 'log_message' 是前端监听的事件名
        socketio.emit('log_message', {'data': log_entry})

# 配置日志
handler = SocketIOHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trigger-log')
def trigger():
    # 就像 print 一样使用，前端会实时收到
    app.logger.info("这是一条后端触发的实时日志！")
    return "日志已发送"

if __name__ == '__main__':
    socketio.run(app, debug=True)
```

#### 前端实现 (HTML/JS)

前端只需要连接 SocketIO 并监听 `log_message` 事件：

HTML

```
<div id="log-container" style="background: #222; color: #0f0; padding: 10px; height: 300px; overflow-y: scroll;">
    </div>

<script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
<script>
    const socket = io();
    const container = document.getElementById('log-container');

    socket.on('log_message', function(msg) {
        const item = document.createElement('div');
        item.textContent = msg.data;
        container.appendChild(item);
        // 自动滚动到底部
        container.scrollTop = container.scrollHeight;
    });
</script>
```

### 