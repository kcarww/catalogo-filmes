from uuid import uuid4
from django.db import models

from core.cast_member.domain.cast_member import CastMemberType

class CastMember(models.Model):
    app_label = "cast_member_app"
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=64, choices=[(tag.name, tag.value) for tag in CastMemberType])
    
    class Meta:
        db_table = "cast_member"
        
    def __repr__(self):
        return str(self.name)