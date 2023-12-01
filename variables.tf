variable "lambda_timeout"{
    type = number
    default = 10 # seconds

}


variable "memory_size"{
    type = number
    default = 1024 # MB

}


variable "package_type"{
    type = string
    default = "zip"

}


variable "runtime"{
    type = string
    default = "python3.11"

}
