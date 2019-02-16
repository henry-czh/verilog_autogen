#!/usr/bin/env python
# -*- coding: UTF-8 -*- 

'''
    author: chaozhanghu
    email:  chaozhanghu@foxmail.com
    date:   2019.02.15
    version:1.0
    function: deal with strobe and data fields for partial access
'''
import sys
import xlrd

def gen_header(output_file,module_name):
    s = '''// This is an autuogen apb interface module
module %s(
    //clock and rst
    input clk,
    input rst_n,
    
    //apb4 register interface
    input [31:0]    paddr,
    input [31:0]    pwdata,
    input           pwrite,
    input           penable,
    input           psel,
    input           peable,
    input           pprot,
    output [31:0]   prdata,
    output          pready
);
'''
    s=s % (module_name)
    output_file.write(s)

def gen_wr(output_file):
    s = '''
wire pready;
wire [31:0] prdata;

assign pready=1;
assign reg_wr=penable & psel & pwrite;
assign reg_rd=penable & psel & ~pwrite;

always@(posedege clk)
if(~rst_n)
    p
'''
def deal_xls(sheet):
    book=xlrd.open_workbook(sys.argv[1])
    page=book.sheet_by_index(sheet)
    
    module_info = page.col_values(1)[0:4]

    regname= page.col_values(0)
    offset = page.col_values(1)
    reset  = page.col_values(2)
    access = page.col_values(3)
    hdl_path = page.col_values(4)
    reg_info = zip(regname[5:],offset[5:],reset[5:],access[5:],hdl_path[5:])
    return reg_info,module_info
    

if __name__=='__main__':
    reg_info=deal_xls(0)[0]
    module_info=deal_xls(0)[1]
    output_file=open('%s.v' % module_info[0],'w')
    gen_header(output_file,module_info[0])
    output_file.close()
