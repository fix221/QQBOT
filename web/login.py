from flask import Flask, render_template, request, redirect, url_for
import yaml
import os

# 设置YAML文件的路径
yml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'web.yml')

# 读取YAML文件中的配置
with open(yml_path, 'r') as ymlfile:
    config = yaml.safe_load(ymlfile)

# 获取Web密码
web_password = config.get("WebPassword")
if web_password is None:
    raise Exception("Failed to load WebPassword from YAML file")

print("Loaded WebPassword:", web_password)  # 添加打印语句

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于保持客户端会话安全

# 登录页面
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != web_password:
            error = '密码错误'
        else:
            return redirect(url_for('config'))
    return render_template('login.html', error=error)

# 配置页面
@app.route('/config')
def config():
    return render_template('config.tsx')

if __name__ == '__main__':
    app.run(debug=True)