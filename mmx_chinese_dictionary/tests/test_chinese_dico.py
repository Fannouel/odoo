from odoo.tests import common
from odoo.exceptions import AccessError
from odoo.tools import mute_logger
from odoo import api
from ..models.chinese_dictionary import ChineseDico


class TestChineseDico(common.TransactionCase):
    def setUp(self):
        super(TestChineseDico, self).setUp()

    def test_chinese_only_methode(self):
        chinese_dic = self.env["chinese.dico"].create(
            {"source": "天线 antenna", "translate": "antenna", "term": "天线"}
        )

        value = "天线 antenna"
        # import pdb; pdb.set_trace()
        value_chinese_only = self.env["chinese.dico"]._chinese_only(value)

        self.assertEqual(value_chinese_only, "天线")

    def test_translation_meth(self):
        chinese_dic = self.env["chinese.dico"].create(
            {"source": "天线 antenna", "translate": "antenna", "term": "天线"}
        )

        value = "天线 antenna"
        env = self.env
        # import pdb; pdb.set_trace()
        value_chinese_only = self.env["chinese.dico"].translate_this(env, value)

        self.assertEqual(value_chinese_only, "antenna")
