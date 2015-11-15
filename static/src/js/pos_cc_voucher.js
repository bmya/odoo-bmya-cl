openerp.l10n_cl_pos_credit_card_voucher = function(instance){
    var module = instance.point_of_sale;
    var QWeb = instance.web.qweb;
	var _t = instance.web._t;

    var PaymentlineSuper = module.Paymentline;
    module.Paymentline = module.Paymentline.extend({
        initialize: function(attributes, options) {
            PaymentlineSuper.prototype.initialize.apply(this, arguments);
            this.ccvoucher = '';
        },
        set_ccvoucher: function(value){
            this.ccvoucher = value;
        },
        get_ccvoucher: function(){
            return this.ccvoucher;
        },
        export_as_JSON: function(){
            var res = PaymentlineSuper.prototype.export_as_JSON.apply(this, arguments);
            res.ccvoucher = this.get_ccvoucher();
            return res;
        },
    });

    module.PaymentScreenWidget.include({
        init: function(parent, options) {
            this._super(parent,options);

            this.line_changeCCV_handler = function(){
                var node = this;
                while(node && !node.classList.contains('paymentline')){
                    node = node.parentNode;
                }
                if(node){
                    var ccvoucher;
                    try{
                        ccvoucher = instance.web.parse_value(this.value, {type: ""});
                    }
                    catch(e){
                        ccvoucher = 0;
                    }
                    node.line.set_ccvoucher(ccvoucher);
                }
            };

        },
        focus_selected_line: function(){
            var event_target_class = $(event.target).attr('class');
            var line = this.pos.get('selectedOrder').selected_paymentline;
            if(line){
                var input;
                if(event_target_class=='paymentlineCCV-input'){
                    input = line.node.querySelector('.paymentlineCCV-input');
                }else{
                    input = line.node.querySelector('.paymentline-input');
                }

                if(!input){
                    return;
                }
                var value = input.value;
                input.focus();

                if(this.numpad_state){
                    this.numpad_state.reset();
                }

                if(Number(value) === 0){
                    input.value = '';
                }else{
                    input.value = value;
                    input.select();
                }
            }
        },
        render_paymentline: function(line){
            var el_html  = openerp.qweb.render('Paymentline',{widget: this, line: line});
                el_html  = _.str.trim(el_html);

            var el_node  = document.createElement('tbody');
                el_node.innerHTML = el_html;
                el_node = el_node.childNodes[0];
                el_node.line = line;
                el_node.querySelector('.paymentline-delete').addEventListener('click', this.line_delete_handler);
                el_node.addEventListener('click', this.line_click_handler);
                el_node.querySelector('.paymentline-input').addEventListener('keyup', this.line_change_handler);
                if(line.cashregister.journal.add_credit_card_voucher_number){
                    el_node.querySelector('.paymentlineCCV-input')
                        .addEventListener('blur', this.line_changeCCV_handler);
                }

            line.node = el_node;

            return el_node;
        },

    });

}
