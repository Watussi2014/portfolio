#!/bin/bash
set -e

echo "Starting database restore process..."

CONNECTION_STRING="$DB_HOST,1433"

# Execute the restore command
echo "Executing restore command..."
TASK_ID=$(/opt/mssql-tools/bin/sqlcmd -S "$DB_HOST" -U "$DB_USER" -P "$DB_PWD" -C -h -1 -Q "
EXEC msdb.dbo.rds_restore_database 
   @restore_db_name='AdventureWorks', 
   @s3_arn_to_restore_from='${BACKUP_FILE_ARN}';")

echo "Restore task ID: $TASK_ID"

# Monitor restore progress in a loop
echo "Monitoring restore progress..."
while true; do
    STATUS=$(/opt/mssql-tools/bin/sqlcmd -S "$CONNECTION_STRING" -U "$DB_USER" -P "$DB_PWD" -h -1 -Q "
    EXEC msdb.dbo.rds_task_status @db_name='AdventureWorks';")
    
    echo "Current status: $STATUS"
    
    if echo "$STATUS" | grep -q "SUCCESS"; then
        echo "Restore completed successfully!"
        break
    elif echo "$STATUS" | grep -q "ERROR"; then
        echo "Restore failed!"
        # Get detailed error status
        /opt/mssql-tools/bin/sqlcmd -S "$CONNECTION_STRING" -U "$DB_USER" -P "$DB_PWD" -Q "
        EXEC msdb.dbo.rds_task_status @db_name='AdventureWorks';"
        exit 1
    elif echo "$STATUS" | grep -q "IN_PROGRESS"; then
        echo "Restore is still in progress..."
    elif [ -z "$STATUS" ]; then
        echo "No status found. Checking if task was created..."
        break
    fi
    
    echo "Waiting 30 seconds before next check..."
    sleep 30
done

echo "Restore process monitoring completed"

