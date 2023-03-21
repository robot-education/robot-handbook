FROM python:3.11.2-bullseye

# Add sudo so setup.sh runs correctly
RUN apt-get update && apt-get install -y sudo man vim less

# Update pip
RUN pip install --upgrade pip