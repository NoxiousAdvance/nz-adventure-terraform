# New Zealand Adventure Game Infrastructure

This Terraform configuration sets up the infrastructure for a text-based adventure game inspired by Zork, set in New Zealand. The infrastructure is hosted on Google Cloud Platform using cost-effective services.

## Architecture

The infrastructure consists of:
- Cloud Run service for the game server
- Cloud Storage bucket for game assets
- Firestore database for game state
- VPC network and subnet for security
- IAM configurations for secure access

## Prerequisites

1. Google Cloud Platform account
2. Google Cloud SDK installed
3. Terraform installed (version 1.0.0 or later)
4. A Google Cloud Project with billing enabled

## Setup Instructions

1. Initialize the project:
   ```bash
   terraform init
   ```

2. Create a `terraform.tfvars` file with your project ID:
   ```hcl
   project_id = "your-project-id"
   ```

3. Plan the deployment:
   ```bash
   terraform plan
   ```

4. Apply the configuration:
   ```bash
   terraform apply
   ```

## Cost Optimization

This infrastructure is designed to be cost-effective:
- Uses serverless Cloud Run for the game server
- Standard storage class for game assets
- Firestore in native mode for game state
- Disabled versioning on storage bucket
- Region selection optimized for New Zealand users (asia-southeast1)

## Maintenance

To update the infrastructure:
1. Make changes to the Terraform files
2. Run `terraform plan` to review changes
3. Run `terraform apply` to apply changes

To destroy the infrastructure:
```bash
terraform destroy
```

## Security

- VPC network isolation
- Cloud Run service with public access but controlled endpoints
- Uniform bucket-level access enabled for Cloud Storage
- Firestore with optimistic concurrency control 