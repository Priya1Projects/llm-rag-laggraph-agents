
#!/bin/bash


# We'll use it for the main service (Streamlit in this case)
export STREAMLIT_PORT=7860 
export FASTAPI_PORT=7860

# Update supervisord config with the correct port
sed -i "s/--server.port 7860 /--server.port $STREAMLIT_PORT/g" /etc/supervisor/conf.d/supervisord.conf

# Start supervisor to manage both processes
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf