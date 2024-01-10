from flask import Flask, request, jsonify, render_template, send_from_directory, g
from pyabsa import AspectTermExtraction as ATEPC
from flask_cors import CORS
import requests
from celery import Celery
import os
import logging
import tempfile
import uuid
import json
import unicodedata
import magic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
# CORS(app)  # TEST ONLY Cross Original Resources Strict
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

RESULTS_DIR = 'results'
os.makedirs(RESULTS_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summary')
def summary():
    return render_template('summary.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/database')
def database():
    return render_template('database.html')

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@celery.task(bind=True)
def process_file(self, file_path):
    logger.info("Starting file processing")

    try:
        logger.info(f"Loading model from checkpoint")
        triplet_extractor = ATEPC.AspectExtractor(
            checkpoint="checkpoints/fast_lcf_atepc_custom_dataset_cdw_apcacc_91.06_apcf1_91.07_atef1_83.09",
            auto_device=True,
            cal_perplexity=False,
        )

        logger.info(f"Running batch_predict on file: {file_path}")
        result = triplet_extractor.batch_predict(
            target_file=file_path,
            save_result=False,
            pred_sentiment=True,
        )

        logger.info("Saving results to temporary file")
        random_filename = f"{uuid.uuid4()}"
        result_file_path = os.path.join(RESULTS_DIR, random_filename)

        # 将结果保存到文件
        with open(result_file_path, 'w+') as temp_file:
            json.dump(result, temp_file)

        # 返回文件名，而不是完整路径
        return {'status': 'completed', 'result_file_path': random_filename}

        logger.info(f"File processing completed, result file: {result_filename}")
    except Exception as e:
        logger.error(f"Error during file processing: {e}")
        raise e

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

def is_punctuation_or_non_english(token):
    # 检查 token 是否是标点符号或非英文字符
    return any(unicodedata.category(char).startswith('P') for char in token) or not token.isascii()

@app.route('/show-result/<filename>')
def show_result(filename):
    result_file_path = os.path.join(RESULTS_DIR, filename)
    try:
        with open(result_file_path, 'r') as file:
            results_data = json.load(file)  # 加载 JSON 数据

        # 处理 JSON 数据以匹配 HTML 模板的需求
        processed_results = []
        for data in results_data:
            tokens = data.get('tokens', [])
            position = data.get('position', [])
            sentiment = data.get('sentiment', [])
            confidence = data.get('confidence', [])

            modified_sentence = []
            for index, token in enumerate(tokens):
                formatted_token = token
                if any(index in pos for pos in position):
                    pos_index = next(i for i, pos in enumerate(position) if index in pos)
                    sentiment_value = sentiment[pos_index]
                    confidence_value = confidence[pos_index]
                    formatted_token = f"<span class='{sentiment_value.lower()}'>{token}&lt;sentiment:{sentiment_value}, confidence:{confidence_value:.4f}&gt;</span>"

                if modified_sentence and not is_punctuation_or_non_english(token):
                    modified_sentence.append(" " + formatted_token)
                else:
                    modified_sentence.append(formatted_token)

            joined_sentence = ''.join(modified_sentence)
            processed_results.append({'sentence': joined_sentence})

        return render_template('result_page.html', results=processed_results)
    except IOError:
        return 'Result not found', 404

@app.route('/download-json')
def download_json():
    filename = request.args.get('filename')  # 从查询参数中获取 filename
    result_file_path = os.path.join(RESULTS_DIR, filename)
    try:
        with open(result_file_path, 'r') as file:
            results_data = json.load(file)  # 加载 JSON 数据
            return jsonify(results_data)
    except IOError:
        return 'Json not found', 404

@app.route('/upload', methods=['POST'])
def upload_file():
    # reCAPTCHA 验证请求
    recaptcha_response = request.form.get('recaptchaResponse')
    secret_key = "[Your Own Secret 4 Google reCHATPCHA]"
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
        score = recaptcha_result.get('score', 0)  # 获取分数，如果不存在则默认为0
        return jsonify({'error': f'reCAPTCHA verification failed, score: {score}'}), 400

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    max_file_size = 1 * 1024 * 1024  # 1 MB
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):

        # 检查文件大小
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)  # 重置文件指针位置

        if file_length > max_file_size:
            # 如果文件超过限制大小，则返回错误信息
            return jsonify({'error': 'File size exceeds limit (1 MB)'}), 413
        mime_type = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)  # 重置文件指针到开头

        # 定义允许的 MIME 类型
        allowed_mime_types = {'text/plain', 'text/csv'}

        if mime_type not in allowed_mime_types:
            return jsonify({'error': 'File type not allowed (Fake File Extension)'}), 403
        else:
            # 保存文件到临时路径
            file_path = os.path.join('/tmp', file.filename)
            file.save(file_path)

            # 启动后台任务
            task = process_file.apply_async(args=[file_path])
            return jsonify({'task_id': task.id}), 202

    else:
        return jsonify({'error': 'File type not allowed (Wrong File Extension)'}), 415


