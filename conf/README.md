# What is this for?

This folder should be used to store configuration files used by Kedro or by separate tools.

This file can be used to provide users with instructions for how to reproduce local configuration with their own credentials. You can edit the file however you like, but you may wish to retain the information below and add your own section in the section titled **Instructions**.

## Local configuration

The `local` folder should be used for configuration that is either user-specific (e.g. IDE configuration) or protected (e.g. security keys).

> *Note:* Please do not check in any local configuration to version control.

## Base configuration

The `base` folder is for shared configuration, such as non-sensitive and project-related configuration that may be shared across team members.

WARNING: Please do not put access credentials in the base configuration folder.

## Find out more
You can find out more about configuration from the [user guide documentation](https://docs.kedro.org/en/stable/configuration/configuration_basics.html).


# Adding Comments Section
This is my first branch commit

## Instructions for Production Environment Setup

### Prerequisites
1. Install MinIO (for local development):
   ```bash
   # macOS
   brew install minio

   # Or using Docker
   docker run -d \
     -p 9000:9000 \
     -p 9001:9001 \
     --name minio \
     -e "MINIO_ROOT_USER=<your-username>" \
     -e "MINIO_ROOT_PASSWORD=<your-password>" \
     minio/minio server /data --console-address ":9001"
   ```

2. Install MinIO Client (mc):
   ```bash
   brew install minio/stable/mc
   ```

### Setting Up MinIO

1. **Start MinIO Server**:
   ```bash
   minio server ~/minio-data --console-address :9001
   ```

   This will start MinIO with:
   - API endpoint: http://127.0.0.1:9000
   - Web Console: http://127.0.0.1:9001

2. **Configure MinIO Client**:
   ```bash
   mc alias set local http://localhost:9000 <username> <password>
   ```

3. **Create Bucket and Upload Data**:
   ```bash
   # Create the spaceflights bucket
   mc mb local/spaceflights

   # Upload raw data files
   mc cp data/01_raw/companies.csv local/spaceflights/data/01_raw/companies.csv
   mc cp data/01_raw/reviews.csv local/spaceflights/data/01_raw/reviews.csv
   mc cp data/01_raw/shuttles.xlsx local/spaceflights/data/01_raw/shuttles.xlsx
   ```

### Credentials Configuration

Create a `conf/production/credentials.yml` file with your MinIO credentials:

```yaml
minio:
  client_kwargs:
    endpoint_url: http://127.0.0.1:9000
  key: <your-access-key>
  secret: <your-secret-key>
```

**Important**: This file is already in `.gitignore` and will NOT be committed to version control. Contact your team lead for the correct credentials.

### Running the Production Environment

Once MinIO is running and credentials are configured:

```bash
# Run the full pipeline
kedro run --env=production

# Run specific pipelines
kedro run --pipeline=data_processing --env=production
kedro run --pipeline=data_science --env=production
```

### Using Docker

The Docker image is configured to run in production mode by default.

**Important**: Before building the Docker image, create `conf/production/credentials.docker.yml`:

```yaml
minio:
  client_kwargs:
    endpoint_url: http://host.docker.internal:9000
  key: <your-minio-access-key>
  secret: <your-minio-secret-key>
```

Note: Use `host.docker.internal` instead of `localhost` or `127.0.0.1` so the container can reach MinIO on your host machine.

Then build and run:

```bash
# Build the image
docker build -t spaceflights .

# Run the container (requires MinIO to be accessible)
docker run spaceflights
```

### Accessing MinIO Web Console

Visit http://localhost:9001 - credentials will be provided by your team administrator.