import holidays
import datetime

def bank_statement_number(date):
    pl_holidays = []
    current_year = datetime.datetime.now().year
    for holiday in holidays.Poland(years=current_year).items():
        pl_holidays.append(holiday[0])

    current_day = datetime.datetime(day=int(date[0:2]), month=int(date[3:5]), year=int(date[6:])).date()
    number = 0
    start_date = datetime.date(current_year, 1, 1)
    delta = datetime.timedelta(days=1)
    while start_date <= current_day:
        if start_date in pl_holidays or start_date.isoweekday() == 6 or start_date.isoweekday() == 7:
            start_date += delta
            continue
        else:
            start_date += delta
            number += 1

    return str(number)


def extract_info(info="a b c d"):
    info = info.split(sep=' ')
    contactor = ""
    account_number = ""
    description = ""
    for cell in info:
        if len(cell) == 26:
            account_number = cell
        elif account_number == "":
            contactor = contactor + cell + " "
        else:
            description = description + cell + " "

    return contactor, account_number, description


def line_to_list(line):

    line = line.split(sep="\"")
    line[0] = line[0].strip(",")
    line.pop(-1)
    counter = line.count("")
    for i in range(counter):
        line.remove("")
    counter = line.count(",")
    for i in range(counter):
        line.remove(",")
    line[0] = line[0].strip(",")
    line[-3] = line[-3].replace('.', '').replace(',', '')
    line[-4] = line[-4].replace('.', '').replace(',', '')
    if '\ufeff' in line:
        line.remove('\ufeff')

    return line


def csv_to_mt940(mt940_file, csv_list):

    #variables
    account_number_IBAN = "PL08103000190109853000416691"
    date = csv_list[-1][0][8:10] + csv_list[-1][0][3:5] + csv_list[-1][0][0:2]
    beginning_balance = int(csv_list[-1][-3]) - int(csv_list[-1][-4])
    counter = 0

    #heather
    mt940_file.write(":20:" + date + "\n")
    mt940_file.write(":25:" + account_number_IBAN + "\n")
    mt940_file.write(":28C:" + bank_statement_number(csv_list[-1][0]) + "\n")
    mt940_file.write(":NS:22" + "PRZEDSIĘBIORSTWO PRODUKCYJNO-HANDLOWO-USŁUGOWE \"HAND\"\nSPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ " + "\n")
    mt940_file.write(":60F:C" + date + "PLN" + str(beginning_balance)[0:-2] + "," + str(beginning_balance)[-2:] + "\n")

    #operation block
    for line in reversed(csv_list):
        counter += 1
        if int(line[-4]) < 0:
            C_D = 'D'
            line[-4] = line[-4].strip("-")
        else:
            C_D = 'C'
        amount = line[-4][:-2] + "," + line[-4][-2:]
        nd_line = extract_info(line[1])
        mt940_file.write(":61:" + date + date[2:] + C_D + amount + "\n")
        mt940_file.write(":86:<10" + str(counter) + "\n")
        mt940_file.write("<20" + nd_line[2] + "\n")
        mt940_file.write("<27" + nd_line[0] + "\n")
        mt940_file.write("<30" + nd_line[1][2:8] + "\n")
        mt940_file.write("<31" + nd_line[1][8:26] + "\n")
        mt940_file.write("<38" + nd_line[1] + "\n")
    balance = csv_list[0][-3][:-2] + "," + csv_list[0][-3][-2:]
    mt940_file.write(":62F:C" + date + "PLN" + str(balance) + "\n")

    return None
