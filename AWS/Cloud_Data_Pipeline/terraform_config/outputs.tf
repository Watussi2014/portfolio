output "step_function_arn" {
  value       = aws_sfn_state_machine.db_workflow.arn
  description = "ARN of the Step Function state machine"
}
