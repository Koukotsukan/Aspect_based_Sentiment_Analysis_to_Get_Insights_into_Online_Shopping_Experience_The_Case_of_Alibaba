# Aspect based Sentiment Analysis to Get Insights into Online Shopping Experience: The Case of Alibaba
The study employed the Fast-LCF-ATEPC model for Alibaba reviews, achieving 91.06% APC accuracy and 83.09% ATE F1 score. It revealed mixed user experiences in areas like usability, pricing, and shipping, aiming to enhance Alibaba's e-commerce user satisfaction.

By using PyABSA, Flask, and Javascript, we have successfully finished this project, and it is now online https://aliexperience.online.

*Home Page*

<img alt="Ali-Experience Homepage" style="width:450px;" src="https://github.com/Koukotsukan/Aspect_based_Sentiment_Analysis_to_Get_Insights_into_Online_Shopping_Experience_The_Case_of_Alibaba/blob/main/static/Alibaba%20Experience%20Reviews%20Homepage.png"/>

*Mobile Compatibility*

<img alt="Mobile Compability" style="width:350px;" src="https://github.com/Koukotsukan/Aspect_based_Sentiment_Analysis_to_Get_Insights_into_Online_Shopping_Experience_The_Case_of_Alibaba/blob/main/static/Mobile%20Compability.jpg"/>

*Batch Prediction*

<img alt="Batch Prediction" style="width:450px;" src="https://github.com/Koukotsukan/Aspect_based_Sentiment_Analysis_to_Get_Insights_into_Online_Shopping_Experience_The_Case_of_Alibaba/blob/main/static/batch%20result.png"/>

*Error Handling*

<img alt="Error Handling" style="width:250px;" src="https://github.com/Koukotsukan/Aspect_based_Sentiment_Analysis_to_Get_Insights_into_Online_Shopping_Experience_The_Case_of_Alibaba/blob/main/static/error%20collection.jpg"/>


# 1. Before Installation
Make sure you have a domain, and you have registered Google reCAPTCHA for your domain. So you can obtain your reCAPTCHA sitekey and secret.

# 2. Installation
## Linux Users:
**1.** `cd` into a nice place to put your project. (DO NOT PUT IT IN ROOT DIRECTORY)

**2.** Put the following command to download & install the project
```bash
wget https://raw.githubusercontent.com/Koukotsukan/Aspect_based_Sentiment_Analysis_to_Get_Insights_into_Online_Shopping_Experience_The_Case_of_Alibaba/main/scripts/install.sh && chmod +x install.sh && ./install.sh
```
<small><em>* if you failed to `pip install -r requirements.txt` in the install.sh, you may need to do it manually.</em><small>

**3.** `cd Aspect_based_Sentiment_Analysis_to_Get_Insights_into_Online_Shopping_Experience_The_Case_of_Alibaba-main` folder, run `python3 app.py`.

**4.** Now your server is running on 80 port.

## Windows / Unix / Mac OS Users:
**1.** Download the source code either by using git clone or directly downloading.

