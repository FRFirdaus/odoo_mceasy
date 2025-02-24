import base64

from odoo import api, models, fields, _

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    token = fields.Char(tracking=True)

    @api.model
    def create(self, vals):
        result = super(ResPartnerInherit, self).create(vals)
        
        # we put logic create static token separately to make easier backfill existing partner
        result._create_partner_static_token()
        
        return result

    
    def _create_partner_static_token(self):
        """craete token that will be used for web form partner request"""
        prefix_token = self.env["ir.config_parameter"].sudo().get_param("mceasy.prefix_token_partner", "McEasyPartner")
        token = "%s-%s" % (prefix_token, self.id)
        token_bytes = token.encode()
        token_base64 = base64.b64encode(token_bytes)
        token_base64_str = token_base64.decode()

        self.token = token_base64_str


