from odoo import http
from odoo.http import request

class CompanyUpdateController(http.Controller):

    @http.route('/update-profile-company/<string:token>', type='http', auth='public', website=True)
    def update_form(self, token, **kwargs):
        """Render the company update form if the token is valid."""
        partner = request.env['res.partner'].sudo().search([('token', '=', token)], limit=1)

        if not partner:
            return request.render('mceasy_partner.invalid_token_page')

        # Check if there's a pending request
        existing_request = request.env['res.partner.request'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'pending')
        ], limit=1)

        if existing_request:
            return request.render('mceasy_partner.pending_request_page')

        return request.render('mceasy_partner.company_update_form_page', {'partner': partner})

    @http.route('/submit-company-update', type='http', auth='public', methods=['POST'], csrf=False)
    def submit_update(self, **post):
        """Handles submission of the update form."""
        token = post.get('token')
        partner = request.env['res.partner'].sudo().search([('token', '=', token)], limit=1)

        if not partner:
            return request.render('mceasy_partner.invalid_token_page')

        # Check for pending requests
        existing_request = request.env['res.partner.request'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'pending')
        ], limit=1)

        if existing_request:
            return request.redirect('/update-profile-company/pending')

        # Create a new request for staff approval
        request.env['res.partner.request'].sudo().create({
            'partner_id': partner.id,
            'name': post.get('company_name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            "address": post.get('address'),
            "zip": post.get("zip"),
            'state': 'pending',
        })

        return request.redirect('/update-profile-company/success')

    @http.route('/update-profile-company/success', type='http', auth='public', website=True)
    def success_form(self, **kwargs):
        """handles if form is submitted and success"""
        return request.render('mceasy_partner.company_update_success_page')
    
    @http.route('/update-profile-company/pending', type='http', auth='public', website=True)
    def pending_form(self, **kwargs):
        """handles if form is submitted and penidng"""
        return request.render('mceasy_partner.pending_request_page')