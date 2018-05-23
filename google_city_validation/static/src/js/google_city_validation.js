/*
    © 2018 Savoir-faire Linux <https://savoirfairelinux.com>
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define('google_city_validation', function (require) {
    "use strict";
    var core = require('web.core');
    var form_widgets = require('web.form_widgets');
    var Model = require('web.Model');
    var warn = require('web.crash_manager');
    var _t = core._t;

    var CityWidget = form_widgets.FieldChar.extend({
        init: function (field_manager, node) {
            this._super(field_manager, node);
            this.on("change:value", this, function() {
                this.onchangeCity();
            });
        },
        start: function() {
            this._super();
            this.geocoder = new google.maps.Geocoder();
        },
        onchangeCity: function() {
            var param = new Model('ir.config_parameter');
            var request = {'address': this.get_value()};
            var self = this;
            param.call('get_param', ['google_city_validation.policy', false])
            .then(function(policy) {
                if (self.get_value() != '') {
                    self.geocoder.geocode(request, function(results, status) {
                        if (status != 'OK' ||
                         !results[0].types.includes("locality")) {
                             if (policy === 'strict') {
                                 warn.show_warning(
                                 {data: {
                                 message: _t('The city name is invalid!')}});
                                 self.set_value('')
                             }
                             else {
                                 warn.show_warning(
                                 {data: {
                                 message: _t('The city name is invalid!')}});
                             }
                         }
                    });
                }
            });
        },
    })
    core.form_widget_registry.add('google_city_validation', CityWidget);
});
