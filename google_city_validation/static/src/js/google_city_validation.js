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
    var level1 = "administrative_area_level_1";
    var level2 = "administrative_area_level_2";

    function feedback(policy,self){
        if (policy === 'strict') {
            warn.show_warning(
            {data: {message: _t('The city name is invalid!')}});
            self.set_value('');
        }
        else {
            warn.show_warning(
            {data: {message: _t('The city name is invalid!')}});
        }
    }
    function checker(res,stat,self){
        var addr;
        var check = 1;
        if (res.length > 0){
            addr = res[0].formatted_address.split(",");
            if (stat != 'OK' ||
            ! ((res[0].types.includes("locality") ||
            res[0].types.includes(level1) ||
            res[0].types.includes(level2)) &&
            addr[0].toUpperCase() === self.get_value().toUpperCase())){
                check = 0;
            }
        }
        else{
            check = 0;
        }
        return check;
    }
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
            var city = this.get_value();
            var self = this;
            var request;
            var manager = this.field_manager;
            var id;

            var country_option = self.options.hasOwnProperty('country');

            param.call('get_param', ['google_city_validation.policy', false])
            .then(function(policy) {
                if (self.get_value() != '') {
                    if (!country_option) {
                        request = {address: city};
                        self.geocoder.geocode(request,
                        function(results, status) {
                            if (status != 'OK' ||
                            ! (results[0].types.includes("locality") ||
                            results[0].types.includes(level1) ||
                            results[0].types.includes(level2))) {
                                feedback(policy,self);
                            }
                        });
                    }
                    else {
                        id = manager.fields[self.options.country].get_value();
                        if (id != ''){
                            new Model('res.country').query(['id','code'])
                            .filter([['id', '=', id]]).first().then(
                            function(country) {
                                request ={
                                    address: city,
                                    componentRestrictions: {
                                        country: country.code
                                    }
                                };
                                self.geocoder.geocode(request,
                                function(results, status) {
                                    var check;
                                    check = checker(results,status,self);
                                    if (check === 0) {
                                      feedback(policy,self);
                                    }
                                });
                            });
                        }
                        else{
                            warn.show_warning(
                            {data: {
                            message: _t('You must select the country!')}});
                            self.set_value('');
                        }
                    }
                }
            });
        },
    })
    core.form_widget_registry.add('google_city_validation', CityWidget);
});
