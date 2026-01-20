import logging
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import time

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
    """主页 - 显示日志实时监控界面"""
    return render_template('index.html')

@app.route('/trigger-info')
def trigger_info():
    """触发一条 INFO 级别日志"""
    app.logger.info("这是一条后端触发的 INFO 日志！")
    return jsonify({"status": "success", "message": "INFO 日志已发送"})

@app.route('/trigger-warning')
def trigger_warning():
    """触发一条 WARNING 级别日志"""
    app.logger.warning("⚠️ 警告：这是一条 WARNING 级别的日志！")
    return jsonify({"status": "success", "message": "WARNING 日志已发送"})

@app.route('/trigger-error')
def trigger_error():
    """触发一条 ERROR 级别日志"""
    app.logger.error("❌ 错误：这是一条 ERROR 级别的日志！")
    return jsonify({"status": "success", "message": "ERROR 日志已发送"})

@app.route('/batch-logs')
def batch_logs():
    """批量触发多条日志，用于测试实时效果"""
    app.logger.info("🚀 开始批量日志测试...")
    
    time.sleep(0.5)
    app.logger.info("正在初始化系统...")
    
    time.sleep(0.5)
    app.logger.warning("检测到配置文件可能需要更新")
    
    time.sleep(0.5)
    app.logger.info("正在连接数据库...")
    
    time.sleep(0.5)
    app.logger.info("数据库连接成功")
    
    time.sleep(0.5)
    app.logger.info("正在加载用户数据...")
    
    time.sleep(0.5)
    app.logger.error("⚠️ 无法加载部分用户数据，但系统继续运行")
    
    time.sleep(0.5)
    app.logger.info("✅ 批量日志测试完成！")
    
    return jsonify({"status": "success", "message": "批量日志已发送"})

@app.route('/clear-logs')
def clear_logs():
    """清除前端日志显示"""
    socketio.emit('clear_logs')
    return jsonify({"status": "success", "message": "日志已清除"})

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Flask 实时日志监控系统启动中...")
    print("=" * 50)
    print("📝 访问地址: http://127.0.0.1:25000")
    print("💡 提示: 打开浏览器访问上述地址即可查看实时日志")
    print("=" * 50)
    socketio.run(app, debug=True, host='0.0.0.0', port=25000)
