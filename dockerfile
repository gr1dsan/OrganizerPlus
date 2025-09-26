FROM python:3.10.11-slim

# Install system dependencies required for Tkinter & GUI support
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    libgl1-mesa-glx \
    libxcb-render0-dev \
    libxcb-shape0-dev \
    libxcb-xfixes0-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy application files into the container
COPY . /app

# Upgrade pip and install Python dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set display environment variable for X11
ENV DISPLAY=:0

# Default command to run your app
CMD ["python", "main.py"]
