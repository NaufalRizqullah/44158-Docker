FROM python:3.11
ENV HF_PORT=7860

WORKDIR /code

# Expose port 7860 (default huggingface)
EXPOSE ${HF_PORT}

# Install First Dependencies
# "./requirements.txt" path-nya itu berdasarkan Dockerfile yang kita eksekusi (berati sudah di dalam src)
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all files required
# Instruction COPY, will create destination folder (this case "src") if didnt exist.
COPY . /code/src

# make Folder cache and open permission for it
RUN mkdir -p /.cache
RUN chmod 777 /.cache

# cause working dir it set from /code
# and we have code in /code/src
# for running command we user fastapi in "src.main:app"
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]