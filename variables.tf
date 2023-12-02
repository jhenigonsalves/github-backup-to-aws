variable "lambda_timeout" {
  description = "Lambda timeout in seconds"
  type    = number
  default = 10
}


variable "memory_size" {
  description = "Lambda memory size in MB"
  type    = number
  default = 1024
}


variable "package_type" {
  description = "Lambda package type. Valid values are Zip or Image"
  type    = string
  default = "Zip"
}


variable "runtime" {
  description = "Lambda Runtime. Valid values are python3.11, python3.8, python3.7, python3.6, python2.7, nodejs14.x, nodejs12.x, nodejs10.x, nodejs8.10, java11, java8.al2, java8, java11.al2, dotnetcore3.1, dotnetcore2.1 ..."
  type    = string
  default = "python3.11"
}
