FROM mcr.microsoft.com/devcontainers/typescript-node:0-18


FROM python:3.11.2-bullseye

# Add sudo so setup.sh runs correctly
RUN apt-get update && apt-get install -y sudo man vim less

# Update pip
# RUN pip install --upgrade pip

COPY --from=mcr.microsoft.com/devcontainers/typescript-node:0-18 . .

# Install Google Chrome Stable and fonts
# Note: this installs the necessary libs to make the browser work with Puppeteer.
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true
# RUN apt-get install -y chromium

RUN apt-get update && apt-get install gnupg wget -y && \
  wget --quiet --output-document=- https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google-archive.gpg && \
  sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
  apt-get update && \
  apt-get install google-chrome-stable -y --no-install-recommends && \
  rm -rf /var/lib/apt/lists/*

# add build.sh alias to .bashrc
# for some reason source is not a valid command, so use . instead
ARG WORKSPACE
RUN echo alias build=\"bash ${WORKSPACE}/build.sh\" >> ~/.bashrc && . ~/.bashrc
