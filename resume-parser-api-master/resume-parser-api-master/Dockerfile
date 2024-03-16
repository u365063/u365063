# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir  flask
RUN pip install --no-cache-dir  flask_restful
RUN pip install --no-cache-dir  analyzer
RUN pip install --no-cache-dir  fileReader
RUN pip install --no-cache-dir  pandas
RUN pip install --no-cache-dir  nltk
RUN pip install --no-cache-dir  tika
RUN pip install --no-cache-dir  scikit-learn
# Expose the Flask app port
EXPOSE 5000
# Run python script to generate the image
CMD ["python", "app.py"]


