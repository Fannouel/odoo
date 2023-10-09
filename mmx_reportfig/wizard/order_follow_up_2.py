import logging
from odoo import models, fields, api, _


class OrderFollowUpWizard(models.TransientModel):
    _name = "order.follow.up.wizard2"
    _description = "Report Wizard for order follow up"

    sale_order_id = fields.Many2one('sale.order', string=_("Sale Order"))
    html = fields.Html(
        string="HTML"
    )

    @api.onchange("sale_order_id")
    def action_generate_report(self):
        html = "<table class=\"table-bordered\">"
        html += """<tr>
            <th>N°Fabrication</th>
            <th>Reference</th>
            <th>Designation</th>
            <th>Qte command</th>
            <th>Client</th>
            <th>Urgence</th>
            <th>coulee</th>
            <th>Ebarbage</th>
            <th>peinture d'apres</th>
            <th>polissage</th>
            <th>peinture 1k(1)</th>
            <th>polissage</th>
            <th>peinture 1k(2)</th>
            <th>controleur</th>
            <th>peinture 2k</th>
            <th>papier collant</th>
            <th>pistolet1</th>
            <th>peinture pinceau</th>
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
            "COULEE": 0,
            "EBARBAGE": 0,
            "PEINTURE_D_APRES": 0,
            "POLISSAGE": 0,
            "PEINTURE_1k(1)": 0, 
            "POLISSAGE": 0,
            "PEINTURE_1k(2)": 0,
            "CONTROLEUR": 0,
            "PPEINTURE_2k": 0,
            "PAPIER_COLLANT": 0,
            "PISTOLET1": 0,
            "PEINTURE_PINCEAU": 0,
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
                <td>{qty_values.get("COULEE", 0)}</td>
                <td>{qty_values.get("EBARBAGE", 0)}</td>
                <td>{qty_values.get("PEINTURE_D_APRES", 0)}</td>
                <td>{qty_values.get("POLISSAGE", 0)}</td>
                <td>{qty_values.get("PEINTURE_1k(1)", 0)}</td>
                <td>{qty_values.get("POLISSAGE", 0)}</td>
                <td>{qty_values.get("CONTROLEUR", 0)}</td>
                <td>{qty_values.get("PPEINTURE_2k", 0)}</td>
                <td>{qty_values.get("PAPIER_COLLANT", 0)}</td>
                <td>{qty_values.get("PISTOLET1", 0)}</td>
                <td>{qty_values.get("PEINTURE_PINCEAU", 0)}</td>
                </tr>"""

            # Update the sums for each work center
            for workcenter_name, qty in qty_values.items():
                workcenter_sums[workcenter_name] += qty

        # Add a row to display the sums of qty for each work center
    #    html += "<tr><td></td>"  # Empty cell for the first column
    #    for workcenter_name in workcenter_sums:
    #        html += f"<td>{workcenter_sums[workcenter_name]}</td>"
    #    html += "</tr>"

        html += "</table>"
        self.html = html
