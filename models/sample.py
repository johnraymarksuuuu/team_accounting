from odoo import models, fields, api
class SaleCustom(models.Model):
   _name = 'sale.custom'
   @api.model
   def get_sale_order(self):
       ret_list = []
       req = (
                   "SELECT sale_order.name, rp.name AS customer, sale_order.amount_total, sale_order.state "
                   "FROM sale_order "
                   "Join res_partner rp ON (sale_order.partner_id=rp.id)")
       self.env.cr.execute(req)
       for rec in self.env.cr.dictfetchall():
           ret_list.append(rec)
       return ret_list