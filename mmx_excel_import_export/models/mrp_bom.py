from asteval import Interpreter
from odoo import models, _
from odoo.exceptions import ValidationError
from odoo.http import request

CHINESE_TO_UOM_XML_IDS = {
    "PCS": "uom.product_uom_unit",
    "G": "uom.product_uom_gram",
    "瓶": "mmx_excel_import_export.product_uom_bottle",
    "支": "mmx_excel_import_export.product_uom_bottle",
    "套": "mmx_excel_import_export.product_uom_set",
}


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @classmethod
    def excel_import_pre_hook(cls, field, value, row_data=None):
        if field == "product_tmpl_id":
            product = request.env["product.product"].search(
                [("default_code", "=", value)]
            )
            if not product:
                raise ValidationError(_("Product not found: %s") % value)
            value = product[0].product_tmpl_id.display_name
        elif field == "bom_line_ids/product_id":
            product = request.env["product.product"].search(
                [("default_code", "=", value)]
            )
            if product:
                value = product[0].product_tmpl_id.display_name
            else:
                name = row_data[5]
                uom_id = None
                uom = row_data[9]
                if uom != "PCS":
                    if uom in CHINESE_TO_UOM_XML_IDS:
                        uom_id = request.env.ref(CHINESE_TO_UOM_XML_IDS[uom]).id
                    else:
                        raise ValidationError(_("UOM not found: %s") % uom)
                else:
                    uom_id = request.env.ref("uom.product_uom_unit").id
                value = (
                    request.env["product.product"]
                    .create(
                        {
                            "default_code": value,
                            "name": name,
                            "detailed_type": "product",
                            "sale_ok": False,
                            "uom_id": uom_id,
                            "uom_po_id": uom_id,
                        }
                    )
                    .product_tmpl_id.display_name
                )
                # .product_tmpl_id.display_name
                # Otherwise product won't be saved
                request.env.cr.commit()
        elif field == "bom_line_ids/product_qty":
            aeval = Interpreter()
            value = aeval.eval(str(value))

        return value
