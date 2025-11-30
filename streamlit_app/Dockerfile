FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy everything inside the build context (streamlit_app)
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Start Streamlit app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]