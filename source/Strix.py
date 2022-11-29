import os
import Diarization as d
import VoiceClassifier as vc

def evaluate(predicts):
    m_count = 0
    f_count = 0
    c_count = 0

    for predict in predicts:
        if predict == "F": m_count += 1
        elif predict == "M": f_count += 1
        elif predict == "C": c_count += 1

    max_v = max(m_count, f_count, c_count)
    if m_count == max_v: return "M"
    elif f_count == max_v: return "F"
    elif c_count == max_v: return "C"

def strix(wav):
    counter = {}
    counter["M"] = 0
    counter["F"] = 0
    counter["C"] = 0

    d.seperation(wav)
    speechs = os.listdir("./sep/")

    spk_dict = {}
    for speech in speechs:
        if speech[8:10] not in spk_dict:
            spk = speech[8:10]
            spk_dict[spk] = [speech]
        else:
            spk_dict[spk].append(speech)

    for _, value in spk_dict:
        predict_list = []
        for item in value:
            predict_list.append(vc.voice_classify("./sep/" + item))
        
        total_predict = evaluate(predict_list)
        if total_predict == "M": counter["M"] += 1
        elif total_predict == "F": counter["F"] += 1
        elif total_predict == "C": counter["C"] += 1

    return counter

def main():
    wav_path = "./test/audio.wav"
    
    for key, value in strix(wav_path):
        print(key + ":", value)
    pass

if __name__ == "__main__":
    main()