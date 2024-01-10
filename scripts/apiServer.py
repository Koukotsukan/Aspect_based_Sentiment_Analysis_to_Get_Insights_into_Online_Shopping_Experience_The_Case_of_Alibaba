from flask import Flask, request, jsonify
from pyabsa import AspectTermExtraction as ATEPC
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # TEST ONLY Cross Original Resources Stricts
# CORS(app, resources={r"/predict": {"origins": "https://aliexperience.online"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://aliexperience.online')  # 域名
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response



@app.route("/predict", methods=["POST"])
def predict():
    # Load the weaker model
    # triplet_extractor = ATEPC.AspectExtractor(
    #     checkpoint="checkpoints/fast_lcf_atepc_custom_dataset_cdw_apcacc_84.81_apcf1_70.62_atef1_55.54",
    #     auto_device=True,
    #     cal_perplexity=True,
    # )

    triplet_extractor = ATEPC.AspectExtractor(
        checkpoint="checkpoints/fast_lcf_atepc_custom_dataset_cdw_apcacc_91.06_apcf1_91.07_atef1_83.09",
        auto_device=True,
        cal_perplexity=True,
    )

    # Get the text from the request
    data = request.get_json(force=True)
    text = data["text"]
    recaptcha_response = request.json.get('recaptchaResponse')

    # reCAPTCHA 验证请求
    secret_key = "6Lc2hDopAAAAAFAbpqo-xyhYcwUXCYFfk9O2e5Ob"
    recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        'secret': secret_key,
        'response': recaptcha_response
    }
    recaptcha_request = requests.post(recaptcha_verify_url, data=payload)
    recaptcha_result = recaptcha_request.json()

    # 检查 reCAPTCHA 验证是否成功
     if not recaptcha_result.get('success') or recaptcha_result.get('score') < 0.5:
        # 如果验证失败或得分低于阈值（例如 0.5）
        return jsonify({'error': 'reCAPTCHA verification failed'}), 400
    #
    # Predict
    result = triplet_extractor.predict(text)

    formed_result = {
        "tokens": result["tokens"],
        "positions": [item for sublist in result["position"] for item in sublist],
        "sentiments": result["sentiment"],
        "aspects": result["aspect"],
        "confidences": result["confidence"]
    }

    # 返回新的JSON结果
    return jsonify(formed_result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
