from flask import Flask
from flask import render_template
from flask import request
import os
import time
import Strix

try:
    from werkzeug.utils import secure_filename
except:
    from werkzeug import secure_filename

app = Flask(__name__)

# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #파일 업로드 용량 제한 단위:바이트

# 홈화면 HTML 렌더링
@app.route('/')
def home_page():
    return render_template('home.html')


# 파일 업로드 처리
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # 저장할 경로 + 파일명
        f.save('./uploads/' + secure_filename(f.filename))
        return render_template('upload.html')

@app.route('/result')
def result_page():
    r = analyze_file()
    return render_template('result.html', result = r)

def analyze_file():
    passenger = Strix.strix(os.listdir("./uploads/")[0])
    return "M: {}, F: {}, C{}".format(passenger["M"], passenger["F"], passenger["C"])

# 서버 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)