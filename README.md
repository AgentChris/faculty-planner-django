# Faculty planner

Aggregation and distribution of ubb faculties planners data

## Setup Instructions:
Both environments can be used for local development

1. [Dockerized](#dockerized)
2. [Local](#local)

## Dockerized

#### Start all the services:
```bash
docker-compose -f docker-compose-dev.yaml up
```

## Local

#### Step 1: Build the app
```bash
make
```

#### Step 2: Activate the virtualenv
```bash
source venv/bin/activate
```

#### Step 3: Run the server

```bash
python manage.py runserver
```

## API documentation
We plan on using swager

## Architecture Documentation
We are using the ADR: https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records
