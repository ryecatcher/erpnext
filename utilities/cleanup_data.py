#!/usr/bin/python

# This script is for cleaning up of all data from system including 
# all transactions and masters (excludes default masters). 
# Basically after running this file, system will reset to it's 
# initial state.
# This script can be executed from lib/wnf.py using 
# lib/wnf.py --cleanup-data

from __future__ import unicode_literals
import sys
sys.path.append("lib/py")
sys.path.append(".")
sys.path.append("erpnext")

import webnotes

#--------------------------------

def delete_transactions():
	print "Deleting transactions..."

	trans = ['Timesheet','Task','Support Ticket','Stock Reconciliation', 'Stock Ledger Entry', \
		'Stock Entry','Sales Order','Salary Slip','Sales Invoice','Quotation', 'Quality Inspection', \
		'Purchase Receipt','Purchase Order','Production Order', 'POS Setting','Period Closing Voucher', \
		'Purchase Invoice','Maintenance Visit','Maintenance Schedule','Leave Application', \
		'Leave Allocation', 'Lead', 'Journal Voucher', 'Installation Note','Purchase Request', \
		'GL Entry','Expense Claim','Opportunity','Delivery Note','Customer Issue','Bin', \
		'Authorization Rule','Attendance', 'C-Form', 'Form 16A', 'Lease Agreement', \
		'Lease Installment', 'TDS Payment', 'TDS Return Acknowledgement', 'Appraisal', \
		'Installation Note', 'Communication'
	]
	for d in trans:
		for t in webnotes.conn.sql("select options from tabDocField where parent='%s' and fieldtype='Table'" % d):
			webnotes.conn.sql("delete from `tab%s`" % (t))
		webnotes.conn.sql("delete from `tab%s`" % (d))
		webnotes.conn.sql("COMMIT")
		webnotes.conn.sql("START TRANSACTION")
		print "Deleted " + d
	
	
	
def delete_masters():
	print "Deleting masters...."
	masters = {
		'Workstation':['Default Workstation'],
		'Warehouse Type':['Default Warehouse Type', 'Fixed Asset', 'Rejected', 'Reserved', 
			'Sample', 'Stores', 'WIP Warehouse'],
		'Warehouse':['Default Warehouse'],
		'UOM':['Kg', 'Mtr', 'Box', 'Ltr', 'Nos', 'Ft', 'Pair', 'Set'],
		'Territory':['All Territories', 'Default Territory'],
		'Terms and Conditions':'',
		'Tag':'',
		'Supplier Type':['Default Supplier Type'],
		'Supplier':'',
		'Serial No':'',
		'Sales Person':['All Sales Persons'],
		'Sales Partner':'',
		'Sales BOM':'',
		'Salary Structure':'',
		'Purchase Taxes and Charges Master':'',
		'Project':'',
		'Print Heading':'',
		'Price List':['Default Price List'],
		'Sales Taxes and Charges Master':'',
		'Letter Head':'',
		'Leave Type':['Leave Without Pay', 'Privilege Leave', 'Casual Leave', 'PL', 'CL', 'LWP', 
			'Compensatory Off', 'Sick Leave'],
		'Landed Cost Master':'',
		'Appraisal Template':'',
		'Item Group':['All Item Groups', 'Default'], 
		'Item':'',
		'Holiday List':'',
		'Grade':'',
		'Feed':'',
		'Expense Claim Type':['Travel', 'Medical', 'Calls', 'Food', 'Others'],
		'Event':'', 
		'Employment Type':'', 
		'Employee':'',
		'Earning Type':['Basic', 'Conveyance', 'House Rent Allowance', 'Dearness Allowance', 
			'Medical Allowance', 'Telephone'],
		'Designation':'',
		'Department':'',
		'Deduction Type':['Income Tax', 'Professional Tax', 'Provident Fund', 'Leave Deduction'],
		'Customer Group':['All Customer Groups', 'Default Customer Group'],
		'Customer':'',
		'Cost Center':'', 
		'Contact':'',
		'Campaign':'', 
		'Budget Distribution':'', 
		'Brand':'',
		'Branch':'',
		'Batch':'', 
		'Appraisal':'', 
		'Account':'', 
		'BOM': ''
	}
	for d in masters.keys():
		for t in webnotes.conn.sql("select options from tabDocField where parent='%s' \
			and fieldtype='Table'" % d):
			webnotes.conn.sql("delete from `tab%s`" % (t))
		lst = '"'+'","'.join(masters[d])+ '"'
		webnotes.conn.sql("delete from `tab%s` where name not in (%s)" % (d, lst))
		webnotes.conn.sql("COMMIT")
		webnotes.conn.sql("START TRANSACTION")
		print "Deleted " + d



