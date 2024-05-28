data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

###############
#    IAM      #
###############
data "aws_iam_policy_document" "lambda" {
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:*:*:*"
    ]
  }
}

###############
#   Lambda    #
###############
data "archive_file" "python_lambda_package" {
  type        = "zip"
  source_file = "${path.module}/src/handler.py"
  output_path = "lambda.zip"
}