from odoo import models, fields, api
import re


class BtnTranslate(models.Model):
    _inherit = "product.template"

    def btn_action(self):
        value = self.env.context.get("value")
        if value:
            val = ChineseDico.translation(value)
            self.write({"name": val})


class ChineseDico(models.Model):
    _name = "chinese.dico"
    _description = "Dictionnaire Chinois"

    source = fields.Char(string="Source", required=True)
    translate = fields.Char(string="Translate", required=True)
    term = fields.Char(string="Term", store=True, compute="_terms")

    @api.depends("source")
    def _terms(self):
        self.term = self._chinese_only(self.source)

    @classmethod
    def _chinese_only(self, value):
        pattern = re.compile(r"[^\u4e00-\u9fff]")
        s = value
        return re.sub(pattern, "", s)

    @classmethod
    def translate_this(cls, env, value):
        result = None
        # import pdb; pdb.set_trace()
        result = env["chinese.dico"].search([("source", "=", value)])

        if not result:
            val = value.split()

            product_records = env["product.product"].search(
                [("default_code", "in", val)]
            )

            product_codes = [product.default_code for product in product_records]

            if not product_codes:
                result = env["chinese.dico"].search(
                    [("term", "=", cls._chinese_only(value))]
                )
                if not result:
                    return value
                value = result[0].translate
                return value

            value = value.replace(product_codes[0], "")

            result = env["chinese.dico"].search([("source", "=", value)])
            value = result[0].translate
            product_code = product_codes[0]
            value = value + " " + product_code
            return value

        translate = result[0].translate
        return translate
