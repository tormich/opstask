# Hello

Script to update resources of dockerized
application and run it using docker-compose.

# Requirements

- python3.7
- docker
- docker-compose
- tar

# Usage


```
python3.7 pleasedo.py
```

Use `sudo` if your user is not in the docker group. 

# Flow

- Download tar.gz
- Unpuck it in to `/afolder/ops-exercise/public/images`
- Create `docker-compose.yaml`
- docker-compose build
- docker-compose run
- Check health
- Remove downloaded tar.gz and generated yaml
