FROM gitpod/workspace-postgres

RUN curl https://cli-assets.heroku.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python3", "main.py"]
