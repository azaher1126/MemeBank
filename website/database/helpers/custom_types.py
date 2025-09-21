from datetime import datetime, timezone
import sqlalchemy as sa

class TimeStamp(sa.types.TypeDecorator):
    impl = sa.types.DateTime
    cache_ok = True

    def process_bind_param(self, value: datetime, dialect):        
        return value.astimezone(timezone.utc)

    def process_result_value(self, value, dialect):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)