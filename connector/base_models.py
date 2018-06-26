# Third Party Packages
from django.db import models
from django_tools.middlewares import ThreadLocal


class AuditModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, db_column='DJCREATEDDATE')
    modified_date = models.DateTimeField(auto_now=True,
                                         db_column='DJMODIFIEDDATE',
                                         null=True,
                                         blank=True)
    created_by = models.ForeignKey("auth.User",
                                   related_name="created_%(class)s_set",
                                   null=True,
                                   blank=True, db_column='DJCREATEDBY')
    modified_by = models.ForeignKey("auth.User",
                                    related_name="modified_%(class)s_set",
                                    null=True,
                                    blank=True, db_column='DJMODIFIEDBY')
    is_sync = models.BooleanField(default=False, db_column="ISSYNC")

    class Meta:
        abstract = True

    def save_audit_user(self):
        user = ThreadLocal.get_current_user()
        if user and user.is_authenticated():
            if self._state.adding:
                self.created_by = user
            self.modified_by = user

    def save(self, *args, **kwargs):
        self.save_audit_user()
        super(AuditModel, self).save(*args, **kwargs)
