from django.db import models

UPDATE = "UPDATE"
CREATE = "CREATE"
DESTROY = "DESTROY"
API_ACTIONS = (UPDATE, CREATE, DESTROY)
ACTIONS = sorted([(item[1][0], item[0]) for item in API_ACTIONS])
MODEL_NAMES = [("Snippet", "SNIPPETS"), ("User", "USERS")]


class AuditLog(models.Model):
    user = models.ForeignKey(
        "auth.User", related_name="audit_logs", on_delete=models.CASCADE
    )
    model_name = models.CharField(max_length=100, null=False, choices=MODEL_NAMES)
    model_id = models.IntegerField(null=False)
    action = models.CharField(choices=ACTIONS, max_length=10, null=False)
    action_taken_on = models.DateTimeField(auto_now_add=True)
