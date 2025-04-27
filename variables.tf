variable "project_id" {
  description = "The Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "The default Google Cloud region"
  type        = string
  default     = "asia-southeast1"  # Singapore region, closest to NZ
}

variable "zone" {
  description = "The default Google Cloud zone"
  type        = string
  default     = "asia-southeast1-a"
} 