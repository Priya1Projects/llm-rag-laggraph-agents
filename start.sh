
#!/bin/bash

# Railway provides the PORT environment variable
# We'll use it for the main service (Streamlit in this case)
export STREAMLIT_PORT=${PORT:-8501}
export FASTAPI_PORT=8000

# Update supervisord config with the correct port
sed -i "s/--server.port 8501/--server.port $STREAMLIT_PORT/g" /etc/supervisor/conf.d/supervisord.conf

# Start supervisor to manage both processes
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf