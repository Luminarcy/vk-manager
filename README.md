# vk-manager
## Setup for development and testing
1. Open folder with your favourite IDE (Pycharm for example).
1. Setup venv.
1. Download all requirements from requirements.txt.
1. Paste your flask app key and vk app service token to config.json.
1. Run.
1. Open http://127.0.0.1:5000/

## Docker Setup
1. Go to the project directory (in where your Dockerfile is, containing your app directory).
1. Build your Flask image: docker build -t myimage .
1. Run a container based on your image: docker run -d --name mycontainer -p 80:80 myimage
1. More info about running vk-manager in Docker can be found here https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask

## Usage
1. Click Get VK user groups
1. Paste user link as https://vk.com/id5 and click Send button.
1. You can view preview and download report as UTF-16 .csv file.
