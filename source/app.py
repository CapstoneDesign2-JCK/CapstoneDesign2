from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
import os
import time
import Strix

def analyze_file():
    file = os.listdir("./uploads/")[0]
    passenger = Strix.strix("./uploads/" + file)

    old_files = os.listdir("./uploads/")
    for old_file in old_files:
        if old_file.split(".")[-1] == "wav":
            os.remove("./uploads/" + old_file)
            
    return passenger

def guess_relationship(passenger):
    m_num = passenger["M"]
    f_num = passenger["F"]
    c_num = passenger["C"]

    if c_num > 0: return "Family"
    elif m_num == 1 and f_num == 1: return "Couple"
    elif m_num != 0 and f_num == 0: return "Friend"
    elif m_num == 0 and f_num != 0: return "Friend"
    else: return "Group"

def recommend_enter(enter, passenger):
    couple_route_text = "커플에게 어울리는 뷰가 좋은 경로를 추천 드릴게요!"
    couple_route_link = "https://naver.me/FXZnlUiz"
    couple_route_img = url_for('static', filename='images/route.png')

    friend_music_text = "남성분들에게 인기 있는 IVE 음악을 추천 드릴게요!"
    friend_music_link = "https://youtu.be/F0B7HDiY-10"
    friend_music_img = url_for('static', filename='images/music.png')

    family_video_text = "어린아이에게 인기 있는 핑크퐁 영상을 추천 드릴게요!"
    family_video_link = "https://youtu.be/761ae_KDg_Q"
    family_video_img = url_for('static', filename="images/video.png")

    return_list = {}

    return_list["M"] = {}
    return_list["M"]["Friend"] = [friend_music_img, friend_music_link, friend_music_text]

    return_list["V"] = {}
    return_list["V"]["Family"] = [family_video_img, family_video_link, family_video_text]

    return_list["N"] = {}
    return_list["N"]["Couple"] = [couple_route_img, couple_route_link, couple_route_text]
    

    relation = guess_relationship(passenger)

    return tuple(return_list[enter][relation])

try:
    from werkzeug.utils import secure_filename
except:
    from werkzeug import secure_filename

app = Flask(__name__)

# 홈화면 HTML 렌더링
@app.route('/')
def home_page():
    return render_template('home.html')

enter_type = ""
# 파일 업로드 처리
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global enter_type
    old_files = os.listdir("./uploads/")
    for old_file in old_files:
        if old_file.split(".")[-1] == "wav":
            os.remove("./uploads/" + old_file)

    if request.method == 'POST':
        f = request.files['file']
        enter_type = request.form.get("entertain")
        f.save('./uploads/' + secure_filename(f.filename))
        return render_template('upload.html')

@app.route('/result')
def result_page():
    r = analyze_file()
    img, link, text = recommend_enter(enter_type, r)

    return render_template('result.html', Img = img, Link = link, Text = text)

# 서버 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)