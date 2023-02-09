import math
import re
from re import match
from datetime import datetime, timedelta
from num2words import num2words
from odoo import models, fields, api, _
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from collections import defaultdict
from odoo.tools import datetime


class account_move(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move Custom Inherit'

    forex_ex = fields.Float(string="Forex Exchange", compute='_compute_forex_ex')
    add_data = fields.Integer(string='Data sample', compute='_compute_add_data')
    forex_exchange = fields.Float(string='Forex Exchange')
    percentage = fields.Float(string='Percentage Added')
    amount_total_in_php = fields.Float(string='Total Amount in PHP')
    divided_usd = fields.Float(string='Divided USD', digits=(12, 3))
    total_usd = fields.Float(string='Total US$')
    compute_total_usd = fields.Float(string='Total US$', compute='_compute_total_usd')
    computed_total = fields.Float(string='Processing Fee', compute='_compute_total')
    # computed_php = fields.Float(string='Computed Total Php', compute='_computed_php')
    percentage_get_total = fields.Float(compute="_compute_percentage_get_total")
    total_amount_without_monetary = fields.Float('Total Amount')
    remove_monetary = fields.Float(compute='_remove_monetary')
    total_amount_without_monetary1 = fields.Float('Total Amount')
    remove_monetary1 = fields.Float(compute='_remove_monetary1')
    word_num = fields.Char(string="Amount In Words:", compute='remove_comma', readonly=True)
    word_move = fields.Char(string='Amount in Words', readonly=True)
    get_currency_name = fields.Float(compute="get_name_currency")
    currency_name_here = fields.Char('Currency Name')

    get_total_in_deb_cred_compute = fields.Float(compute='calculate_journal')
    get_total_in_deb_cred = fields.Float('Journal Items Total Amount')

    usd_to_php = fields.Float(compute='usd_to_php_compute')
    debit_here = fields.Float(compute='get_journal')

    debit_payable = fields.Float(compute='get_journal_payable')

    to_convert_debit_credit = fields.Float(compute='convert_debit_credit')
    converting_percent = fields.Float(compute='converting_with_fee')
    add_percent = fields.Float()

    getting_forex_php = fields.Float(compute='getting_php_forex')
    saving_forex_php_value = fields.Float()

    adding_usd_with_percent_here = fields.Float(compute='adding_usd_with_percent')
    adding_usd_with_percent_value = fields.Float()

    computing_forex_and_amm = fields.Float(compute='computing_forex_and_amm_var')
    forex_and_amm_val = fields.Float()

    computing_forex_and_amm_v2 = fields.Float(compute='computing_forex_and_amm_var_v2')
    forex_and_amm_val_v2 = fields.Float()

    getting_total_of_debit_credit_var = fields.Float(compute='getting_total_of_debit_credit')
    getting_total_of_debit_credit_val = fields.Float()

    def getting_total_of_debit_credit(self):
        self.getting_total_of_debit_credit_var = 0
        a = 0
        for rec in self.line_ids:
            a += rec.credit
        print(a, '<-- Deb Cred Var')
        self.getting_total_of_debit_credit_val = a

    def computing_forex_and_amm_var_v2(self):
        self.computing_forex_and_amm_v2 = 0
        get_currency_payable = self.currency_id
        get_curr_name = 0
        for rec in get_currency_payable:
            get_curr_name = rec.name
        print(get_curr_name)
        if get_curr_name:
            if get_curr_name == 'PHP':
                currency = self.env['res.currency'].search([('name', '=', 'PHP')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = list(data_here.values())
                save_record = 0
                for rec in number:
                    save_record = int(rec)
                total = self.total_usd / save_record
                self.forex_and_amm_val_v2 = total

                debit_val = 0
                for rec_debit in self.line_ids:
                    debit_val = rec_debit.debit / save_record
                    rec_debit.debit_data_v2 = debit_val

                credit_val = 0
                for rec_credit in self.line_ids:
                    credit_val = rec_credit.credit / save_record
                    rec_credit.credit_data_v2 = credit_val


            elif get_curr_name == 'USD':
                currency = self.env['res.currency'].search([('name', '=', 'PHP')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = list(data_here.values())
                save_record = 0
                for rec in number:
                    save_record = int(rec)
                total = self.total_usd
                self.forex_and_amm_val_v2 = total

                debit_val = 0
                for rec_debit in self.line_ids:
                    debit_val = rec_debit.debit / save_record
                    rec_debit.debit_data_v2 = debit_val

                credit_val = 0
                for rec_credit in self.line_ids:
                    credit_val = rec_credit.credit / save_record
                    rec_credit.credit_data_v2 = credit_val
            elif get_curr_name == 'EUR':
                currency = self.env['res.currency'].search([('name', '=', 'PHP')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = list(data_here.values())
                save_record = 0
                for rec in number:
                    save_record = int(rec)
                total = self.total_usd / save_record
                self.forex_and_amm_val_v2 = total
            else:
                print('Error')
        else:
            print('Error')

    def computing_forex_and_amm_var(self):
        self.computing_forex_and_amm = 0
        get_currency_payable = self.currency_id
        get_curr_name = 0
        for rec in get_currency_payable:
            get_curr_name = rec.name
        print(get_curr_name)
        if get_curr_name:
            if get_curr_name == 'PHP':
                self.forex_and_amm_val = self.amount_total
            elif get_curr_name == 'USD':
                currency = self.env['res.currency'].search([('name', '=', 'PHP')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = list(data_here.values())
                save_record = 0
                for rec in number:
                    save_record = int(rec)
                total = self.amount_total * save_record
                self.forex_and_amm_val = total
            elif get_curr_name == 'EUR':
                currency = self.env['res.currency'].search([('name', '=', 'PHP')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = list(data_here.values())
                save_record = 0
                for rec in number:
                    save_record = int(rec)
                total = self.amount_total / save_record
                self.forex_and_amm_val = total
            else:
                print('Error')
        else:
            print('Error')

    def adding_usd_with_percent(self):
        self.adding_usd_with_percent_here = 0
        adding = self.getting_total_of_debit_credit_val + self.add_percent
        print(self.getting_total_of_debit_credit_val, '<-- USD')
        print(adding, '<-- Adding')
        self.adding_usd_with_percent_value = adding

    def getting_php_forex(self):
        self.getting_forex_php = 0
        currency = self.env['res.currency'].search([('name', '=', 'PHP')])
        currency_id_here = currency.id
        query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
        self.env.cr.execute(query)
        data_here = self.env.cr.dictfetchone()
        print(data_here)
        number = list(data_here.values())
        save_record = 0
        for rec in number:
            save_record = int(rec)
        self.saving_forex_php_value = save_record
        print(save_record, '<-- new ')

    def converting_with_fee(self):
        self.converting_percent = 0
        five_percent = self.usd_to_php
        print(five_percent, '<-- FIVE PERCENT')
        total_convert = five_percent * 0.05
        self.add_percent = total_convert
        print(self.add_percent, '<-- CONVERT')

    def get_journal_payable(self):
        self.debit_payable = 0
        get_currency_payable = self.currency_id
        get_curr_name = 0
        for rec in get_currency_payable:
            get_curr_name = rec.name
        print(get_curr_name)
        if get_curr_name:
            if get_curr_name == 'PHP':
                currency = self.env['res.currency'].search([('name', '=', 'PHP')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = list(data_here.values())
                save_record = 0
                for rec in number:
                    save_record = int(rec)
                print(save_record)

                for rec in self.line_ids:
                    get_debit = rec.debit
                    print(get_debit)
                    rec.debit_data_payable = get_debit
                    print(rec.debit_data_payable, '<----- Teeeesssttt Payable')

                for rec in self.line_ids:
                    get_credit = rec.credit
                    print(get_credit)
                    rec.credit_data_payable = get_credit
                    print(rec.credit_data_payable, '<----- Credit Payable')

            elif get_curr_name == 'USD':
                currency = self.env['res.currency'].search([('name', '=', 'PHP')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = list(data_here.values())
                save_record = 0
                for rec in number:
                    save_record = int(rec)
                print(save_record)
                # get currency from amount end

                # this is for debit

                for rec in self.line_ids:
                    get_debit = rec.debit / save_record
                    print(get_debit)
                    rec.debit_data_payable = get_debit
                    print(rec.debit_data_payable, '<----- Debit Payable')

                # this is for credit

                for rec in self.line_ids:
                    get_credit = rec.credit / save_record
                    print(get_credit)
                    rec.credit_data_payable = get_credit
                    print(rec.credit_data_payable, '<----- Credit Payable')

            elif get_curr_name == 'EUR':
                currency = self.env['res.currency'].search([('name', '=', 'PHP')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = list(data_here.values())
                save_record = 0
                for rec in number:
                    save_record = int(rec)
                print(save_record)
                # get currency EUR

                # this is for debit

                for rec in self.line_ids:
                    print(rec.credit, '<--- credit')
                    get_debit = rec.debit / save_record
                    print(get_debit)
                    rec.debit_data_payable = get_debit
                    print(rec.debit_data_payable, '<----- Debit Payable')

                # this is for credit
                for rec in self.line_ids:
                    get_credit = rec.credit / save_record
                    print(get_credit)
                    rec.credit_data_payable = get_credit
                    print(rec.credit_data_payable, '<----- Credit Payable')

            elif get_curr_name == 'JPY':
                print('JPY')
            else:
                print('Error')
        else:
            print('Error')

    def get_journal(self):
        self.debit_here = 0
        currency = self.env['res.currency'].search([('name', '=', 'PHP')])
        get_rate = 0
        for rec in currency:
            get_rate = rec.rate
        for rec in self.line_ids:
            get_debit = rec.debit / get_rate
            print(get_debit)
            rec.debit_data = get_debit
            print(rec.debit_data)
        for rec in self.line_ids:
            get_credit = rec.credit / get_rate
            print(get_credit)
            rec.credit_data = get_credit
            print(rec.credit_data)

    def convert_debit_credit(self):
        self.to_convert_debit_credit = 0
        currency = self.currency_name_here
        if currency == 'USD':
            currency = self.env['res.currency'].search([('name', '=', 'PHP')])
            get_rate = 0
            for rec in currency:
                get_rate = rec.rate
                print(get_rate)
            for rec in self.line_ids:
                counter = rec.debit / get_rate
                # rec.to_debit_data = counter
                rec.to_debit_data_converted = counter
                print(counter, '<-- debit')
            for rec in self.line_ids:
                counter1 = rec.credit / get_rate
                print(counter1, '<-- credit')
                # rec.to_credit_data = counter1
                rec.to_credit_data_converted = counter1
        elif currency == 'PHP':
            for rec in self.line_ids:
                counter = rec.debit
                print(counter, '<-- debit')
                rec.to_debit_data_converted = counter
            for rec in self.line_ids:
                counter1 = rec.credit
                print(counter1, '<-- credit')
                rec.to_credit_data_converted = counter1
        elif currency == 'EUR':
            for rec in self.invoice_line_ids:
                counter = rec.debit / self.forex_exchange
                counter1 = rec.credit / self.forex_exchange
                print(counter, '<-- debit')
                print(counter1, '<-- Credit')
        else:
            print('Test')

    def print_for_invoice_voucher(self):
        print_here = self.env.ref('team_accounting.account_vendor_bills_report').report_action(self)
        return print_here

    def print_for_payable_voucher(self):
        print_here = self.env.ref('team_accounting.ap_voucher_print_id').report_action(self)
        return print_here

    def print_for_credit_note_voucher(self):
        print_here = self.env.ref('team_accounting.debit_credit_report_id_here').report_action(self)
        return print_here

    def print_for_credit_note_voucher_v2(self):
        print_here = self.env.ref('team_accounting.debit_credit_report_id_wo_fee_here').report_action(self)
        return print_here

    def print_for_journal_entry_voucher(self):
        print_here = self.env.ref('team_accounting.action_report_payment_voucher_acc_move').report_action(self)
        return print_here

    # @api.depends('forex_exchange',  'currency_name_here')
    # def _computed_php(self):
    #     for rec in self:
    #         rec.computed_php = rec.forex_exchange / rec.amount_total
    #         rec.amount_total_in_php = rec.computed_php

    # @api.depends('invoice_payment_term_id', 'invoice_date_due')
    # def count_date_here(self):
    #     self.to_count_total_days = 0
    #     for rec in self:
    #         split_inv_payment = rec.invoice_payment_term_id.name
    #         if rec.invoice_payment_term_id:
    #             print(split_inv_payment, '<---------- Inv Payment')
    #             splitting_inv = split_inv_payment.split(' ')
    #             dates = [
    #                 'Days',
    #                 'Months',
    #                 'Weeks'
    #                 'Years',
    #                 'Days',
    #                 'Months',
    #                 'Years',
    #                 'days',
    #                 'months',
    #                 'years',
    #                 'days',
    #                 'weeks',
    #                 'months',
    #                 'years',
    #             ]
    #             for item1 in splitting_inv:
    #                 for item2 in dates:
    #                     if item1 == item2:
    #                         if item1 == 'Days' or item1 == 'days':
    #                             val1, val2 = split_inv_payment.split(' ')
    #                             print(int(val1))
    #                             get_number = int(val1)
    #                             date_timedelta = self.invoice_date + timedelta(days=get_number)
    #                             print(date_timedelta)
    #                             self.get_days = date_timedelta
    #                         elif item1 == 'Weeks' or item1 == 'weeks':
    #                             val1, val2 = split_inv_payment.split(' ')
    #                             print(int(val1))
    #                             get_number = int(val1)
    #                             date_timedelta = self.invoice_date + timedelta(weeks=get_number)
    #                             print(date_timedelta)
    #                             self.get_days = date_timedelta
    #                         elif item1 == 'Months' or item1 == 'months':
    #                             val1, val2 = split_inv_payment.split(' ')
    #                             print(int(val1))
    #                             get_number = int(val1)
    #                             date_timedelta = self.invoice_date + relativedelta(months=get_number)
    #                             print(date_timedelta)
    #                             self.get_days = date_timedelta
    #                         elif item1 == 'Years' or item1 == 'years':
    #                             val1, val2 = split_inv_payment.split(' ')
    #                             print(int(val1))
    #                             get_number = int(val1)
    #                             date_timedelta = self.invoice_date + relativedelta(years=get_number)
    #                             print(date_timedelta)
    #                             self.get_days = date_timedelta
    #         elif rec.invoice_date_due:
    #             for get_date in self:
    #                 due_date = get_date.invoice_date_due
    #                 self.get_days = due_date
    #                 print(due_date)
    #         else:
    #             print('no data')
    def calculate_journal(self):
        self.get_total_in_deb_cred_compute = 0
        calculate_deb_cred = 0
        for rec in self.line_ids:
            calculate_deb_cred = calculate_deb_cred + rec.debit
        print(calculate_deb_cred)
        self.get_total_in_deb_cred = calculate_deb_cred

    @api.depends('currency_name_here')
    def usd_to_php_compute(self):
        self.usd_to_php = 0
        currency = self.currency_name_here
        if currency == 'USD':
            for rec in self:
                rec.usd_to_php = rec.amount_total * rec.forex_exchange
                rec.amount_total_in_php = rec.usd_to_php
                print(rec.amount_total_in_php)
        elif currency == 'PHP':
            for rec in self:
                rec.usd_to_php = rec.amount_total / rec.forex_exchange
                rec.amount_total_in_php = rec.usd_to_php
                print(rec.amount_total_in_php)
        else:
            print('Test')

    @api.depends('currency_id')
    def get_name_currency(self):
        self.get_currency_name = 0
        name_here = ""
        for rec in self:
            name_here = rec.currency_id.name
            print(name_here)
        self.currency_name_here = name_here

    @api.depends('currency_id')
    def calculate_dropdown(self):
        currency_here = ""
        for rec in self:
            currency_here = rec.currency_id.rate_ids.rate
        print(currency_here, "<----- NEW")

    @api.depends('percentage', 'amount_total')
    def _compute_total(self):
        for rec in self:
            rec.computed_total = rec.amount_total * rec.percentage
            rec.divided_usd = rec.computed_total

    @api.depends('forex_exchange', 'amount_total')
    def _computed_php(self):
        for rec in self:
            rec.computed_php = rec.forex_exchange / rec.amount_total
            rec.amount_total_in_php = rec.computed_php

    @api.depends('percentage', 'amount_total')
    def _compute_percentage_get_total(self):
        for rec in self:
            rec.percentage_get_total = rec.percentage * rec.amount_total
            rec.divided_usd = rec.percentage_get_total

    @api.depends('amount_total', 'divided_usd')
    def _compute_total_usd(self):
        for rec in self:
            rec.compute_total_usd = rec.amount_total + rec.divided_usd
            rec.total_usd = rec.compute_total_usd

    @api.depends('amount_total')
    def _remove_monetary(self):
        for rec in self:
            rec.remove_monetary = rec.amount_total + 0
            rec.total_amount_without_monetary = rec.remove_monetary

    @api.depends('percentage')
    def _remove_monetary1(self):
        for rec in self:
            rec._remove_monetary1 = rec.percentage * 100
            rec.total_amount_without_monetary1 = rec._remove_monetary1
            print(rec.converted)

    def _amount_in_word(self):
        for rec in self:
            rec.word_num = num2words((rec.total_usd))

    def sample(self):
        sample = self.amount_total_signed
        print(sample)
        get_currency_ex = self.currency_id.rate_ids
        # sample = get_currency_ex.rate
        # print(sample)
        get_currency_ex = self.currency_id.rate_ids
        print(self.add_data, get_currency_ex)
        # sample = self.amount_total_signed.amount_to_text()
        percentage = self.percentage
        total = sample * percentage
        check = self.forex_exchange
        print(check)
        print(total)

    def _compute_add_data(self):
        currency = self.env['res.currency'].search([('name', '=', 'PHP')])
        self.add_data = currency
        record = self.write({
            'add_data': currency
        })
        return record

    @api.depends('currency_id')
    def _compute_forex_ex(self):
        self.forex_ex = 0
        print('Compute Forex')
        get_currency_ex = self.currency_id.rate_ids
        for rec in get_currency_ex:
            exchange_rate = rec.rate
            self.forex_ex = exchange_rate
            record = self.write({
                'forex_exchange': exchange_rate,
            })
            return record

    @api.depends('remove_monetary')
    def remove_comma(self):
        self.word_num = 0
        print('sample')
        for x in self:
            print(x)
            dollars, cents = str(x.remove_monetary).split(".")

            # Convert the dollar amount to words
            dollar_words = num2words(float(dollars))
            print(dollar_words)
            # If the amount has no cents, return the dollar amount with "Only"
            if cents == "00":
                print("{} Only".format(dollar_words))
                word = "{} Only".format(dollar_words)
                remove_comma = re.sub(',', '', str(word))
                remove_dash = re.sub('-', ' ', str(remove_comma))
                word_in_arr = remove_dash.split(' ')
                print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                test_str = ''
                for rec_arr in word_in_arr:
                    if rec_arr != 'and':
                        test_str = test_str + rec_arr + ' '
                print(test_str.title())
                self.word_move = test_str.title()
            # If the amount has cents, convert the cents to a fraction and combine with the dollar amount
            elif cents == "0":
                print("{} Only".format(dollar_words))
                word = "{} Only".format(dollar_words)
                remove_comma = re.sub(',', '', str(word))
                remove_dash = re.sub('-', ' ', str(remove_comma))
                word_in_arr = remove_dash.split(' ')
                print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                test_str = ''
                for rec_arr in word_in_arr:
                    if rec_arr != 'and':
                        test_str = test_str + rec_arr + ' '
                print(test_str.title())
                self.word_move = test_str.title()
            else:
                print('Sample')
                cents_int = cents
                cent_int = list(map(int, str(cents_int)))
                print(cent_int)
                counting_cents_stored = len(cent_int)
                if counting_cents_stored == 1:
                    print(counting_cents_stored)
                    cent_fraction = "{}0/100".format(cents)
                    word = "{} & {} Only".format(dollar_words, cent_fraction)
                    remove_and = re.sub(',', '', str(word))
                    remove_dash = re.sub('-', ' ', str(remove_and))
                    word_in_arr = remove_dash.split(' ')
                    print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                    test_str = ''
                    for rec_arr in word_in_arr:
                        if rec_arr != 'and':
                            test_str = test_str + rec_arr + ' '
                    print(test_str.title())
                    self.word_move = test_str.title()
                else:
                    print(counting_cents_stored)
                    cent_fraction = "{}/100".format(cents)
                    word = "{} & {} Only".format(dollar_words, cent_fraction)
                    remove_and = re.sub(',', '', str(word))
                    remove_dash = re.sub('-', ' ', str(remove_and))
                    word_in_arr = remove_dash.split(' ')
                    print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                    test_str = ''
                    for rec_arr in word_in_arr:
                        if rec_arr != 'and':
                            test_str = test_str + rec_arr + ' '
                    print(test_str.title())
                    self.word_move = test_str.title()


class account_move_line(models.Model):
    _inherit = 'account.move.line'
    _description = 'Account Move Line Custom Inherit'

    debit_data_payable = fields.Float()
    credit_data_payable = fields.Float()
    debit_data = fields.Float()
    credit_data = fields.Float()
    to_debit_data = fields.Float()
    to_credit_data = fields.Float()
    to_debit_data_converted = fields.Float()
    to_credit_data_converted = fields.Float()
    debit_data_v2 = fields.Float()
    credit_data_v2 = fields.Float()
