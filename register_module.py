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

def gen_main(output_file,reg_info):
    s = '''
reg pready;
reg [31:0] prdata;

assign reg_wr=penable & psel & pwrite;
assign reg_rd=penable & psel & ~pwrite;

always@(posedge clk)
if(~rst_n)
    pready <= 1'b0;
else if(penable & psel)
    pready <= 1'b1;
else
    pready <= 1'b0;

'''
    output_file.write(s)

    for data in reg_info:
        output_file.write('reg [31:0] %s;\n' % (data[0]))
    
    s='''
always@(posedge clk)
if(~rst_n) begin
'''
    output_file.write(s)
    
    for data in reg_info:
        if data[3].find('W'):
            output_file.write('\t%s <= \'h%s;\n' % (data[0],data[2].split('x')[1]))
    
    s='''end
else if(reg_wr) begin
    case(paddr)
'''
    output_file.write(s)
    
    for data in reg_info:
        if data[3].find('W'):
            output_file.write('\t32\'h%s: %s <= pwdata;\n' % (data[1].split('x')[1],data[0]))
    s='''    default:
    endcase
end 
'''
    output_file.write(s)
    
    s='''
always@(posedge clk)
if(~rst_n)
    prdata <= 'h0;
else if(reg_rd) begin
    case(paddr)
'''
    output_file.write(s)
    
    for data in reg_info:
        if data[3].find('R'):
            output_file.write('\t32\'h%s: prdata <= %s;\n' % (data[1].split('x')[1],data[0]))
    s='''    default:
    endcase
end 

endmodule
'''
    output_file.write(s)

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
    #print reg_info
    output_file=open('%s.v' % module_info[0],'w')
    gen_header(output_file,module_info[0])
    gen_main(output_file,reg_info)
    output_file.close()
