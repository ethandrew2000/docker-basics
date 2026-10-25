# Docker Basics

## Completed app: Dungeon Party Generator

This app creates a party of fantasy adventurers, assigns roles, and rolls six
ability scores per hero by rolling four six-sided dice and discarding the lowest.
It uses the **Rich** pip package to print a character table and Python's `print()`
to display the environment, dice rules, and party summary.

### Build and run

From the repository root, with Docker running:

```sh
docker build -t myapp .
docker run --rm myapp
```

The app prints its party and exits successfully; it needs no input or server port.

### Build argument and environment variable

`APP_ENV` is a Docker build argument whose value becomes the container's `APP_ENV`
environment variable. The app reads it with `os.getenv()` and prints it. Its default
is `development`, so the assignment's basic build command also works.

```sh
docker build --build-arg APP_ENV=production -t myapp-production .
docker run --rm myapp-production
docker run --rm -e APP_ENV=staging myapp-production
```

The last command overrides the saved build value at runtime.

### Choose party size and reproduce a party

```sh
docker run --rm myapp python src/app.py --count 4 --seed 42
```

`--count` accepts 1 through 6 and defaults to 3. Reusing a seed reproduces the party
with the same Python version. Omitting the seed generates a fresh party.

### Tests and Docker verification

```sh
docker run --rm myapp python -m unittest discover -s test -v
```

The [Docker workflow](https://github.com/ethandrew2000/docker-basics/actions/workflows/docker.yml)
builds the image, runs the tests inside it, and verifies default startup, a custom
build argument, runtime environment overrides, repeatable seeded output, and
invalid input. Open a workflow run to see the actual Docker build and run logs.

The Dockerfile copies `requirements.txt` and installs it before copying `src/` and
`test/`, allowing Docker to reuse dependencies when only the app code changes.
`.dockerignore` keeps Git metadata, local environments, and caches out of the build.

To run locally without Docker:

```sh
python -m pip install -r requirements.txt
python src/app.py --seed 42
python -m unittest discover -s test -v
```

The original assignment instructions follow.

## Creating a Dockerfile for a App

In this assignment, you will create a Dockerfile for a small application. Docker allows you to package your application along with its dependencies into a container, making it easy to deploy and run consistently across different environments.


## Step 1: Download and Install Docker

To download and install Docker, follow these steps:

1. Visit the [Docker website](https://www.docker.com/get-started) and download the appropriate version of Docker for your operating system.
1. Run the Docker installer and follow the on-screen instructions to complete the installation process.
1. Once the installation is complete, open a terminal or command prompt and verify that Docker is installed correctly by running the following command:

    ```
    docker --version
    ```

    This should display the version of Docker installed on your system.

Congratulations! You have successfully downloaded and installed Docker on your system. You can now proceed with the rest of the assignment.

## Step 2: Setting up the project

1. Create a new directory for your project: `mkdir src`
1. Create a new file named `app.py` in the `src` directory and code for a small app. Include the following in your app:
    * Uses at least 1 pip package in the app. This can be flask or any other pip package you want to experiment with.
    * References at least 1 environment variable and uses that variable in the code:
        ```python
        import os

        app_env = os.getenv("APP_ENV")

        # Your code here that uses the app_env variable
        ```
    * Uses python `print()` function to print something interesting to the console.

## Step 3: Creating the Dockerfile

1. In the project directory, create a new file named `Dockerfile` (without any file extension).
1. Open the `Dockerfile` and add docker code to run your new app. The Docker file should have the following:
    * A layer that pip installs the requirements file
    * A layer that copies the rest of your code.
    * A layer that adds an environment variable that requires a build argument

Make sure that your layer order makes sense for this dockerfile (ie install your pip requirements before you add the rest of your code files)

## Step 4: Building and running the Docker image

1. Open a terminal and navigate to the project directory.
1. Build the Docker image using the following command: `docker build -t myapp .`
1. Once the image is built, run the container using the following command: `docker run myapp`

Congratulations! You have successfully created a Dockerfile for a small application and ran it in a Docker container. This allows you to easily package and deploy your app in a consistent and reproducible manner.

Feel free to explore more Docker features and experiment with different configurations to enhance your app deployment.

## Step 5: Submitting your Dockerized App

Once you have completed all the steps and have successfully created and run your Dockerized app, it's time to submit your work. Here are the steps to follow:

1. Make sure all your code changes are saved and committed.
1. Push your local repository to GitHub.
1. Share the link to your GitHub repo.
