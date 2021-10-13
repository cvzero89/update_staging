import subprocess
import os
import shutil

site_name = os.path.split(os.getcwd())[1]
site_without_dot = site_name.replace('.','')
stage_name = f'{site_without_dot}.stage.site'
print(f'Site is {site_name}. \nIf you\'re not running this from the live site, exit now.')
print(f'Staging URL is {stage_name}')
wordpress_prefix = subprocess.Popen(['wp', 'config', 'get', 'table_prefix'], stdout=subprocess.PIPE)
prefix = wordpress_prefix.communicate()[0].decode('utf-8').strip()
print(f"The WordPress Prefix is {prefix}")
wordpress_prefix.stdout.close()

tables_check = subprocess.Popen(['wp', 'db', 'tables', '--all-tables'], stdout=subprocess.PIPE)
table_check = tables_check.communicate()[0].decode('utf-8').strip()

def get_tables():
    tables_with_prefix = []
    input_string = input("List tables to update in staging separated with a space without the WordPress prefix:")
    tables = input_string.split()
    for table in tables:
        complete_table = f'{prefix}{table}'
        if complete_table not in table_check:
            print(f'{complete_table} is not a valid table')
            exit()
        elif complete_table in table_check:
            print(f"Tables to export {prefix}{table}")
            tables_with_prefix.append(f'{prefix}{table}')
    return tables_with_prefix
tables_to_drop = get_tables()

checks = False
while checks == False:
    input_check = input("Are the tables above correct?: [Y/N]")
    if input_check.upper() == "N":
        print("Let's try this again")
        tables_to_drop = get_tables()
    elif input_check.upper() == "Y":
        print("All good!")
        checks = True
    elif input_check.upper != "Y" and input_check.upper != "N":
        print("Bad input. I can only accept Y or N. To cancel the script use Ctrl + C")
        tables_to_drop = get_tables()

tables_check.stdout.close()

tables_join = ",".join(tables_to_drop)
tables_formatted = f"--tables={tables_join}"
filename = f'{prefix}to_update_staging.sql'
export_tables = subprocess.Popen(['wp', 'db', 'export', tables_formatted, filename], stdout=subprocess.PIPE)
export_check = export_tables.communicate()[0].decode('utf-8').strip()
print(export_check)

shutil.move(filename, f'../{stage_name}/')
print(f'File {filename} moved to {stage_name}. Changing directories.')
os.chdir(f'../{stage_name}')

tables_space = ", ".join(tables_to_drop)
drop = f'wp db query \"DROP TABLE {tables_space};\"'
drop_tables = subprocess.Popen([drop], shell=True, stdout=subprocess.PIPE)
print(f'Dropping tables {tables_space}')
drop_tables.stdout.close()

run_import = subprocess.Popen(['wp', 'db', 'import', filename], stdout=subprocess.PIPE)
import_check = run_import.communicate()[0].decode('utf-8').strip()
if import_check == f"Success: Imported from '{filename}'.":
    print(import_check, "You can publish from staging now!")
else:
    print(f"Could not import file. Don't ask me, I'm a script. \nError: \n {import_check}")
run_import.stdout.close()
