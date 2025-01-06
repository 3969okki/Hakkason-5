import requests
import re
import json



#VOICEVOXは音声作成後wavになって音声が作成される
def synthesize_voice(word, speaker = 1,speed = 1.2, filename = "output.wav"):

    #テキストからの音声合成クエリ作成
    #クエリ データベースに送る命令文
    text = re.sub(r'\(.*?\)', '', str(word))
    query_payload = {'text': text, 'speaker': speaker}
    query_response = requests.post(f'http://localhost:50021/audio_query', params=query_payload)

    if query_response.status_code != 200:
        print(f"Error in audio_query: {query_response.text}")
        return
    

    query = query_response.json()
    query['speed'] = speed  # speedを変更
    
    #音声データの作成
    synthesis_payload = {'speaker' : speaker}
    synthesis_response = requests.post(f'http://localhost:50021/synthesis', params = synthesis_payload, json = query)

    if synthesis_response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(synthesis_response.content)
        print(f"音声が {filename} に保存されました。")
    else:
        print(f"Error in synthesis: {synthesis_response.text}")


"""
def main():
    text = "こんにちは"
    synthesize_voice(text, speaker=1, filename="voicevox_output.wav")


if __name__ == '__main__':
    main()
"""




