document.addEventListener("DOMContentLoaded", function() {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.nav li a');
    const menuToggle = document.getElementById("menu-toggle");
    const nav = document.querySelector(".nav");
    const leftDiv = document.querySelector('.left');
    const reviewContainer = document.querySelector('.input-container');

    // Highlight current page in menu
    menuItems.forEach(menuItem => {
        const menuItemLink = menuItem.getAttribute('href');
        if (currentPath === menuItemLink) {
            menuItem.style.color = "#000000";
            menuItem.style.borderBottom = "2px solid #af2639";
        } else {
            menuItem.style.color = "rgba(0, 0, 0, 0.4)";
        }
    });

    // Menu toggle functionality
    menuToggle.addEventListener("click", function () {
        nav.classList.toggle("show");
    });

function adjustLayout() {
console.log("adjustLayout called");
		if (!reviewContainer) {
            return; // 如果 reviewContainer 不存在则退出函数
        }
        
     const radioButtonsHTML = 
        '<div style="display: flex; flex-wrap: wrap; justify-content: space-evenly; align-items: center; margin-bottom: 10px;">' +
        '<label style="font-weight: bold; margin-right: 10px;">' +
        '<input type="radio" id="FAST-LCF-DeBERTa" name="model" value="1" checked> FAST-LCF(DeBERTa)' +
        '</label>' +
        '<label style="margin-right: 10px;">' +
        '<input type="radio" id="LCF-DeBERTa" name="model" value="2"> LCF(DeBERTa)' +
        '</label>' +
        '<label style="margin-right: 10px;">' +
        '<input type="radio" id="FAST-LCF-BERT" name="model" value="3"> FAST-LCF(BERT)' +
        '</label>' +
        '<label>' +
        '<input type="radio" id="BERT-Base" name="model" value="4"> BERT-Base' +
        '</label>' +
        '</div>';

    if (window.innerWidth < 768) {
        // // 移动端布局
        leftDiv.classList.remove('left');
        // reviewContainer.innerHTML = 
            // '<form id="review-form" method="POST" action="https://aliexperience.online/predict">' +
            // '<textarea id="review" name="review" placeholder="Your Review" required></textarea>' +
            // radioButtonsHTML +
            // '<input type="submit" value="Submit" style="margin-right: 5px;">' +
            // '<input type="file" id="file-upload" name="file" accept=".txt, .csv" style="display: none;">' +
            // '<input type="button" id="upload-button" value="Upload">' +
            // '</form><small><em>*Uploading a file only supports default model, file types .txt &amp; .csv with one sentence per line.</em></small>';
    
	} else {
        // 桌面端布局
        leftDiv.classList.add('left');
        reviewContainer.innerHTML = 
            '<form id="review-form" method="POST" action="/predict">' +
            '<div style="display: flex; flex-wrap: wrap; align-items: center;">' +
            '<div style="flex-grow: 1;">' +
            '<input type="text" id="review" name="review" placeholder="Your Review" required>' +
            '</div>' +
            radioButtonsHTML +
            '<div>' +
            '<input type="file" id="file-upload" name="file" accept=".txt, .csv" style="display: none;">' +
            '<input type="submit" value="Submit" style="margin-right: 10px;">' +
            '<input type="button" id="upload-button" value="Upload" >' +
            '</div>' +
            '</div>' +
            '</form>'+"<small><em>*Uploading a file only supports default model, file types .txt &amp; .csv with one sentence per line.</em></small>";
    }


        var fileInput = document.getElementById('file-upload');
        var uploadButton = document.getElementById('upload-button');

        uploadButton.addEventListener('click', function() {
            fileInput.click(); // 当点击上传按钮时触发文件输入的点击事件
        });

        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                handleFileUpload(this.files[0]);
            }
        });
        console.log("adjustLayout finished");

        }
		adjustLayout();
        window.addEventListener('resize', adjustLayout);
        attachFormSubmitEvent();
    

    // attachFormSubmitEvent 函数
    function attachFormSubmitEvent() {
        const form = document.getElementById('review-form');
        if (form) {
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                grecaptcha.execute('[Your Own Sitekey 4 Google reCHATPCHA]', { action: 'submit' }).then(function(token) {
                    const recaptchaResponseInput = document.createElement('input');
                    recaptchaResponseInput.setAttribute('type', 'hidden');
                    recaptchaResponseInput.setAttribute('name', 'recaptchaResponse');
                    recaptchaResponseInput.setAttribute('value', token);
                    form.appendChild(recaptchaResponseInput);

                    // 调用 submitFormWithRecaptcha 函数
                    submitFormWithRecaptcha(form);
                });
            });
        }
    }

    // submitFormWithRecaptcha 函数
    function submitFormWithRecaptcha(form) {
        const formData = new FormData(form);
		const review = formData.get('review');
		const modelChoice = formData.get('model'); // 获取选中的模型选项
        const data = {
            'review': review,
            'modelChoice': modelChoice, // 添加模型选项至请求数据中
            'recaptchaResponse': formData.get('recaptchaResponse')
        };

        // 显示遮罩和加载指示器
        const overlay = document.getElementById('overlay');
        const loader = document.getElementById('loader');
        const popup = document.getElementById('popup');
        const responseContent = document.getElementById('responseContent');

        overlay.style.display = 'block';
        loader.style.display = 'block';

        fetch('/predict', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.error); // 只抛出错误信息
                });
            }
            return response.json();
        })
        .then(data => {
            // 隐藏遮罩和加载指示器
            overlay.style.display = 'none';
            loader.style.display = 'none';

            // 显示弹出窗口和处理响应数据
            popup.style.display = 'block';
            if (!data.aspects || data.aspects.length === 0) {
                let new_sentence = buildSentence(data);
                responseContent.innerHTML = new_sentence + "<br/><br/><span style='color: red;'><i class='fas fa-sad-tear'></i></span></i> Sorry, we didn't detect any aspect from your input.";
            } else {
                let new_sentence = buildSentence(data);
                let table_html = buildTable(data);
                responseContent.innerHTML = "<p style='font-size:24px;font-weight:bold;'>Sentence:</p><br/>" + new_sentence + "<br/><br/>" + table_html;
            }
        })
        .catch(error => {
            overlay.style.display = 'none';
            loader.style.display = 'none';
            popup.style.display = 'block';
            responseContent.innerHTML = "<p style='color: red;'><i class='fas fa-exclamation-circle'></i> " + error.message + "</p>";
            console.error('Error:', error);
        });
    }

    // buildSentence 函数
    function buildSentence(data) {
        let new_sentence = "";
        if (data.tokens && data.positions) {
            data.tokens.forEach((token, i) => {
                let nextToken = data.tokens[i + 1] || "";
                let sentiment = data.positions.includes(i) ? data.sentiments[data.positions.indexOf(i)] : null;
                let colored_token = token;

                if (sentiment === "Positive") {
                    colored_token = `<span style="color: green;">${token}</span>`;
                } else if (sentiment === "Negative") {
                    colored_token = `<span style="color: red;">${token}</span>`;
                } else if (sentiment === "Neutral") {
                    colored_token = `<span style="color: #444;">${token}</span>`;
                }

                new_sentence += colored_token;
if (!nextToken.match(/^[\p{P}\p{Z}\p{S}^\p{N}]/u)) {
    new_sentence += " ";
}

            });
        }
        return new_sentence;
    }

    // buildTable 函数
    function buildTable(data) {
        let table_html = '<table style="width: 100%; border-collapse: collapse;">';
        table_html += '<tr><th style="border: 1px solid #FF8C00; padding: 8px; text-align: left;">Aspect</th><th style="border: 1px solid #FF8C00; padding: 8px; text-align: left;">Polarity</th><th style="border: 1px solid #FF8C00; padding: 8px; text-align: left;">Confidence</th></tr>';
        data.aspects.forEach((aspect, index) => {
            table_html += `<tr><td style="border: 1px solid #FF8C00; padding: 8px; text-align: left;">${aspect}</td><td style="border: 1px solid #FF8C00; padding: 8px; text-align: left;">${data.sentiments[index]}</td><td style="border: 1px solid #FF8C00; padding: 8px; text-align: left;">${data.confidences[index]}</td></tr>`;
        });
        table_html += '</table>';
        return table_html;
    }

	function adjustReCaptchaStyle() {
			if (window.innerWidth < 768) {
				// 移动端：移除 grecaptcha-badge 样式
				const styleSheets = document.styleSheets;
				for (let i = 0; i < styleSheets.length; i++) {
					const rules = styleSheets[i].cssRules || styleSheets[i].rules;
					for (let j = 0; j < rules.length; j++) {
						if (rules[j].selectorText === '.grecaptcha-badge') {
							styleSheets[i].deleteRule(j);
							return;
						}
					}
				}
			}
		}

    // 调用函数以根据屏幕宽度调整样式
    adjustReCaptchaStyle();
    window.addEventListener('resize', adjustReCaptchaStyle);

    // 尝试获取 closeButton
    var closeButton = document.querySelector('#closeButton');

    // 检查 closeButton 是否获取成功
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            var popup = document.getElementById('popup');
            if (popup) {
                popup.style.display = 'none';
            }
            location.reload();
        });
    } else {
        console.log('closeButton not found in the DOM');
    }
    function showPopupMessage(message, isError = false) {
        const popup = document.getElementById('popup');
        const responseContent = document.getElementById('responseContent');
        responseContent.innerHTML = `<p style='color: ${isError ? 'red' : 'black'};'>${message}</p>`;
        popup.style.display = 'block';
    }



    // 上传文件的函数
