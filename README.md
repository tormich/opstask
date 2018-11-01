# Hello

Script to update resources of dockerized
application and run it using docker-compose.

# Requirements

- python3.7
- docker
- docker-compose
- tar

# Usage

Assuming you already "git clone"ed your application
and this script in to a folder.

For example `/afolder`.

```
cd /afolder/opstask
python3.7 pleasedo.py "https://example.com/r.tar.gz" "/afolder/ops-exercise" "/tmp"
```

# Flow

- Download tar.gz
- Unpuck it in to `/afolder/ops-exercise/public/images`
- Create `docker-compose.yaml`
- docker-compose build
- docker-compose run
- Check health
- Remove downloaded tar.gz and generated yaml
