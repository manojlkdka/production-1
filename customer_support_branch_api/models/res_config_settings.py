# -*- coding: utf-8 -*-
# Part of 10 Orbits. 
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    end_point = fields.Text(string='End-Point Api', 
    help="Api Gateway Support Link")
    
    access_token = fields.Text(string='Access Token', 
    help="Generated Token from the support api")



    def get_access_token_from_support_api(self):
        params = self.env['ir.config_parameter'].sudo()
        return dict(
            end_point=params.get_param('end_point', 
            default=''),
            access_token=params.get_param('access_token', 
            default=''),
            
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(self.get_access_token_from_support_api())
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('end_point', self[0].end_point or '')
        params.set_param('access_token', self[0].access_token or '')