def reset_all_series():
	# Reset master series
	webnotes.conn.sql("""update tabSeries set current = 0 where name not in 
		('Ann/', 'BSD', 'DEF', 'DF', 'EV', 'Event Updates/', 'FileData-', 
		'FL', 'FMD/', 'GLM Detail', 'Login Page/', 'MDI', 'MDR', 'MI', 'MIR', 
		'PERM', 'PR', 'SRCH/C/', 'TD', 'TIC/', 'TMD/', 'TW', 'UR', '_FEED', 
		'_SRCH', '_TRIGGER', '__NSO', 'CustomField', 'Letter')
	""")
	print "Series updated"
		
def reset_transaction_series():
	webnotes.conn.sql("""update tabSeries set current = 0 where name in 
		('JV', 'INV', 'BILL', 'SO', 'DN', 'PO', 'LEAD', 'ENQUIRY', 'ENQ', 'CI',
		 'IN', 'PS', 'IDT', 'QAI', 'QTN', 'STE', 'SQTN', 'SUP', 'TDSP', 'SR', 
		'POS', 'LAP', 'LAL', 'EXP')""")
	print "Series updated"


def delete_main_masters():
	main_masters = ['Fiscal Year','Company', 'DefaultValue']
	for d in main_masters:
		for t in webnotes.conn.sql("select options from tabDocField where parent='%s' and fieldtype='Table'" % d):
			webnotes.conn.sql("delete from `tab%s`" % (t))
		webnotes.conn.sql("delete from `tab%s`" % (d))
		webnotes.conn.sql("COMMIT")
		webnotes.conn.sql("START TRANSACTION")
		print "Deleted " + d
	


def reset_global_defaults():
	flds = {
		'default_company': '', 
		'default_currency': '', 
		'default_currency_format': 'Lacs', 
		'default_currency_fraction': '', 
		'current_fiscal_year': '', 
		'date_format': 'dd-mm-yyyy', 
		'sms_sender_name': '', 
		'default_item_group': 'Default', 
		'default_stock_uom': 'Nos', 
		'default_valuation_method': 'FIFO', 
		'default_warehouse_type': 'Default Warehouse Type', 
		'tolerance': '', 
		'acc_frozen_upto': '', 
		'bde_auth_role': '', 
		'credit_controller': '', 
		'default_customer_group': 'Default Customer Group', 
		'default_territory': 'Default', 
		'default_price_list': 'Standard', 
		'default_supplier_type': 'Default Supplier Type'
	}

	from webnotes.model.code import get_obj
	gd = get_obj('Global Defaults', 'Global Defaults')
	for d in flds:
		gd.doc.fields[d] = flds[d]
	gd.doc.save()
	
	webnotes.clear_cache()


def run():
	webnotes.connect()
	
	# Confirmation from user
	confirm = ''
	while not confirm:
		confirm = raw_input("Are you sure you want to delete the data from the system (N/Y)?")
	if confirm.lower() != 'y':
		raise Exception

	cleanup_type = ''
	while cleanup_type not in ['1', '2']:
		cleanup_type = raw_input("""\nWhat type of cleanup you want ot perform?
	1. Only Transactions
	2. Both Masters and Transactions

	Please enter your choice (1/2):
		""")
		
	# delete
	delete_transactions()
	
	if cleanup_type == '1':
		reset_transaction_series()
	else:
		delete_masters()
		reset_all_series()
		delete_main_masters()
		reset_global_defaults()

	print "System cleaned up succesfully"
	webnotes.conn.close()


if __name__ == '__main__':
	run()
