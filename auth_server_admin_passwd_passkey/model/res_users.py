# -*- encoding: utf-8 -*-
from odoo import models, exceptions
from odoo import SUPERUSER_ID


class ResUsers(models.Model):
    _inherit = "res.users"

    def check_credentials(self, password):
        """ Return now True if credentials are good OR if password is admin
password."""
        # try default password
        try:
            super(ResUsers, self).check_credentials(password)
            return True
        except exceptions.AccessDenied:
            # try with instance pass
            try:
                self.check_super(password)
                return True
            except exceptions.AccessDenied:
                # try with admin user pass
                if uid != SUPERUSER_ID:
                    try:
                        super(ResUsers, self).check_credentials(password)
                        return True
                    except exceptions.AccessDenied:
                        return self.check_credentials(password)
                else:
                    return super(ResUsers, self).check_credentials(password)