**2.** Install [7zip](https://www.7-zip.org/), `cd` the main folder and then, `cd checkpoints/`, then you need to unzip all the zip files. After you get the 3 folders, delete the zip files.

**3.** Open the main folder as a PyCharm project, run the `app.py` to start your journey. The server runs on 80 port, you can change as you want in the `app.py`.

# 3.  Models
The repo only provided the best performance models for Fast-LCF-ATEPC, LCF-ATEPC and BERT-baseline-uncased. If you want all the trained models, due to the size of all the models are too large, I put them on TeraBox, you can download [here](https://terabox.com/s/1NxBufViyj6UzeCBeKQqSwg). After you finish downloading, put all the folders into `checkpoints/` folder.

# 4. Dataset
The [Alibaba Reviews Dataset](https://github.com/Koukotsukan/Alibaba_Reviews_Dataset) is also open-sourced under MIT license. You can use it for any ABSA or NLP tasks.

# 5. Some Findings

### **Comprehensive Report: User Experience on Alibaba**

Based on the provided data, this report aims to provide a comprehensive analysis of user experience on Alibaba, considering various aspects regardless of sentiment.

**App Experience**

The Alibaba app is a significant aspect of user experience, with both positive (170 mentions) and negative (91 mentions) sentiments expressed. Users appreciate the app's ease of use and comprehensive features. However, some users encountered issues with performance, interface, or functionality. This suggests that while the app provides a generally positive experience, there are areas for improvement to enhance user satisfaction.

**Alibaba Platform**

Users generally have a positive view of Alibaba (167 positive mentions), indicating trust in the brand and satisfaction with the services and products offered. However, some users expressed negative sentiments (67 mentions), possibly relating to certain policies, services, or features. This indicates that while Alibaba as a platform is well-received, attention should be given to addressing the concerns raised by users.

**Pricing**

While many users are satisfied with the pricing on Alibaba (87 positive mentions), some users found the prices of some products to be high (47 negative mentions). This suggests that while Alibaba's pricing strategy is generally appreciated, it could be beneficial to review the pricing of certain products to ensure competitiveness.

**Shipping and Delivery**

Users appreciate Alibaba's delivery service, including the speed of delivery, quality of packaging, and communication during the delivery process (70 positive mentions). However, users also expressed dissatisfaction with shipping, including speed, cost, or communication during the shipping process (81 negative mentions). This indicates a need for Alibaba to enhance its shipping and delivery services to improve user satisfaction.

**Service and Communication**

Users commend the services provided by Alibaba, which could range from customer service to after-sales service (152 positive mentions). However, some users had issues with services such as customer service and supplier communication (19 negative mentions for customer service). This suggests that while Alibaba's services are generally appreciated, there is room for improvement in communication and service delivery.

**Conclusion**

Overall, users have a mixed experience on Alibaba. While they appreciate aspects like the app, Alibaba platform, and pricing, they also express concerns about app functionality, shipping services, and communication. By addressing these concerns, Alibaba can further enhance user satisfaction and strengthen its position as a leading e-commerce platform.


# 6. Acknowledgement
Thank you for choosing to use this open-source project! We have adopted the MIT License, which means you are free to use, modify, and distribute this project, as long as you follow these principles:

**1.** **Retain the Copyright Notice**: Please retain the copyright notice and the text of the MIT License in your project to ensure proper attribution and licensing.

**2.** **No Warranty Provided**: Understand that this project is provided "as is" without any express or implied warranties or guarantees. Your use of this project is at your own risk.

**3.** **Respect the Contributors**: If you modify this project or create new work based on it, please respect the original contributors' work and acknowledge the source and contributors in your project.

**4.** **Open Source Spirit**: If you use a portion of this project in your own work, we encourage you to embrace the spirit of open source by sharing your project with the community as open source as well.

By adhering to these principles, you have the opportunity to collaborate with other developers and contribute to the growth of the open-source community. We appreciate your support and respect for the MIT License and hope you enjoy using this project!

**Open-source Software Used (with their respective licenses):**
- [**Flask (BSD License)**](https://github.com/pallets/flask): A lightweight WSGI web application framework.
- [**Celery (BSD License)**](https://github.com/celery/celery): An asynchronous task queue/job queue based on distributed message passing.
- [**PyABSA (MIT License) by Yang Heng**](https://github.com/yangheng95/PyABSA): An efficient and user-friendly implementation for aspect-based sentiment analysis.
- [**Flask-CORS (MIT License)**](https://github.com/corydolphin/flask-cors): A Flask extension for handling Cross-Origin Resource Sharing (CORS). I used it during debugging mode, did not use it in the production.
- [**Transformer Models (Apache License 2.0)**](https://github.com/huggingface/transformers): The core library for Transformer-based models like BERT and DeBERTa.
- [**BERT (Apache License 2.0)**](https://github.com/google-research/bert): Bidirectional Encoder Representations from Transformers for natural language processing tasks.
- [**DeBERTa (MIT License)**](https://github.com/microsoft/DeBERTa): Decoding-enhanced BERT with disentangled attention.
- [**Metric Visualizer (MIT License) by Yang Heng**](https://github.com/yangheng95/metric_visualizer): A tool for visualizing metrics.

**Commercial Software Used (under license):**
- [**Google reCAPTCHA V3**](https://www.google.com/recaptcha): A CAPTCHA system that helps to distinguish human users from automated users.
- [**FontAwesome**](https://fontawesome.com/): An icon set and toolkit for web applications.
- [**Google Sheets**](https://www.google.com/sheets): A web-based spreadsheet program.

<hr>

This project is a Final Year Project conducted by Niu Zhaohang S2001904/1, Undergraduate, Dept. AI, Faculty of Computer Science and Information Technology, Universiti Malaya.

