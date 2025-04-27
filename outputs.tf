output "game_service_url" {
  value       = google_cloud_run_service.game_service.status[0].url
  description = "The URL of the deployed game service"
}

output "storage_bucket_name" {
  value       = google_storage_bucket.game_assets.name
  description = "The name of the storage bucket for game assets"
}

output "vpc_name" {
  value       = google_compute_network.vpc.name
  description = "The name of the VPC network"
} 