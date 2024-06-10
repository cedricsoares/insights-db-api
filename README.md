# insights-db-api
Used api to connect to a database in order to in ingest Pages, Videos, Video Insight.



### Context

This api has been designed to suits purpose of recordings informations about data from social networks and video plateforms about pages, videos and video insights.  This projet was developpement to fullfill

The goal of this projet is mostly to provide a tested API in order to record data in a sqlite database assess a technical test in an hiring processes.

#### Questions to adresse

1. create page with name OurMedia France
2. create a video A and a video B of page Brut France
3. create an insight for video A and and insight video B
4. delete video B
5. The created database is a transactional database (OLTP). Create a simple architecture schema that illustrates a solution to create an analytics database (OLAP) on Google Cloud Cloud platform that is synchronized with the OLTP db.

### Specifications

#### Pages

A page has the following characteristics:
- `created_at`: the timestamp of creation of the page
- `id`: unique identifier of the page
- `name`: page name

#### Videos

A video has the following characteristics:
- `created_at`: the timestamp of creation of the video
- `id`: unique identifier of the video
- `title`: title of the video
- `page_id`: id of the page where the video was published

#### Video Insights

A video insight has the following characteristics:
- `created_at`: the timestamp of creation of the video insight
- `id`: unique identifier of the video insight
- `video_id`: id of the video
- `likes`: number of likes of the video
- `views`: number of views of the video


### Getting Started

#### Prerequisites

Ensure you have the following installed:
- Python 3.10
- Poetry 1.8.3

#### Setup

The best way to lauch the api localy would be to use Docker. But it stills have some database inizialisation issue with the Dockerfile.

1. Clone the repository from GitHub:
    using HTTPS:
        ```bash
        git clone https://github.com/cedricsoares/insights-db-api.git
        ```

    or using ssh
     ```bash
        git clone git@github.com:cedricsoares/insights-db-api.git
    ```

    then go the cloned local files:
    ```bash
        cd insights-db-api
    ```

2. Install poetry :
    Poetry is a powerfull environement / package manager that lowers risks on dependencies mnagement and multi envs.

    To insall poetry use the bash command (works with MacOS, Linux, Windows):
    ``bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```


3. Install the required dependencies:
    ```bash
    poetry install
    ```

4. Initialize the database:
    ```bash
    poetry run python init_db.py
    ```

5. Run the Flask application:
    ```bash
    poetry run python -m app.py
    ```

6. OpenAPI documentation is available in different formats:
    If you run the projet locally it will be available at :
     ```bash
        http://127.0.0.1:5000/openapi
    ```


### Usage

Follow these steps to execute tasks 1 to 4:
    every task can be achived via the apoenapi documentation user interface, a curl query or an API client like Postman.
    Below you are the curl queries to fullfil the tasks:

1. **Create a page "OurMedia France":**
    ```bash
    curl -X POST http://127.0.0.1:5000/page -H "Content-Type: application/json" -d '{"id": 1, "name": "OurMedia France"}'
    ```

2. **Create videos "A" and "B" for the page "Brut France":**
    First of all Brut France is not yet stored in the pages table. So to ensure foreign key constraints we need to create à new page for Brut France

    ```bash
    curl -X POST http://127.0.0.1:5000/page -H "Content-Type: application/json" -d '{"id": 2, "name": "Brut France"}'

    Then, you can add the videos
    ```
    ```bash
    curl -X POST http://127.0.0.1:5000/video -H "Content-Type: application/json" -d '{"id": 1, "page_id": 2, "title": "Video A"}'
    curl -X POST http://127.0.0.1:5000/video -H "Content-Type: application/json" -d '{"id": 2, "page_id": 2, "title": "Video B"}'
    ```

3. **Create insights for videos "A" and "B":**
    ```bash
    curl -X POST http://127.0.0.1:5000/video_insight -H "Content-Type: application/json" -d '{"id": 1, "video_id": 1, "likes": 100, "views": 1000}'
    curl -X POST http://127.0.0.1:5000/video_insight -H "Content-Type: application/json" -d '{"id": 2, "video_id": 2, "likes": 50, "views": 500}'
    ```

4. **Delete video "B":**
    ```bash
    curl -X DELETE http://127.0.0.1:5000/video/2
    ```

### Testing

Run the tests using pytest:

1. Install pytest if you haven't already:
    ```bash
    poetry add --dev pytest
    ```

2. Run the tests:
    ```bash
    poetry run pytest test_app.py
    ```

### Remarks

Projets is provided with a bunch of tools to facilitate collaboration in a team context:
- On Github two CI worflows are implemented: One to run linters on Dockerfile, Python and SQL and to run unit tests, the second to push Docker builder image on DockerHub.
- For local purpose a pre-commit configuration YAML file is provides to run linters and unit tests before each commit
- Project was developped in a vscode dev container. Config files might also be commited on Github

### Deploying developped soliution using Google Cloud Platform

A final purpose of the project would be to deploy the solution GCP. A good choice to deploy API could Cloud Endpoints.
For the OLTP might be Cloud SQL.

For OLAP database the best option option is Bigquery.

To sync both I have two solutions to propose:

First the efforthless in terms of configuration: using federated queries. The solution tends to be effortless but is not the faster solution to answer the need.

On GCP, Google provides a dedicated "near to real time" Charge Data Capture solution: Datastream

The schema below illustrates a solution to create an analytics database (OLAP) on Google Cloud Platform that is synchronized with the OLTP database.

![OLAP Architecture](olap_architecture.png)
