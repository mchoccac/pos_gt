# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    bom_extra_ids = fields.One2many('pos_gt.bom_extra_line', 'bom_id', 'BoM Extras', copy=True)

class PosGTExtraLine(models.Model):
    _name = "pos_gt.bom_extra_line"

    def _get_default_product_uom_id(self):
        return self.env['product.uom'].search([], limit=1, order='id').id

    name = fields.Char(string="Nombre", required=True)
    product_id = fields.Many2one("product.product", string="Producto", required=True, domain=[('available_in_pos', '=', True)])
    product_qty = fields.Float("Cantidad", digits=dp.get_precision('Product Unit of Measure'), default=1)
    product_uom_id = fields.Many2one("product.uom", "Product Unit of Measure", default=_get_default_product_uom_id, required=True)
    bom_id = fields.Many2one("mrp.bom", "Parent BoM", index=True, ondelete="cascade", required=True)

    @api.onchange('product_id')
    def product_id_change(self):
        self.name = self.product_id.name
