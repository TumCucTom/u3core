## [Deploy Frontend](deploy-frontend.yml)
We need to install dependencies and build into website files:
```angular2html
cd code/frontend/web-app
npm install && npm install --only=dev
npm install @quasar/cli
npx quasar build
```
### Build to gh-pages
Deploy to github pages:
```angular2html
- name: Deploy 🚀
    uses: JamesIves/github-pages-deploy-action@v4
    with:
      folder: code/frontend/web-app/dist/spa # The folder the action should deploy.
```
### Deploy to domain
We then need to use FTP to give the website files to our website hoster
```angular2html
name: Deploy via FTP
    uses: SamKirkland/FTP-Deploy-Action@4.3.0
    with:
      server: ftp.u3core.com
      username: ai@u3core.com
      password: ${{ secrets.FTP_PASSWORD }}
      local-dir: ./
      server-dir: ./
```

## [Deploy Backend](deploy-backend.yml)
### SSH into the AWS instance
```angular2html
mkdir -p ~/.ssh
echo "${{ secrets.AWS_SSH_KEY }}" | tr -d '\r' > ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa
ssh-keyscan -H github.com >> ~/.ssh/known_hosts
ssh-keyscan -H ${{ secrets.AWS_HOST }} >> ~/.ssh/known_hosts
```
Here we are also telling the AWS instance that Githuh.com should be a known host so that we can git clone.
### Install git
```angular2html
set -e  # Exit on any error
sudo yum update && sudo yum install -y git  # Ensure git is installed
```
### Clone the repo and remove old code
```angular2html
# Navigate to home directory and remove any existing repo
cd ~
rm -r 2024-MLAIPredictionMicroservices

# Clone the latest version
git clone git@github.com:spe-uob/2024-MLAIPredictionMicroservices.git
cd 2024-MLAIPredictionMicroservices/code/backend
```
### Run the docker container for the backend server
```angular2html
# Start the service using Docker Compose
docker compose down
docker compose pull
docker compose up -d --build
```
This is also taking down the old docker container
## [Python Build](pybuild.yml)
### Install dependencies
```angular2html
sudo apt-get update && sudo apt-get install -y libcurl4-openssl-dev
python -m pip install --upgrade pip
pip install flake8
pip install -r code/frontend/requirements.txt
pip install -r code/backend/requirements.txt 
```
### First lint
```angular2html
# stop the build if there are Python syntax errors or undefined names
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

### Run tests
#### Install additional dependencies
```angular2html
pip install pytest pytest-cov pytest-html
```
#### Run tests
```angular2html
pytest test/ --doctest-modules --cov=com --cov-report=xml --cov-report=html --maxfail=5 --disable-warnings
```
#### Log coverage
```angular2html
uses: codecov/codecov-action@v3
    with:
        file: coverage.xml 
```
## [Python Linting](pylint.yml)

Runs linting on all python scripts. We first have to install dependencies:
```angular2html
sudo apt-get update && sudo apt-get install -y libcurl4-openssl-dev
python -m pip install --upgrade pip
pip install pylint
pip install -r code/frontend/requirements.txt
pip install -r code/backend/requirements.txt
```

### Feature Scripts
We then run:
```angular2html
pylint $(git ls-files 'code/backend/python-features/*.py') --rcfile=.github/workflows/.pylintrc
```
Which will lint the relevant files
### Server scripts
We then run:
```angular2html
pylint $(git ls-files 'code/backend/python-server/*.py') --rcfile=.github/workflows/.pylintrc
```
Which will lint the relevant files

## [Web App](webApp.yml)

Runs linting on the frontend server. The main functions runs are:
```angular2html
npm --prefix code/frontend/web-app ci
npm --prefix code/frontend/web-app run build
npm --prefix code/frontend/web-app run lint
```
This install dependencies, builds the application then lints