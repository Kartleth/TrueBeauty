# TrueBeauty
TrueBeauty is a comprehensive solution designed to streamline appointment and service management for a local beauty salon. Its primary objective is to enhance logistical efficiency and provide valuable statistical insights for administrative purposes. The system incorporates various user roles, each with unique credentials, leveraging the power of a MySQL database for secure data storage and retrieval.
## Requirements
- Python
- Conda
- MySQL 5 or higher
- Docker

## Run These commands to get everything set up

1. Clone the project

```bash
  $ git clone https://Kartleth/TrueBeauty
```

3. Create environment (conda) (If you have Conda, you can skip step 4)

```bash
  $ conda create --name truebeauty python=3.9
  $ conda activate truebeauty
```
4. Install dependecies

```bash
  $ pip install -r requirements.txt
```

## Other commands

Update dependecies

```bash
  $ pip freeze > requirements.txt
```

If you use Docker for enable database for the first time (run mysql_dump file):
```bash
  $ docker-compose up --build
```
Turn it down:
```bash
  $ docker-compose down
```
Turn it back on:
```bash
  $ docker-compose up
```
