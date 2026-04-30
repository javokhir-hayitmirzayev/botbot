#!/bin/bash
set -e

# This script will be run by the PostgreSQL container's entrypoint
# It will be executed after the database is initialized but before it starts accepting connections

# The actual database initialization will be handled by scripts in /docker-entrypoint-initdb.d/
# This is just a wrapper to ensure the entrypoint chain works correctly

# Call the original entrypoint with all arguments
exec /usr/local/bin/docker-entrypoint.sh "$@"
