import dns.resolver
from ipwhois import IPWhois
import xlsxwriter
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, help='input file',dest="filename", required=True)
args = parser.parse_args()
path = Path(args.filename)

workbook = xlsxwriter.Workbook('output.xlsx') 
worksheet = workbook.add_worksheet()
counter = 2

worksheet.write('A1','Subdomain')
worksheet.write('B1','IP')
worksheet.write('C1','CIDR')
worksheet.write('D1','Asn')
worksheet.write('E1','Asn Registry')

f=open(path, 'r')
lines = f.readlines()

for subdomain in lines:
    str_counter = str(counter)
    counter += 1
    worksheet.write('A' + str_counter,subdomain.strip())
    try:
        cname = dns.resolver.resolve(subdomain.strip(), 'A')
        for i in cname.response.answer:
            for j in i.items:
                # 1 represents A record
                if j.rdtype != 1:
                    break
                ip=j.to_text()
                worksheet.write('B' + str_counter, ip)
                obj= IPWhois(ip)
                res= obj.lookup_whois()
                worksheet.write('C' + str_counter, res['asn_cidr'])
                worksheet.write('D' + str_counter, res['asn'])
                worksheet.write('E' + str_counter, res['asn_registry'])
    except dns.resolver.NXDOMAIN as err:
        #print("No A Record")
        pass
    except dns.resolver.NoAnswer as err:
        #print("No Answer")
        pass
workbook.close()

        



        
