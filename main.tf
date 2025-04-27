terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Create VPC
resource "google_compute_network" "vpc" {
  name                    = "nz-adventure-vpc"
  auto_create_subnetworks = false
}

# Create Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "nz-adventure-subnet"
  ip_cidr_range = "10.0.0.0/24"
  network       = google_compute_network.vpc.id
  region        = var.region
}

# Cloud Run service for the game server
resource "google_cloud_run_service" "game_service" {
  name     = "nz-adventure-game"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/nz-adventure:latest"
        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Allow unauthenticated access to Cloud Run service
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.game_service.name
  location = google_cloud_run_service.game_service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Cloud Storage bucket for game assets and state
resource "google_storage_bucket" "game_assets" {
  name          = "${var.project_id}-game-assets"
  location      = "ASIA-SOUTHEAST1"  # Closest to NZ for lower latency
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
  
  versioning {
    enabled = false  # Save costs by disabling versioning
  }
}

# Firestore database for game state
resource "google_firestore_database" "game_db" {
  name                        = "(default)"
  location_id                 = "asia-southeast1"  # Closest to NZ
  type                       = "FIRESTORE_NATIVE"
  concurrency_mode           = "OPTIMISTIC"
  app_engine_integration_mode = "DISABLED"
} 