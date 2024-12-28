FROM mcr.microsoft.com/mssql-tools

# Copy the restore script
COPY restore.sh /
RUN chmod +x /restore.sh

ENV ACCEPT_EULA=Y

# Run the restore script
CMD ["/restore.sh"]