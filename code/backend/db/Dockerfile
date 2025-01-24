FROM mysql:8

# Copy the custom shutdown script
COPY custom-shutdown.sh /usr/local/bin/custom-shutdown.sh

# Make the script executable
RUN chmod +x /usr/local/bin/custom-shutdown.sh

# Override CMD to include the custom shutdown script
CMD ["sh", "-c", "trap '/usr/local/bin/custom-shutdown.sh' SIGTERM; docker-entrypoint.sh mysqld"]
