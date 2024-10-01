from flask import Flask, render_template, request, redirect, url_for, jsonify
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

app = Flask(__name__, template_folder='../web/templates')

# 配置路径
CONFIG_PATH = 'config/main.yml'
DEFAULT_CONFIG_PATH = 'config/default_main.yml'

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
        yaml.dump(config, file, allow_unicode=True)

# 登录页面
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != web_password:
            error = '密码错误'
        else:
            return redirect(url_for('config_page'))
    return render_template('login.html', error=error)

# 配置页面
@app.route('/config')
def config_page():
    config = load_config()
    return render_template('config.html', config=config)

@app.route('/save_config', methods=['POST'])
def save_config_route():
    try:
        config = load_config()
        config['AI_api_key'] = request.form['AI_api_key']
        config['AI_url'] = request.form['AI_url']
        config['root'] = request.form['root']
        config['group'] = request.form['group']
        config['bot_url'] = request.form['bot_url']
        config['bot_port'] = int(request.form['bot_port'])
        
        save_config(config)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e))

@app.route('/reset_config', methods=['POST'])
def reset_config():
    try:
        if os.path.exists(DEFAULT_CONFIG_PATH):
            with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as default_file:
                default_config = yaml.safe_load(default_file)
            save_config(default_config)
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Default configuration file not found")
    except Exception as e:
        return jsonify(success=False, message=str(e))

if __name__ == '__main__':
    app.run(debug=True)