@app.route('/check-status/<task_id>', methods=['GET'])
def check_status(task_id):
    logger.info("Starting file processing")
    task = process_file.AsyncResult(task_id)
    if task.state == 'PENDING':
        # 任务仍在运行中
        return jsonify({'status': 'pending'}), 202
    elif task.state == 'FAILURE':
        # 任务执行失败
        return jsonify({'status': 'error', 'error': str(task.info)}), 500
    return jsonify(task.result)


@app.route("/predict", methods=["POST"])
def predict():
    print ("Acceptted New Mission")
    # Get the text from the request
    data = request.get_json(force=True)
    text = data["review"]
    recaptcha_response = request.json.get('recaptchaResponse')
    modelChoice = data['modelChoice']

    # reCAPTCHA 验证请求
    secret_key = "[Your Own Secret 4 Google reCHATPCHA]"
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
        score = recaptcha_result.get('score', 0)  # 获取分数，如果不存在则默认为0
        return jsonify({'error': f'reCAPTCHA verification failed, score: {score}'}), 400

    else:
        if int(modelChoice) == 1:
            triplet_extractor = ATEPC.AspectExtractor(
                checkpoint="checkpoints/fast_lcf_atepc_custom_dataset_cdw_apcacc_91.06_apcf1_91.07_atef1_83.09",
                auto_device=True,
                cal_perplexity=False,
            )
            # Predict
            result = triplet_extractor.predict(text)
        elif int(modelChoice) == 2:
            triplet_extractor = ATEPC.AspectExtractor(
                checkpoint="checkpoints/lcf_atepc_custom_dataset_cdw_apcacc_85.95_apcf1_63.37_atef1_72.52",
                auto_device=True,
                cal_perplexity=False,
            )
            # Predict
            result = triplet_extractor.predict(text)
        elif int(modelChoice) == 3:
            triplet_extractor = ATEPC.AspectExtractor(
                checkpoint="checkpoints/fast_lcf_atepc_custom_dataset_cdw_apcacc_83.76_apcf1_70.59_atef1_67.63",
                auto_device=True,
                cal_perplexity=False,
            )
            # Predict
            result = triplet_extractor.predict(text)
        elif int(modelChoice) == 4:
            triplet_extractor = ATEPC.AspectExtractor(
                checkpoint="checkpoints/bert_base_atepc_custom_dataset_cdw_apcacc_84.12_apcf1_67.38_atef1_73.15",
                auto_device=True,
                cal_perplexity=False,
            )
            # Predict
            result = triplet_extractor.predict(text)
        else:
            return jsonify({'error': 'Model Not Found'}), 400

        formed_result = {
            "tokens": result["tokens"],
            "positions": [item for sublist in result["position"] for item in sublist],
            "sentiments": result["sentiment"],
            "aspects": result["aspect"],
            "confidences": result["confidence"],
            "captcha_score": recaptcha_result.get('score')
        }

        # 返回新的JSON结果
        return jsonify(formed_result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)