function uploadFile(file, recaptchaToken, modelChoice) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('recaptchaResponse', recaptchaToken);

    // 显示文件上传遮罩和加载指示器
    const overlay = document.getElementById('overlay');
    const fileLoading = document.getElementById('file_loader');
    overlay.style.display = 'block';
    fileLoading.style.display = 'block';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // 隐藏文件上传的加载指示器和遮罩
        overlay.style.display = 'none';
        fileLoading.style.display = 'none';

        if (data.error) {
            // 显示错误信息
            showPopupMessage(data.error, true);
        } else {
            // 显示文件加载成功的消息
            const fileLoaded = document.getElementById('file_loaded');
            fileLoaded.style.display = 'block';
            checkTaskStatus(data.task_id);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // 隐藏文件上传的加载指示器和遮罩，并显示错误信息
        overlay.style.display = 'none';
        fileLoading.style.display = 'none';
        showPopupMessage('An error occurred while uploading.', true);
    });
}

    // Function to handle file selection and upload
    function handleFileUpload() {
        var fileInput = document.getElementById('file-upload');
        var file = fileInput.files[0];
        if (file) {
            grecaptcha.execute('[Your Own Sitekey 4 Google reCHATPCHA]', { action: 'submit' }).then(function(token) {
                uploadFile(file, token);
            });
        }
    }

    // Event listener for the upload button
    var uploadButton = document.getElementById('upload-button');
    if (uploadButton) {
        uploadButton.addEventListener('click', function() {
            handleFileUpload();
        });
    }

    // Function to check task status
    function checkTaskStatus(taskId) {
        // Display overlay and loader
        const fileLoaded = document.getElementById('file_loaded');
        const overlay = document.getElementById('overlay');
        const fileAnalyser = document.getElementById('file_analyser');
        fileLoaded.style.display = 'none';
        fileAnalyser.style.display = 'block';
        overlay.style.display = 'block';

        fetch(`/check-status/${taskId}`)
        .then(response => response.json())
        .then(data => {
	
            if (data.status === 'completed') {
            // Hide overlay and loader after response
            overlay.style.display = 'none';
            fileAnalyser.style.display = 'none';
                window.location.href = `/show-result/${data.result_file_path}`;
            } else if (data.status === 'error') {
            // Hide overlay and loader after response
            overlay.style.display = 'none';
            fileAnalyser.style.display = 'none';
                showPopupMessage(data.error, true);
            } else {
                setTimeout(function() { checkTaskStatus(taskId); }, 5000);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Hide overlay and loader after response
            overlay.style.display = 'none';
            fileAnalyser.style.display = 'none';
            showPopupMessage('An error occurred while checking the status.', true);
        });
    }


});
