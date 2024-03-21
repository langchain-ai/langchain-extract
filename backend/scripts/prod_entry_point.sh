# -e: fail on any nonzero exit status
# -u: fail if any referenced variables are not set
# -x: print commands before running them
# -o pipefail: fail if a command in a pipe has a nonzero exit code
set -euxo pipefail

# For now just create the db if it doesn't exist
# python -m scripts.run_migrations create

uvicorn server.main:app --host 0.0.0.0 --port 8080 --reload
