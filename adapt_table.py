import sys
import sqlite3

ammcat_table = 'ammcat'
ammcat_com_id = 'FKAMMCOM'
ammcom_table = 'ammcom'
ammcom_com_id = 'CLASSID'
com_id_prefix = 'AMB003_'
ammcva_table = 'ammcva'
ammcva_cva_id = 'CLASSID'
cva_id_prefix = 'AMB002_'

def adapt_amm_tables(db_file):
	conn = sqlite3.connect(db_file)
	cur = conn.cursor()
	
	cur.execute("UPDATE {0} SET {1} = substr({1}, length('{2}') + 1, length({1}) - length('{2}'));".format(ammcom_table, ammcom_com_id, com_id_prefix))
	
	cur.execute("UPDATE {0} SET {1} = substr({1}, length('{2}') + 1, length({1}) - length('{2}'));".format(ammcat_table, ammcat_com_id, com_id_prefix))
	
	cur.execute("UPDATE {0} SET {1} = substr({1}, length('{2}') + 1, length({1}) - length('{2}'));".format(ammcva_table, ammcva_cva_id, cva_id_prefix))
	
	conn.commit()
	cur.close()
	conn.close()

def adapt_cat_table(db_file, table):
	conn = sqlite3.connect(db_file)
	cur = conn.cursor()
	
	cur.execute("ALTER TABLE '{0}' ADD COLUMN dsup_sopra TEXT DEFAULT '';".format(table))
	cur.execute("ALTER TABLE '{0}' ADD COLUMN dsup_sotto TEXT DEFAULT '';".format(table))
	cur.execute("ALTER TABLE '{0}' ADD COLUMN ctwexpr_ INTEGER;".format(table))
	cur.execute("ALTER TABLE '{0}' ADD COLUMN ctwexpr_id INTEGER;".format(table))
	
	conn.commit()
	cur.close()
	conn.close()
	
try:
	db_file = str(sys.argv[1])
	table = str(sys.argv[2])
	if table == 'amm':
		adapt_amm_tables(db_file)
		print('Fixed {0} values in {1}.'.format(ammcom_com_id, ammcom_table))
		print('Fixed {0} values in {1}.'.format(ammcat_com_id, ammcat_table))
		print('Fixed {0} values in {1}.'.format(ammcva_cva_id, ammcva_table))
	else:
		adapt_cat_table(db_file, table)
		print('Added columns to {0}.'.format(table))
except IndexError:
	print('Error: missing DB file or table.')