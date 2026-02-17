resource "aws_s3_bucket" "example" {
    bucket = "my-bucket"
}

resource "aws_s3_bucket_object" "example" {
    bucket = aws_s3_bucket.example.id
    key    = "example.txt"
    source = "example.txt"
}

output "bucket_name" {
    value = aws_s3_bucket.example.id
}
