FROM python:3.11.2-bullseye

# Add sudo so setup.sh runs correctly
RUN apt-get update && apt-get install -y sudo

# Update pip
RUN pip install --upgrade pip

# add build.sh alias to .bashrc
# for some reason source is not a valid command, so use . instead
ARG WORKSPACE
RUN echo alias build=\"bash ${WORKSPACE}/build.sh\" >> ~/.bashrc && . ~/.bashrc