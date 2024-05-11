# Indicates to Docker that you'd like to use the
# python 3.11 image as a base image for the container.
# A base image gives you a foundation on which to build
# your own image.  For example, python 3.11 gives you a
# Debian OS with Python installed as a starting point.
FROM python:3.11
# This line copies the requirements.txt file into the
# container image.
COPY ./requirements.txt .
# The RUN keyword indicates that the command should
# execute while the image is being built, as opposed to
# CMD which indicates the command should wait until the
# container is initialized before executing.
# Dockerfiles will often contain multiple RUN lines --
# preparing an image by installing dependencies --
# followed by a single CMD line at the very end to start
# the application.
RUN pip install -r requirements.txt

# This line copies the entrypoint.py file into the
# container image.  Because Docker containers run their
# own operating system, they have an entirely different
# file system from the host machine, meaning  if you want
# to access a file on your host machine from the container,
# you must explicitly copy it over.
COPY ./entrypoint.py .

# This line starts up our Flask application using
# Gunicorn, which basically acts as the glue between your
# python code and the container's underlying networking
# infrastructure.
# Upon typing docker build and docker run, you will now
# have a Flask server running in a Docker container.
# The process up to this point has been how to
# containerize an application.
CMD exec gunicorn --bind 0.0.0.0:8000 entrypoint:app

# Instructs Docker to execute our python program when it
# starts up.
### CMD python entrypoint.py
# The CMD keyword specifies the thing you'd like your
# container to actually do.  When the Docker engine
# creates a new container from an image, the container
# immediately executes the CMD you specify.  In this case,
# when we create a container using this image, the
# container will execute the command 'echo "hello world"'
# which prints some text to the console.
### CMD echo "hello world"