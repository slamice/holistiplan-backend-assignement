import logging
from functools import wraps
from audits.models import AuditLog, CREATE, UPDATE, DESTROY
from django.contrib.auth.models import User
from django.db.models import Model

logger = logging.getLogger(__name__)


def log_action(user: User, model_name: str, model_id: int | None, action: str):
    if not model_id:
        logger.warning(f"Could not log {model_name} {model_id} with action {action}")
    try:
        AuditLog.objects.create(
            user=user,
            model_name=model_name,
            model_id=model_id,
            action=action,
        )
    except Exception as e:
        logger.warning(f"Could not audit log {model_name} {model_id}: {e}")


def get_model_attributes(model: Model):
    return


def audit_log(action: str):
    """A decorator for logging actions."""

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if action == DESTROY:
                model = self.get_object()
                model_id, model_name = model.pk, model.__class__.__name__
            result = func(self, *args, **kwargs)
            if action != DESTROY:
                model_id, model_name = (
                    result.data["id"],
                    self.serializer_class.Meta.model.__name__,
                )
            log_action(
                user=self.request.user,
                model_name=model_name,
                model_id=model_id,
                action=action,
            )
            return result

        return wrapper

    return decorator


audit_log_delete = audit_log(DESTROY)
audit_log_create = audit_log(CREATE)
audit_log_update = audit_log(UPDATE)
