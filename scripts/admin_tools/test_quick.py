import urllib.request
import urllib.error
import json

KEY = 'sk-ws-H.IRMLYE.kWPQ.MEUCIQCyysRaStOHxFEO4sO_cbGi_ZjXab66QcPvGsf2cyAm_wIgdkFYeWKKbuI4FNao6T60U2oI9BLzj74q4PgdK8VrSA8'
URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions'

def test(key, model):
    payload = json.dumps({
        'model': model,
        'messages': [{'role': 'user', 'content': 'OK'}],
        'max_tokens': 5
    }).encode()
    req = urllib.request.Request(
        URL, data=payload,
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return 'OK'
    except urllib.error.HTTPError as e:
        return f'{e.code} {e.read().decode()[:150]}'
    except Exception as e:
        return str(e)

print('qwen-vl-ocr-2025-11-20:', test(KEY, 'qwen-vl-ocr-2025-11-20'))
print('qwen3.7-plus:', test(KEY, 'qwen3.7-plus'))
print('glm-5.1:', test(KEY, 'glm-5.1'))
