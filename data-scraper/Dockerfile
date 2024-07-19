# Use the official Selenium image with Chrome
FROM selenium/standalone-chrome:latest
# Switch to root user to install additional packages
USER root

# Set the working directory
WORKDIR /app

COPY requirements.txt .

# Install any additional packages if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install Python dependencies
RUN pip3 install -r requirements.txt
