# https://github.com/devcontainers/images/tree/main/src/python
FROM mcr.microsoft.com/devcontainers/python:3.11

# Add sudo so setup.sh runs correctly
# Also install developer convenience utilities
RUN apt-get update && apt-get install -y sudo man vim less

# add build.sh alias to .bashrc
# for some reason source is not a valid command, so use . instead
# ARG WORKSPACE
# RUN echo alias build=\"bash ${WORKSPACE}/build.sh\" >> ~/.bashrc && . ~/.bashrc