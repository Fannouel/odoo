odoo.define('votre_module.votre_module', function (require) {
    "use strict";
    var ActionManager = require('web.ActionManager');

    ActionManager.include({
        ir_actions_act_window: function (action, options) {
            var res = this._super.apply(this, arguments);
            if (action.context.form_view_ref === 'view_report_wizard') {
                this.do_resize(false); // Pour désactiver le redimensionnement automatique
                this.$el.dialog({ width: '800px' }); // Remplacez '800px' par la largeur souhaitée
            }
            return res;
        }
    });
});

