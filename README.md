# butena
## How to use

> Requirements
1. python3.12
2. install the requirements

Clone repo 
```bash
git clone https://github.com/Vortexdude/butena
```
Navigate to project directory - 
```bash
cd butena
```
create and activate the virtual environment  
```bash
python3 -m venv venv
source venv/bin/activate
```

install the requirements  
```bash
pip3 install -r requirements.txt
```

run the server  
```bash
python3 app/server.py
```

```yaml
version: '3'
services:
  api:
    build:
      context: .
    container_name: butena-api
    env_file:
      - .env
    environment:
      PORT: 8000
    ports:
      - '8000:8000'
    restart: always
    depends_on:
      - mongodb

  mongodb:
    image: mongo
    container_name: mongodb
    ports:
      - "27017:27017"

  mongo-express:
    image: mongo-express
    restart: always
    ports:
      - 8081:8081
    environment:
      ME_CONFIG_MONGODB_URL: mongodb://mongodb:27017/






```