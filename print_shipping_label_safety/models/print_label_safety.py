# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class StockPickingBatchInherit(models.Model):
    _inherit = "stock.picking.batch"


    # this field toggle the grey out of validate button 
    is_label_printed = fields.Boolean(string="Label Printed", default=False)

    # this function removes grey of validate button after clicked
    def prepare_shipping_labels(self):
        result = super(StockPickingBatchInherit, self).prepare_shipping_labels()
        self.is_label_printed = True
        return result

    # this function triggers warning if validate button is clicked first
    def action_done(self):
        if not self.is_label_printed:
            raise ValidationError(_("You must print the shipping label first"))
        else:
            return super(StockPickingBatchInherit, self).action_done()
