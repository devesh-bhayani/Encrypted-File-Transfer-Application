from sqlalchemy.orm import sessionmaker
from .models import AuditLog, engine

class AuditLogger:
    """
    Handles logging of audit trails for important application events.
    """
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def log_event(self, action, user_id=None, details=None):
        """
        Logs an event to the audit log.

        :param action: A description of the action being logged.
        :param user_id: The ID of the user performing the action (optional).
        :param details: Additional details about the event (optional).
        """
        session = self.Session()
        try:
            log_entry = AuditLog(
                user_id=user_id,
                action=action,
                details=details
            )
            session.add(log_entry)
            session.commit()
        except Exception as e:
            session.rollback()
            # In a real app, you'd want to handle this more gracefully
            print(f"Error logging event: {e}")
        finally:
            session.close()

# Instantiate a single audit logger for the application
audit_logger = AuditLogger()
