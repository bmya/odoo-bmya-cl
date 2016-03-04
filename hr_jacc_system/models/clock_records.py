# -*- coding: utf-8 -*-
from __future__ import print_function
from openerp import models, fields, api
from datetime import datetime
import datetime as dt1
from openerp.tools.translate import _
from openerp.exceptions import Warning
# import io
import pytz
from openerp import SUPERUSER_ID


try:
    import xlrd
    from xlrd.sheet import ctype_text
except ImportError:
    pass

try:
    import base64
except ImportError:
    pass



class clock_records(models.Model):

    def convert_timezone(self, tz, day, time):

        naive = datetime.strptime(
            day + ' ' + time+':00.000000', '%d-%m-%Y %H:%M:%S.%f')
        local_dt = tz.localize(naive, is_dst=None)
        utc_dt = local_dt.astimezone (pytz.utc)
        print(local_dt)
        print(utc_dt)
        return utc_dt.strftime ("%Y-%m-%d %H:%M:%S")


    _name = 'hr.clock.records'

    name = fields.Char('File Name', readonly=True, compute='_get_name',
                       store=True)

    filename = fields.Char('File Name')

    clock_file = fields.Binary(
        string='Clock Records File', filters='*.xls', required=True,
        store=True, help='Upload the XLS Clock File in this holder')

    issued_date = fields.Datetime('Issued Date', compute='_get_date',
                                  store=True)

    
    start_date = fields.Date(
        string='Start Date', help='First Control Date')
    
    final_date = fields.Date(
        string='Last Date', help='Last Control Date')

    status = fields.Selection([('draft', 'Draft'),('processed', 'Processed'),
                               ('cancelled', 'Cancelled')],
                          string='Status', default='draft',
                          help='''Draft: means it has not been processed yet.
You must press the \"process"\ button in order to execute the calculator
proccess, that injects the contents of the file inside attendance.''')

    company_id = fields.Many2one(
        'res.company', 'Company', required=False,
        default=lambda self: self.env.user.company_id)

    attendance_ids = fields.One2many(
        'hr.attendance', 'clock_record_id', string='Attendance Records')

    @api.multi
    def action_process(self):
        if 1 == 1:
            self.ensure_one()
            # get user's timezone
            user = self.env['res.users'].browse(SUPERUSER_ID)
            tz = pytz.timezone(user.partner_id.tz) or pytz.utc

            print('aca se procesa el archivo')

            fname = 'clock_file.xls'
            print(fname)
            filecontent = base64.b64decode(self.clock_file)

            f = open(fname,'w')
            f.write(filecontent)
            f.close()

            # open file
            xl_workbook = xlrd.open_workbook(fname, encoding_override='cp1252')
            # xl_workbook = xlrd.open_workbook(
            #    fname, file_contents=xlsfile, encoding_override='cp1252')
            # List sheet names, and pull a sheet by name
            #
            sheet_names = xl_workbook.sheet_names()
            # print('Sheet Names', sheet_names)

            xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])

            # Or grab the first sheet by index
            #  (sheets are zero-indexed)
            #
            xl_sheet = xl_workbook.sheet_by_index(0)
            # print ('Sheet name: %s' % xl_sheet.name)

            # Pull the first row by index
            #  (rows/columns are also zero-indexed)
            #
            row = xl_sheet.row(0)  # 1st row

            datos_title = []
            dictio_data = []
            log_not_present = {}

            # Print 1st row values and types
            #
            from xlrd.sheet import ctype_text

            # print('(Column #) type:value')
            for idx, cell_obj in enumerate(row):
                cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
                # print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))
                datos_title.append(cell_obj.value.encode('utf-8'))

            print(datos_title)

            # Print all values, iterating through rows and columns
            #
            num_cols = xl_sheet.ncols   # Number of columns
            for row_idx in range(0, xl_sheet.nrows):    # Iterate through rows
                row_data = {}
                if row_idx == 0:
                    continue
                # print ('-'*40)
                # print ('Row: %s' % row_idx)   # Print row number
                for col_idx in range(0, num_cols):  # Iterate through columns
                    cell_obj = xl_sheet.cell(row_idx, col_idx)
                    row_data[datos_title[col_idx]] = cell_obj.value.encode(
                        'utf-8')

                # aca lista los rut con los cuales debo buscar los partner_id

                employee_id = self.env['hr.employee'].search(
                    [['identification_id', 'like', row_data['AC-No.']]]).id
                print(
                    row_data['Nombre'], 'RUT: ', row_data['AC-No.'],
                    employee_id)
                if employee_id == False:
                    log_not_present[row_data['AC-No.']] = row_data['Nombre']
                else:
                    row_data['empl_id'] = employee_id
                    pass
                    # arma un diccionario para meter los datos en Odoo

                # saca la fecha de inicio
                if dictio_data == []:
                    print('fecha inicio:')
                    print(row_data['Dia'])
                    print(datetime.strptime(
                        row_data['Dia'], '%d-%m-%Y').strftime('%Y-%m-%d'))
                    # debe controlar que no se repita la start date en
                    # ningun otro archivo
                    # ni como start date ni como end data.
                    # Si no da error, grabar
                    # si no, cortar sin procesar
                    self.start_date = datetime.strptime(
                        row_data['Dia'], '%d-%m-%Y').strftime('%Y-%m-%d')

                    # Arma la lista de diccionario

                # Arma la lista de diccionario
                dictio_data.append(row_data)

            if log_not_present != {}:
                # no lo puede procesar por existir registros que no estan
                # ingresados
                raise Warning(_('''The following employees are not present
in database, : '''), log_not_present, _('''The file could not be processed.'''))
                # print('''El empleado %s con RUT %s no
                # está en la base de
                # empleados de Odoo''' % (row_data['Nombre'],
                # row_data['AC-No.']))
            print('fecha fin:')
            print(row_data['Dia'])
            print(datetime.strptime(
                row_data['Dia'], '%d-%m-%Y').strftime('%Y-%m-%d'))
            # debe controlar que no se repita la start date en ningun otro
            # archivo ni como start date ni como end data. Si no da error,
            # grabar
            # si no, cortar sin procesar
            self.final_date = datetime.strptime(
                row_data['Dia'], '%d-%m-%Y').strftime('%Y-%m-%d')
            # comienzo el proceso de grabado
            print('dictio_data: %s' % dictio_data)
            record_data_in = {}
            record_data_out = {}
            penalizacion = dt1.timedelta(hours=1)
            for d_data in dictio_data:
                record_data_in['forfeit'] = False
                record_data_out['forfeit'] = False

                # analiza la entrada
                if d_data['Marc-Ent'] == '':
                    # tomar la hora de entrada normal mas 1h
                    d_data['Marc-Ent'] = (datetime.strptime(
                        d_data['HoraEnt'], '%H:%M') + penalizacion).strftime(
                        '%H:%M')
                    record_data_in['forfeit'] = True

                if d_data['Marc-Sal'] == '':
                    # tomar la hora de salida normal menos 1h
                    print(d_data['HoraSal'])
                    d_data['Marc-Sal'] = (datetime.strptime(
                        d_data['HoraSal'], '%H:%M') - penalizacion).strftime(
                        '%H:%M')
                    record_data_out['forfeit'] = True

                # establecer si el registro corriente se graba en hr.holidays
                # o en hr.leave
                # correr la fecha de acuerdo a la zona horaria en la que viene
                # informada
                record_data_in['employee_id'] = d_data['empl_id']
                record_data_in['name'] = self.convert_timezone(
                    tz, d_data['Dia'], d_data['Marc-Ent'])
                record_data_in['action'] = 'sign_in'
                record_data_in['clock_record_id'] = self.id
                print('estoy por grabar %s' % record_data_in)
                self.env['hr.attendance'].create(record_data_in)

                record_data_out['employee_id'] = d_data['empl_id']
                record_data_out['name'] = self.convert_timezone(
                    tz, d_data['Dia'], d_data['Marc-Sal'])
                record_data_out['action'] = 'sign_out'
                record_data_out['clock_record_id'] = self.id
                print('estoy por grabar %s' % record_data_out)
                self.env['hr.attendance'].create(record_data_out)

            # fin del proceso de grabado
            self.status = 'processed'
        else:
            pass

    @api.multi
    def action_cancel(self):
        try:
            self.ensure_one()
            print('aca se cancela el archivo')
            self.status = 'cancelled'
        except:
            pass

    @api.multi
    @api.depends('clock_file')
    def _get_date(self):
        self.ensure_one()
        old_date = self.issued_date
        if self.clock_file != None and self.status == 'draft':
            print(self.clock_file)
            self.issued_date = fields.datetime.now()
        else:
            print('valor antiguo de fecha')
            print(old_date)
            self.issued_date = old_date



    @api.multi
    @api.depends('clock_file')
    def _get_name(self):
        self.ensure_one()
        old_name = self.name
        if self.clock_file != None and self.status == 'draft':
            if self.filename:
                self.name = '%s - %s' % (
                    self.filename.replace('.xls', ''), datetime.strptime(
                        self.issued_date, '%Y-%m-%d %H:%M:%S').strftime(
                        '%Y/%m/%d %H:%M:%S'))
        else:
            print('valor antiguo de nombre')
            print(old_name)
            self.name = old_name


class hr_attendance(models.Model):

    _name = 'hr.attendance'
    _inherit = 'hr.attendance'

    clock_record_id = fields.Many2one('hr.clock.records', 'Clock Record File',
                                      select=True, ondelete='cascade')
    forfeit = fields.Boolean('Forfeit', help='''Forfeit or penalty when check
in or check out not executed''')