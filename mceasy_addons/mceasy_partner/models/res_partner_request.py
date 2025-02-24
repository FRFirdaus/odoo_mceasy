from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class ResPartnerRequest(models.Model):
    _name = 'res.partner.request'
    _order = 'create_date desc'
    _description = 'Partner Update Request'

    partner_id = fields.Many2one('res.partner', required=True)
    state = fields.Selection([
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected")
    ])

    name = fields.Char()
    address = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    zip = fields.Char()

    reject_reason = fields.Text()

    def action_approve_request(self):
        """
        Action to approve request changee to res.partner data
        """
        self.partner_id.write({
            "name": self.name,
            "street": self.address,
            "email": self.email,
            "phone": self.phone,
            "zip": self.zip,
        })

        self.write({
            "state": "approved"
        })
    
    def action_reject_request(self):
        if not self.reject_reason:
            raise ValidationError(_("You need to define reject reason first before reject this change request"))

        self.write({
            "state": "rejected"
        })
