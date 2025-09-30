
# Use Microsoft's official Playwright image with Python pre-installed
# - Includes browsers (Chromium, Firefox, WebKit) and drivers needed for Playwright
# - "noble" = Ubuntu 24.04 base
FROM mcr.microsoft.com/playwright/python:v1.54.0-noble

# Install pytest-playwright plugin
# - Adds Playwright integration with pytest (lets you write/play tests easily)
RUN pip install pytest-playwright

# Ensure browsers and dependencies are installed inside the container
# - This makes sure Chromium, Firefox, and WebKit are ready to use
RUN playwright install

# Copy your test file(s) into the container
# - Takes test_home.py from your host machine and places it into /home inside the container
COPY ./test_home.py /home

# Set the working directory
# - Any following commands (like pytest) will run from /home
WORKDIR /home

# Default command when container starts
# - Runs pytest, which will discover and execute test_home.py

CMD ["pytest", "-s", "-v"]