# Use a Python base image.
FROM python:3.9

# Set the working directory.
WORKDIR /app

# Copy the application files to the container.
COPY . /app

# Installs dependencies.
RUN pip install -r requirements.txt

# Exposes the port on which the application will run.
EXPOSE 8501

# Command to run the Streamlit application.
CMD ["streamlit", "run", "app.py"]
