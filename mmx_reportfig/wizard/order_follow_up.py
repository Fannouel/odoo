import logging
from odoo import models, fields, api, _


class OrderFollowUpWizard(models.TransientModel):
    _name = "order.follow.up.wizard"
    _description = "Report Wizard for order follow up"

    sale_order_id = fields.Many2one('sale.order', string=_("Sale Order"))
    html = fields.Html(
        string="HTML"
    )

    @api.onchange("sale_order_id")
    def action_generate_report(self):
        html = "<table class=\"table-bordered\">"
        html += """<tr>
            <th>N°Fab</th>
            <th>Code</th>
            <th>Designation</th>
            <th>Qte command</th>
            <th>Client</th>
            <th>Urgence</th>
            <th>Fonderie</th>
            <th>Ebarbage</th>
            <th>Soudure</th>
            <th>Souscouche</th>
            <th>Peintre</th>
        </tr>
        """

        qty_mapping = {}  # Create a dictionary to store rows grouped by 'production_id', 'product_qty', 'workcenter_name', and 'product_id'

        if self.sale_order_id:
            suivie_command = self.env['reportfig.reportfig'].search(
                [('sale_order_id', '=', self.sale_order_id.id)])
            for reportfig_reportfig in suivie_command:
                production_id = reportfig_reportfig.production_id.name
                product_qty = reportfig_reportfig.product_qty
                workcenter_name = reportfig_reportfig.workcenter_id.name.upper()  # Convert to uppercase
                product_id = reportfig_reportfig.product_id.default_code
                qty = reportfig_reportfig.qty
                partner_name = reportfig_reportfig.partner_id.name
                urgence_name = reportfig_reportfig.Urgence
                product_name = reportfig_reportfig.product_id.name

                # Create a unique key for grouping
                key = (production_id, product_id, product_name)

                # Check if the key already exists in the dictionary
                if key in qty_mapping:
                    # Add qty to the respective workcenter in the existing dictionary
                    if workcenter_name not in qty_mapping[key]["qty"]:
                        qty_mapping[key]["qty"][workcenter_name] = 0
                    qty_mapping[key]["qty"][workcenter_name] += qty
                else:
                    # If it doesn't exist, initialize it with the qty and other values
                    qty_mapping[key] = {
                        "qty": {
                            workcenter_name: qty,
                        },
                        "product_qty": product_qty,
                        "partner_name": partner_name,
                        "urgence_name": urgence_name,
                    }

                # Update the product_qty, partner_name, and urgence_name in the dictionary
                qty_mapping[key]["product_qty"] = product_qty
                qty_mapping[key]["partner_name"] = partner_name
                qty_mapping[key]["urgence_name"] = urgence_name

        # Create a dictionary to store the sums of qty for each work center
        workcenter_sums = {
            "FONDERIE": 0,
            "EBARBAGE": 0,
            "SOUDURE": 0,
            "SOUSCOUCHE": 0,
            "PEINTRE": 0,
        }

        # Iterate through the qty_mapping dictionary and add rows for each group with the values
        for (production_id, product_id, product_name), values in qty_mapping.items():
            product_qty = values["product_qty"]
            partner_name = values["partner_name"]
            urgence_name = values["urgence_name"]
            qty_values = values["qty"]

            html += f"""<tr>
                <td>{production_id}</td>
                <td>{product_id}</td>
                <td>{product_name}</td>
                <td>{product_qty}</td>
                <td>{partner_name}</td>
                <td>{urgence_name}</td>
                <td>{qty_values.get("FONDERIE", 0)}</td>
                <td>{qty_values.get("EBARBAGE", 0)}</td>
                <td>{qty_values.get("SOUDURE", 0)}</td>
                <td>{qty_values.get("SOUSCOUCHE", 0)}</td>
                <td>{qty_values.get("PEINTRE", 0)}</td>
                </tr>"""

            # Update the sums for each work center
            for workcenter_name, qty in qty_values.items():
                workcenter_sums[workcenter_name] += qty

        html += "</table>"
        self.html = html
