FROM python:3.12-slim
WORKDIR /app
# Install pinned dependencies for scientific computing and stats
RUN pip install --no-cache-dir \
    numpy==2.2.5 \
    scipy==1.15.3 \
    pandas==2.2.3 \
    statsmodels==0.14.4
# Create directory structure
RUN mkdir -p /app/data /app/results /app/solution /app/tests
COPY environment/data/ /app/data/
COPY solution/ /app/solution/
COPY tests/ /app/tests/
RUN chmod +x /app/solution/solve.sh /app/tests/test.sh
