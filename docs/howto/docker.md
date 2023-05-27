# Use with docker

If you follow the `mkdocs-material` [tutorial on installation with `docker`](https://squidfunk.github.io/mkdocs-material/getting-started/#with-docker), you will run into an error if you try to add this plugin saying:

> × Building wheel for numpy (pyproject.toml) did not run successfully.

The reason is that the `mkdocs-material` docker image uses the `alpine` image. `mkdocs-table-reader-plugin` depends on [`pandas`](https://pandas.pydata.org/), which depends on [`numpy`](https://numpy.org/), which in turn requires C++ to install, which is not part of the `alpine` image.

If you need a very small image, you can [adapt the alpine image to support numpy](https://stackoverflow.com/questions/33421965/installing-numpy-on-docker-alpine), but you are better off using a more complete docker image like `python-slim`. So you need to build a different docker image.

As an example, below is a `Dockerfile` that is adapted from the [mkdocs-material dockerfile](https://github.com/squidfunk/mkdocs-material/blob/master/Dockerfile). You can use it to create a new Docker image that supports `mkdocs-table-reader-plugin`:

```bash
git clone https://github.com/squidfunk/mkdocs-material.git material-git/
cd material-git
# Manually replace `Dockerfile` with the example below
docker build -t YOUR-CONTAINER-NAME .
# Now, inside your own project, you can use:
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs YOUR-CONTAINER-NAME
```

??? info "Dockerfile"

    ```Dockerfile
    FROM python:3-slim

    # Build-time flags
    ARG WITH_PLUGINS=true

    # Environment variables
    ENV PACKAGES=/usr/local/lib/python3.11/site-packages
    ENV PYTHONDONTWRITEBYTECODE=1

    # Set build directory
    WORKDIR /tmp

    # Copy files necessary for build
    COPY material-git/material material
    COPY material-git/package.json package.json
    COPY material-git/README.md README.md
    COPY material-git/requirements.txt requirements.txt
    COPY material-git/pyproject.toml pyproject.toml

    # Perform build and cleanup artifacts and caches
    RUN \
    apt update \
    && \
    apt install -y \
        libcairo2-dev \
        libfreetype6-dev \
        git \
        libturbojpeg-dev \
        openssh-server \
        zlib1g-dev \
    && \
    apt install -y \
        gcc \
        libffi-dev \
        musl-dev \
    && \
    pip install --no-cache-dir . \
    && \
    if [ "${WITH_PLUGINS}" = "true" ]; then \
        pip install --no-cache-dir \
        "mkdocs-minify-plugin>=0.3" \
        "mkdocs-redirects>=1.0" \
        "pillow>=9.0" \
        "cairosvg>=2.5" \
        "mkdocs-table-reader-plugin" \
        ; \
    fi \
    && \
    for theme in mkdocs readthedocs; do \
        rm -rf ${PACKAGES}/mkdocs/themes/$theme; \
        ln -s \
        ${PACKAGES}/material \
        ${PACKAGES}/mkdocs/themes/$theme; \
    done \
    && \
    rm -rf /tmp/* /root/.cache \
    && \
    find ${PACKAGES} \
        -type f \
        -path "*/__pycache__/*" \
        -exec rm -f {} \;

    # Trust directory, required for git >= 2.35.2
    RUN git config --global --add safe.directory /docs &&\
        git config --global --add safe.directory /site

    # Set working directory
    WORKDIR /docs

    # Expose MkDocs development server port
    EXPOSE 8000

    # Start development server by default
    ENTRYPOINT ["mkdocs"]
    CMD ["serve", "--dev-addr=0.0.0.0:8000"]
    ```
        "mkdocs-table-rea