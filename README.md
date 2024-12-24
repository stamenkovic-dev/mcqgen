1. login to the AWS
2. search EC2 instances
3. configure UBUNTU machine
4. lunch the instance
5. go to security and add the inbound rule and add port 8501
6. update the machine
    sudo apt update
    sudo apt-get updated
    sudo apt upgrade -y
    sudo apt install git curl unzip tar make sudo vim wget python3-venv python3-full -y
    git clone "your repository"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
7. python3 -m streamlit run StreamlitAPP.py

##### for adding openai api key
1. create .env file in your server
touch .env
vi .env
#copy your api key
#:wq

