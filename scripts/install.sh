#!/bin/bash

REPO_URL="https://github.com/Koukotsukan/Aspect_based_Sentiment_Analysis_to_Get_Insights_into_Online_Shopping_Experience_The_Case_of_Alibaba"
REPO_ZIP_URL="$REPO_URL/archive/main.zip"
CHECKPOINTS_DIR="Aspect_based_Sentiment_Analysis_to_Get_Insights_into_Online_Shopping_Experience_The_Case_of_Alibaba-main/checkpoints"

# 检查是否已有repo.zip文件
if [ ! -f "repo.zip" ]; then
    echo -e "\e[31mDownloading Aspect_based_Sentiment_Analysis_to_Get_Insights_into_Online_Shopping_Experience_The_Case_of_Alibaba from $REPO_ZIP_URL...\e[0m"
    wget $REPO_ZIP_URL -O repo.zip || { echo -e "\e[31mFailed to download repository.\e[0m"; exit 1; }
fi

echo -e "\e[31mExtracting the repository...\e[0m"
unzip repo.zip || { echo -e "\e[31mFailed to extract repository.\e[0m"; exit 1; }
rm repo.zip

# 检测 Linux 发行版并安装 7-Zip
echo -e "\e[31mDetecting Linux distribution and installing 7-Zip and python3-venv...\e[0m"
if [ -f /etc/debian_version ]; then
    sudo apt-get update && sudo apt-get install -y p7zip-full && sudo apt install python3-venv
elif [ -f /etc/redhat-release ]; then
    sudo yum install -y p7zip p7zip-plugins && sudo yum install python3-virtualenv
elif [ -f /etc/arch-release ]; then
    sudo pacman -Sy p7zip
else
    echo -e "\e[31mUnsupported Linux distribution\e[0m"; exit 1
fi

# 解压分卷文件并删除压缩包
echo -e "\e[31mUnzipping files in $CHECKPOINTS_DIR...\e[0m"
cd $CHECKPOINTS_DIR
7z x '*.zip.001' -y && rm *.zip.* || { echo "Failed to unzip files."; exit 1; }
cd ../..

# 提示用户输入 reCAPTCHA 的 sitekey 和 secret key
read -p "Enter reCAPTCHA sitekey (press Enter to skip): " sitekey
read -p "Enter reCAPTCHA secret key (press Enter to skip): " secretkey

cd Aspect_based_Sentiment_Analysis_to_Get_Insights_into_Online_Shopping_Experience_The_Case_of_Alibaba-main

# 如果提供了 reCAPTCHA secret key，则更新 app.py
if [ ! -z "$secretkey" ]; then
    sed -i "s/\[Your Own Secret 4 Google reCHATPCHA\]/$secretkey/g" app.py
fi

# 如果提供了 reCAPTCHA sitekey，则更新 index.js
if [ ! -z "$sitekey" ]; then
    sed -i "s/\[Your Own Sitekey 4 Google reCHATPCHA\]/$sitekey/g" static/js/index.js
fi

# 创建 Python 虚拟环境
echo -e "\e[31mCreating Python virtual environment...\e[0m"
python3 -m venv venv || { echo "Failed to create virtual environment."; exit 1; }

# 激活虚拟环境
echo "Activating virtual environment..."
source venv/bin/activate

# 安装 requirements.txt 的包
echo "Installing packages from requirements.txt..."
pip install -r requirements.txt || { echo "Failed to install packages. You can manually install by 'pip install -r requuirements.txt"; exit 1; }

echo "if you want help, can type ./install.sh --help to find more information."
echo "Installation completed."



show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  --help             Show help messages"
    echo "  --uninstall        Uninstall the project"
    echo "  -r, --recaptcha    If previously you skipped to input reCAPTCHA sitekey and secret key, you can input here."
}

# 定义卸载函数
uninstall() {
    echo "Uninstalling the repository directory..."
    rm -rf repository-main
    echo "Uninstallation completed."
}

# 定义 reCAPTCHA 更新函数
update_recaptcha() {
    read -p "Enter reCAPTCHA sitekey (press Enter to skip): " sitekey
    read -p "Enter reCAPTCHA secret key (press Enter to skip): " secretkey

    if [ ! -z "$secretkey" ]; then
        sed -i "s/\[Your Own Secret 4 Google reCHATPCHA\]/$secretkey/g" app.py
    fi

    if [ ! -z "$sitekey" ]; then
        sed -i "s/\[Your Own Sitekey 4 Google reCHATPCHA\]/$sitekey/g" static/js/index.js
    fi
}

# 处理输入参数
if [[ $# -eq 0 ]]; then
    echo "no parameter was received, try .install.sh --help"
    exit 1
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help)
            show_help
            exit 0
            ;;
        --uninstall)
            uninstall
            exit 0
            ;;
        -r|--recaptcha)
            update_recaptcha
            exit 0
            ;;
        *)
            echo "Unknown parameter: $1"
            show_help
            exit 1
            ;;
    esac
    shift
done

