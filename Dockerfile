FROM mambaorg/micromamba:jammy

WORKDIR /workspace
USER root

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get  update --yes --quiet
RUN apt-get install --yes --quiet --no-install-recommends \
    curl ffmpeg git

# configre python to output directly to terminal
# see: https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONUNBUFFERED=1

RUN micromamba install --yes --name base python=3.12 --channel conda-forge
RUN micromamba   clean --yes --all
ARG MAMBA_DOCKERFILE_ACTIVATE=1

RUN pip install "modin[all]" polars pandas

# ARG PINECONE_API
# ENV PINECONE_API=$PINECONE_API
ENV PYDEVD_DISABLE_FILE_VALIDATION=1