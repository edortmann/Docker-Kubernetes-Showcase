FROM python:3.10-slim
WORKDIR /opt/ui
COPY src/translator_ui translator_ui
RUN pip install --no-cache-dir streamlit requests

# ---------- create user & set HOME ---------------------------
ARG APP_UID=10001
ARG APP_GID=10001
RUN groupadd --gid $APP_GID app && \
    useradd  --uid $APP_UID --gid $APP_GID --create-home --home-dir /opt/ui app && \
    chown -R app:app /opt/ui

ENV HOME=/opt/ui \
    XDG_CACHE_HOME=/opt/ui/.cache \
    PYTHONUNBUFFERED=1

USER app

EXPOSE 8501
CMD ["streamlit", "run", "translator_ui/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
