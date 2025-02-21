## How to run

### Run everything for testing

```
brew install docker
brew install docker-compose
docker compose up --build
```

### Run python scripts individually
```angular2html
python3 -m venv env-name
source env-name/bin/activate
pip install - r requirements.txt
python3 path/to/file/file.py
```

### Test an API endpoint
```angular2html
python3 -m venv env-name
source env-name/bin/activate
pip install - r requirements.txt
python3 python-server/server.py
```
in a new terminal, to test, for example the api/add-camera endpoint
```angular2html
curl -X POST http://[address]:5000/api/add-camera \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Test Camera",
           "rtsp_url": "tcp://192.168.1.100:554/live"
         }'
```
where you replace [address] with either ```localhost``` or the AWS instance address ```16.171.224.57```


## Training Data
Find information about training data in the [Training README](training/README.md)

## Backend Process
Find information about backend process in the [Process README](process/README.md)

