# File generator for instantiating the IOD blocks 
# The pattern is same as what you get with Libero
# Author: Dmitry Eliseev
# Version 1.0 
# 15.05.2019

import sys, getopt
from datetime import datetime


try:
	opts, args = getopt.getopt(sys.argv[1:],"hn:")
except getopt.GetoptError:
	print 'Usage: python deser_filegen.py -n <Number of IOs to be instantiated>'
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print 'Usage: python deser_filegen.py -n <Number of IOs to be instantiated>'
		sys.exit()
	elif opt == '-n':
		inp_number = int(arg)
	elif opt == '-c':
		print 'exiting...'
		sys.exit()
print 'Number of IOs to be implemented: ', inp_number


#----------- Generating ides_(NN)_PF_IOD_RX_PF_IOD.v

filename= 'ides_'+str(inp_number)+'_PF_IOD_RX_PF_IOD.v'
print 'Generating ', filename
f= open (filename,"w")

now = datetime.now()
date_time = "// Created: " + now.strftime("%d.%m.%Y, %H:%M:%S") +"\n"


f.write('`timescale 1 ns/100 ps\n')
f.write('// ')
f.write(filename)
f.write('\n// Automatically generated by deser_filegen.py (D.Eliseev)\n')
f.write(date_time)
f.write ("\n\n")

######  Module's ports ######
string = 'module ides_'+str(inp_number)+'_PF_IOD_RX_PF_IOD(\n' + \
		'       ARST_N, \n' + \
		'       RX_SYNC_RST, \n' + \
        '       TX_SYNC_RST, \n' + \
       	'       HS_IO_CLK, \n' + \
       	'       RX_DQS_90, \n' + \
       	'       FIFO_WR_PTR, \n' + \
  	    '       FIFO_RD_PTR, \n' + \
        '       EYE_MONITOR_LANE_WIDTH, \n'

for i in range (0, inp_number):
	string += "       EYE_MONITOR_CLEAR_FLAGS_"+str(i)+", \n"

for i in range (0, inp_number):
	string += "       DELAY_LINE_MOVE_"+str(i)+", \n"
	
for i in range (0, inp_number):
	string += "       DELAY_LINE_DIRECTION_"+str(i)+", \n"
	
for i in range (0, inp_number):
	string += "       DELAY_LINE_LOAD_"+str(i)+", \n"
	
for i in range (0, inp_number):
	string += "       DELAY_LINE_OUT_OF_RANGE_"+str(i)+", \n"	

string += "       FAB_CLK, \n"	

for i in range (0, inp_number):
	string += "       EYE_MONITOR_EARLY_"+str(i)+", \n"
	
for i in range (0, inp_number):
	string += "       EYE_MONITOR_LATE_"+str(i)+", \n"	
	
for i in range (0, inp_number):
	string += "       RX_DATA_"+str(i)+", \n"	
	
string += "       PAD_I, \n"
	
for i in range (0, inp_number-1):
	string += "       ODT_EN_"+str(i)+", \n"
	
string += "       ODT_EN_"+str(inp_number-1)+" \n    ); \n"
	
f.write(string);	

######  IO description ######
string ='input ARST_N; \n' + \
		'input RX_SYNC_RST; \n' + \
		'input TX_SYNC_RST; \n' + \
		'input  [0:0] HS_IO_CLK; \n' + \
		'input  [0:0] RX_DQS_90; \n' + \
		'input  [2:0] FIFO_WR_PTR; \n' + \
		'input  [2:0] FIFO_RD_PTR; \n' + \
		'input  [2:0] EYE_MONITOR_LANE_WIDTH; \n' 

for i in range (0, inp_number):
	string += 'input  EYE_MONITOR_CLEAR_FLAGS_'+str(i)+'; \n'

for i in range (0, inp_number):
	string += "input  DELAY_LINE_MOVE_"+str(i)+"; \n"
	
for i in range (0, inp_number):
	string += "input  DELAY_LINE_DIRECTION_"+str(i)+"; \n"
	
for i in range (0, inp_number):
	string += "input  DELAY_LINE_LOAD_"+str(i)+"; \n"
	
for i in range (0, inp_number):
	string += "output DELAY_LINE_OUT_OF_RANGE_"+str(i)+"; \n"	

string += "input  FAB_CLK; \n"	

for i in range (0, inp_number):
	string += "output EYE_MONITOR_EARLY_"+str(i)+"; \n"
	
for i in range (0, inp_number):
	string += "output EYE_MONITOR_LATE_"+str(i)+"; \n"	
	
for i in range (0, inp_number):
	string += "output [9:0] RX_DATA_"+str(i)+"; \n"	
	
string += 'input  ['+str(inp_number-1)+':0] PAD_I; \n'
	
for i in range (0, inp_number):
	string += 'input  ODT_EN_'+str(i)+'; \n'

f.write(string);	


######  Signals descr ######
string='\nwire GND_net, VCC_net, \n'

for i in range (0, inp_number-1):
	string += '    Y_I_INBUF_'+str(i)+'_net, \n'
	
string += '    Y_I_INBUF_'+str(i+1)+'_net;\n'

f.write(string);
	
######  INBUF instantiations ######
string = '\n'
for i in range (0, inp_number):
	string +='    INBUF I_INBUF_'+str(i)+' (.PAD(PAD_I['+str(i)+']),' +'.Y(Y_I_INBUF_'+str(i)+'_net));\n'	
f.write(string);	

######  VCC GND instantiations ######
string = '\n'
string+='    VCC vcc_inst (.Y(VCC_net));\n'	
string+='    GND gnd_inst (.Y(GND_net));\n'	
f.write(string);	

######  IODs instantiations ######
for i in range (0, inp_number):
	string ='\n    IOD #(  .DATA_RATE(1200.0), \n' + \
		'            .FORMAL_NAME(\"RXD%STATIC_DELAY\"), \n' + \
		'            .INTERFACE_NAME(\"RX_DDRX_B_G_DYN\"), \n' + \
		'            .DELAY_LINE_SIMULATION_MODE(\"DISABLED\"), \n' + \
		'            .RESERVED_0(1\'b0), \n' + \
		'            .RX_CLK_EN(1\'b1), \n' + \
		'            .RX_CLK_INV(1\'b0), \n' + \
		'            .TX_CLK_EN(1\'b0), \n' + \
		'            .TX_CLK_INV(1\'b0), \n' + \
		'            .HS_IO_CLK_SEL(3\'b000), \n' + \
		'            .QDR_EN(1\'b0), \n' + \
		'            .EDGE_DETECT_EN(1\'b0), \n' + \
		'            .DELAY_LINE_MODE(2\'b01), \n' + \
		'            .RX_MODE(4\'b1101), \n' + \
		'            .EYE_MONITOR_MODE(1\'b0), \n' + \
		'            .DYN_DELAY_LINE_EN(1\'b1), \n' + \
		'            .FIFO_WR_EN(1\'b1), \n' + \
		'            .EYE_MONITOR_EN(1\'b1), \n' + \
		'            .TX_MODE(7\'b0000000), \n' + \
		'            .TX_CLK_SEL(2\'b00), \n' + \
		'            .TX_OE_MODE(3\'b111), \n' + \
		'            .TX_OE_CLK_INV(1\'b0), \n' + \
		'            .RX_DELAY_VAL(8\'b00000001), \n' + \
		'            .RX_DELAY_VAL_X2(1\'b0), \n' + \
		'            .TX_DELAY_VAL(8\'b00000001), \n' + \
		'            .EYE_MONITOR_WIDTH(3\'b001), \n' + \
		'            .EYE_MONITOR_WIDTH_SRC(1\'b1), \n' + \
		'            .RESERVED_1(1\'b0), \n' + \
		'            .DISABLE_LANECTRL_RESET(1\'b0), \n' + \
		'            .INPUT_DELAY_SEL(2\'b00), \n' + \
		'            .OEFF_EN_INV(1\'b0), \n' + \
		'            .INFF_EN_INV(1\'b0), \n' + \
		'            .OUTFF_EN_INV(1\'b0) ) \n'
	f.write(string)
	string='    I_IOD_' + str(i)+' (\n'+ \
        '            .EYE_MONITOR_EARLY(EYE_MONITOR_EARLY_'+str(i)+'),\n' + \
        '            .EYE_MONITOR_LATE(EYE_MONITOR_LATE_'+str(i)+'),\n' + \
        '            .RX_DATA({' 
	for k in range (9, 0, -1):
		string+= 'RX_DATA_'+str(i)+'['+str(k)+'], '
	string+= 'RX_DATA_'+str(i)+'[0]}), \n'
	string+='            .DELAY_LINE_OUT_OF_RANGE(DELAY_LINE_OUT_OF_RANGE_'+str(i)+'),\n' 
	string+='            .TX_DATA({GND_net, GND_net, GND_net, GND_net, GND_net, GND_net, GND_net, GND_net}),\n'
	string+='            .OE_DATA({GND_net, GND_net, GND_net, GND_net}),\n' 
	string+='            .RX_BIT_SLIP(GND_net),\n' 
	string+='            .EYE_MONITOR_CLEAR_FLAGS(EYE_MONITOR_CLEAR_FLAGS_'+str(i)+'),\n' 
	string+='            .DELAY_LINE_MOVE(DELAY_LINE_MOVE_'+str(i)+'),\n'
	string+='            .DELAY_LINE_DIRECTION(DELAY_LINE_DIRECTION_'+str(i)+'),\n' 
	string+='            .DELAY_LINE_LOAD(DELAY_LINE_LOAD_'+str(i)+'),\n' 
	string+='            .RX_CLK(FAB_CLK),\n'
	string+='            .TX_CLK(GND_net),\n' 
	string+='            .ODT_EN(ODT_EN_0),\n' 
	string+='            .INFF_SL(GND_net),\n' 
	string+='            .INFF_EN(GND_net),\n' 
	string+='            .OUTFF_SL(GND_net),\n' 
	string+='            .OUTFF_EN(GND_net),\n' 
	string+='            .AL_N(GND_net),\n' 
	string+='            .OEFF_LAT_N(GND_net),\n' 
	string+='            .OEFF_SD_N(GND_net),\n' 
	string+='            .OEFF_AD_N(),\n' 
	string+='            .INFF_LAT_N(GND_net),\n' 
	string+='            .INFF_SD_N(GND_net),\n' 
	string+='            .INFF_AD_N(GND_net),\n' 	
	string+='            .OUTFF_LAT_N(GND_net),\n' 
	string+='            .OUTFF_SD_N(GND_net),\n' 
	string+='            .OUTFF_AD_N(),\n' 
	string+='            .RX_P(Y_I_INBUF_'+str(i)+'_net),\n' 
	string+='            .RX_N(),\n' 
	string+='            .TX_DATA_9(GND_net),\n'
	string+='            .TX_DATA_8(GND_net),\n' 
	string+='            .ARST_N(ARST_N),\n' 
	string+='            .RX_SYNC_RST(RX_SYNC_RST),\n' 
	string+='            .TX_SYNC_RST(TX_SYNC_RST),\n' 
	string+='            .HS_IO_CLK({GND_net, GND_net, GND_net, GND_net, GND_net, HS_IO_CLK[0]}),\n' 
	string+='            .RX_DQS_90({GND_net, RX_DQS_90[0]}), \n'
	string+='            .TX_DQS(GND_net),\n' 
	string+='            .TX_DQS_270(GND_net),\n' 
	string+='            .FIFO_WR_PTR({FIFO_WR_PTR[2], FIFO_WR_PTR[1], FIFO_WR_PTR[0]}),\n'
	string+='            .FIFO_RD_PTR({FIFO_RD_PTR[2], FIFO_RD_PTR[1], FIFO_RD_PTR[0]}),\n' 
	string+='            .TX(),\n'
	string+='            .OE(),\n' 
	string+='            .CDR_CLK(GND_net),\n' 
	string+='            .CDR_NEXT_CLK(GND_net),\n' 
	string+='            .EYE_MONITOR_LANE_WIDTH({EYE_MONITOR_LANE_WIDTH[2], EYE_MONITOR_LANE_WIDTH[1], EYE_MONITOR_LANE_WIDTH[0]}),\n' 
	string+='            .DDR_DO_READ(),\n' 
	string+='            .CDR_CLK_A_SEL_8(),\n' 
	string+='            .CDR_CLK_A_SEL_9(),\n' 
	string+='            .CDR_CLK_A_SEL_10(),\n' 
	string+='            .CDR_CLK_B_SEL({'
	for k in range (0, 10):
		string+='nc'+str(i*11+k)+', '
	string+='nc'+str(i*11+10)+'}),\n'
	string+='            .SWITCH(),\n' 
	string+='            .CDR_CLR_NEXT_CLK_N(),\n'
	string+='            .TX_DATA_OUT_9(),\n'
	string+='            .TX_DATA_OUT_8(),\n'
	string+='            .AL_N_OUT(),\n'
	string+='            .OUTFF_SL_OUT(),\n' 
	string+='            .OUTFF_EN_OUT(),\n'
	string+='            .INFF_SL_OUT(),\n' 
	string+='            .INFF_EN_OUT(),\n' 
	string+='            .RX_CLK_OUT(),\n' 
	string+='            .TX_CLK_OUT());\n'
	f.write(string)

f.write ('endmodule\n');
f.close()
print 'Done.'




#----------- Generating ides_(NN).v

filename= 'ides_'+str(inp_number)+'.v'
print 'Generating ', filename
f= open (filename,"w")


f.write('// ')
f.write(filename)
f.write('\n// Automatically generated by deser_filegen.py (D.Eliseev)\n')
now = datetime.now()
date_time = '// Timestamp: ' + now.strftime("%d.%m.%Y, %H:%M:%S") +'\n'
f.write(date_time)
f.write('\n`timescale 1 ns/100 ps\n\n')

######  Module's ports ######
f.write('// ides_')
f.write(str(inp_number))
f.write('\n')
string = 'module ides_'+str(inp_number)+'(\n' + \
		'       ARST_N, \n' + \
		'       DELAY_LINE_DIRECTION, \n' + \
		'       DELAY_LINE_LOAD, \n' + \
		'       DELAY_LINE_MOVE, \n' + \
		'       EYE_MONITOR_CLEAR_FLAGS, \n' + \
		'       EYE_MONITOR_WIDTH, \n' + \
		'       HS_IO_CLK_PAUSE, \n' + \
		'       RXD, \n' + \
		'       RX_CLK, \n' + \
		'       DELAY_LINE_OUT_OF_RANGE,\n' + \
		'       EYE_MONITOR_EARLY,\n' + \
		'       EYE_MONITOR_LATE,\n'

for i in range (0, inp_number):
	string += '       L'+str(i)+'_RXD_DATA, \n'
string += '       RX_CLK_G \n);\n\n'
f.write(string)


string='input         ARST_N;\n'
string+='input  ['+str(inp_number-1)+':0] DELAY_LINE_DIRECTION;\n'
string+='input  ['+str(inp_number-1)+':0] DELAY_LINE_LOAD;\n'
string+='input  ['+str(inp_number-1)+':0] DELAY_LINE_MOVE;\n'
string+='input  ['+str(inp_number-1)+':0] EYE_MONITOR_CLEAR_FLAGS;\n'
string+='input  [2:0]  EYE_MONITOR_WIDTH;\n'
string+='input         HS_IO_CLK_PAUSE;\n'
string+='input  ['+str(inp_number-1)+':0] RXD;\n'
string+='input         RX_CLK;\n'

string+='output ['+str(inp_number-1)+':0] DELAY_LINE_OUT_OF_RANGE;\n'
string+='output ['+str(inp_number-1)+':0] EYE_MONITOR_EARLY;\n'
string+='output ['+str(inp_number-1)+':0] EYE_MONITOR_LATE;\n'
for i in range (0, inp_number):
	string+='output [9:0]  L'+str(i)+'_RXD_DATA;\n'
string+='output        RX_CLK_G;\n'
f.write(string)


######  IO description ######
string = 'input         ARST_N;\n'
string += 'input  ['+str(inp_number-1)+':0] DELAY_LINE_DIRECTION;\n'
string += 'input  ['+str(inp_number-1)+':0] DELAY_LINE_LOAD;\n'
string += 'input  ['+str(inp_number-1)+':0] DELAY_LINE_MOVE;\n'
string += 'input  ['+str(inp_number-1)+':0] EYE_MONITOR_CLEAR_FLAGS;\n'
string += 'input  [2:0]  EYE_MONITOR_WIDTH;\n'
string += 'input         HS_IO_CLK_PAUSE;\n'
string += 'input  ['+str(inp_number-1)+':0] RXD;\n'
string += 'input         RX_CLK;\n\n'

string += 'output ['+str(inp_number-1)+':0] DELAY_LINE_OUT_OF_RANGE;\n'
string += 'output ['+str(inp_number-1)+':0] EYE_MONITOR_EARLY;\n'
string += 'output ['+str(inp_number-1)+':0] EYE_MONITOR_LATE;\n'
for i in range (0, inp_number):
	string += 'output [9:0]  L'+str(i)+'_RXD_DATA;\n'
string += 'output        RX_CLK_G;\n\n'


######  Nets ######
string =  'wire           ARST_N;\n'
string += 'wire           CLK_0_Y;\n'
for i in range (0, inp_number):
	string += 'wire   ['+str(i)+':'+str(i)+'] DELAY_LINE_DIRECTION_slice_'+str(i)+';\n'

for i in range (0, inp_number):
	string += 'wire   ['+str(i)+':'+str(i)+'] DELAY_LINE_LOAD_slice_'+str(i)+';\n'

for i in range (0, inp_number):
	string += 'wire   ['+str(i)+':'+str(i)+'] DELAY_LINE_MOVE_slice_'+str(i)+';\n'
	
string+= 'wire           DELAY_LINE_OUT_OF_RANGE_net_0;\n'
for i in range (0, inp_number-1):
	string += 'wire           DELAY_LINE_OUT_OF_RANGE_'+str(i)+';\n'

for i in range (0, inp_number):
	string += 'wire   ['+str(i)+':'+str(i)+'] EYE_MONITOR_CLEAR_FLAGS_slice_'+str(i)+';\n'

string+= 'wire           EYE_MONITOR_EARLY_net_0;\n'
for i in range (0, inp_number-1):
	string += 'wire           EYE_MONITOR_EARLY_'+str(i)+';\n'

string+= 'wire           EYE_MONITOR_LATE_net_0;\n'
for i in range (0, inp_number-1):
	string += 'wire           EYE_MONITOR_LATE_'+str(i)+';\n'

string+= 'wire   [2:0]   EYE_MONITOR_WIDTH; \n'
string+= 'wire           HS_IO_CLK_CASCADED_Y; \n'
string+= 'wire           HS_IO_CLK_FIFO_Y; \n'
string+= 'wire           HS_IO_CLK_PAUSE; \n'
string+= 'wire           HS_IO_CLK_RX_Y; \n'

for i in range (0, inp_number):
	string += 'wire   [9:0] L'+str(i)+'_RXD_DATA_net_0;\n'

string+= 'wire           PF_CLK_DIV_FIFO_CLK_DIV_OUT; \n'
string+= 'wire           PF_CLK_DIV_FIFO_CLK_OUT;\n'
string+= 'wire           PF_CLK_DIV_RXCLK_CLK_OUT;\n'
string+= 'wire           PF_LANECTRL_0_ARST_N;\n'
string+= 'wire   [2:0]   PF_LANECTRL_0_EYE_MONITOR_WIDTH_OUT;\n'
string+= 'wire   [2:0]   PF_LANECTRL_0_FIFO_RD_PTR;\n'
string+= 'wire   [2:0]   PF_LANECTRL_0_FIFO_WR_PTR;\n'
string+= 'wire   [0:0]   PF_LANECTRL_0_RX_DQS_90;\n'
string+= 'wire           PF_LANECTRL_0_RX_SYNC_RST;\n'
string+= 'wire           PF_LANECTRL_0_TX_SYNC_RST;\n'
string+= 'wire           RX_CLK;\n'
string+= 'wire           RX_CLK_G_net_0;\n'
string+= 'wire   ['+str(inp_number-1)+':0]  RXD;\n'
for i in range (0, inp_number):
	string += 'wire   [9:0] L'+str(i)+'_RXD_DATA_net_1;\n'
string+= 'wire           RX_CLK_G_net_1;\n'
string+= 'wire   [0:0]   EYE_MONITOR_EARLY_net_1;\n'
for i in range (0, inp_number-1):
	string += 'wire   ['+str(i+1)+':'+str(i+1)+']  EYE_MONITOR_EARLY_'+str(i)+'_net_0;\n' 

string+= 'wire   [0:0]   EYE_MONITOR_LATE_net_1;\n'
for i in range (0, inp_number-1):
	string += 'wire   ['+str(i+1)+':'+str(i+1)+']  EYE_MONITOR_LATE_'+str(i)+'_net_0;\n' 

string+= 'wire   [0:0]   DELAY_LINE_OUT_OF_RANGE_net_1;\n'
for i in range (0, inp_number-1):
	string += 'wire   ['+str(i+1)+':'+str(i+1)+']  DELAY_LINE_OUT_OF_RANGE_'+str(i)+'_net_0;\n' 
	
string+= 'wire   [1:0]   HS_IO_CLK_net_0;\n'
string+= 'wire   ['+str(inp_number-1)+':0]  EYE_MONITOR_CLEAR_FLAGS;\n'
string+= 'wire   ['+str(inp_number-1)+':0]  DELAY_LINE_MOVE;\n'
string+= 'wire   ['+str(inp_number-1)+':0]  DELAY_LINE_DIRECTION;\n'
string+= 'wire   ['+str(inp_number-1)+':0]  DELAY_LINE_LOAD;\n'
f.write (string)

string = 'wire           GND_net;\n'
for i in range (0, 64):
	string += 'wire   [9:0]   TX_DATA_'+str(i)+'_const_net_0;\n'
for i in range (0, 64):
	string += 'wire   [3:0]   OE_DATA_'+str(i)+'_const_net_0;\n'
	
string+='wire   ['+str(inp_number-1)+':0]  PAD_const_net_0;\n'
string+='wire   ['+str(inp_number-1)+':0]  PAD_N_const_net_0;\n'
string+='wire   ['+str(inp_number-1)+':0]  PAD_I_N_const_net_0;\n'
string+='wire   [7:0]   DLL_CODE_const_net_0;\n'
string+='wire   [2:0]   READ_CLK_SEL_const_net_0;\n'
string+='wire   [7:0]   CDR_CLK_A_SEL_const_net_0;\n'
string+='wire           VCC_net;\n'
string+='wire   [10:0]  CDR_CLK_B_SEL_const_net_0;\n'
string+='wire           RESET_IN_POST_INV0_0;\n'
f.write (string)

# Constant assignments
string='assign GND_net                   = 1\'b0;\n'
for i in range (0, 64):
	string += 'assign TX_DATA_'+str(i)+'_const_net_0     = 10\'h000;\n'
for i in range (0, 64):
	string += 'assign OE_DATA_'+str(i)+'_const_net_0     = 4\'h0;\n'
	
#find out how many 4-bit words can be fitted in the input bus
SymbolsNo = inp_number//4
InitZerosString =str(inp_number)+'\'h0'
for i in range (0, SymbolsNo):
	InitZerosString += '0'
	
# proceed with constants assignment
string+='assign PAD_const_net_0           = '+InitZerosString+';\n'
string+='assign PAD_N_const_net_0         = '+InitZerosString+';\n'
string+='assign PAD_I_N_const_net_0       = '+InitZerosString+';\n'
string+='assign DLL_CODE_const_net_0      = 8\'h00;\n'
string+='assign READ_CLK_SEL_const_net_0  = 3\'h0;\n'
string+='assign CDR_CLK_A_SEL_const_net_0 = 8\'h00;\n'
string+='assign VCC_net                   = 1\'b1;\n'
string+='assign CDR_CLK_B_SEL_const_net_0 = 11\'h000;\n'	
string+='assign RESET_IN_POST_INV0_0 = ~ ARST_N;\n'


for i in range (0, inp_number):
	string += 'assign L'+str(i)+'_RXD_DATA_net_1                    = L'+str(i)+'_RXD_DATA_net_0;\n'
	string += 'assign L'+str(i)+'_RXD_DATA[9:0]                     = L'+str(i)+'_RXD_DATA_net_1;\n'

string += 'assign RX_CLK_G_net_1                       = RX_CLK_G_net_0;\n'
string += 'assign RX_CLK_G                             = RX_CLK_G_net_1;\n'	
f.write (string)

string = 'assign EYE_MONITOR_EARLY_net_1[0]           = EYE_MONITOR_EARLY_net_0;\n'
string+='assign EYE_MONITOR_EARLY[0:0]               = EYE_MONITOR_EARLY_net_1[0];\n'
for i in range (0, inp_number-1):
	string += 'assign EYE_MONITOR_EARLY_'+str(i)+'_net_0['+str(i+1)+']         = EYE_MONITOR_EARLY_'+str(i)+';\n'
	string += 'assign EYE_MONITOR_EARLY['+str(i+1)+':'+str(i+1)+']               = EYE_MONITOR_EARLY_'+str(i)+'_net_0['+str(i+1)+'];\n'

string+= 'assign EYE_MONITOR_LATE_net_1[0]            = EYE_MONITOR_LATE_net_0;\n'
string+='assign EYE_MONITOR_LATE[0:0]                = EYE_MONITOR_LATE_net_1[0];\n'
for i in range (0, inp_number-1):
	string += 'assign EYE_MONITOR_LATE_'+str(i)+'_net_0['+str(i+1)+']         = EYE_MONITOR_LATE_'+str(i)+';\n'
	string += 'assign EYE_MONITOR_LATE['+str(i+1)+':'+str(i+1)+']               = EYE_MONITOR_LATE_'+str(i)+'_net_0['+str(i+1)+'];\n'

string+= 'assign DELAY_LINE_OUT_OF_RANGE_net_1[0]     = DELAY_LINE_OUT_OF_RANGE_net_0;\n'
string+='assign DELAY_LINE_OUT_OF_RANGE[0:0]         = DELAY_LINE_OUT_OF_RANGE_net_1[0];\n'
for i in range (0, inp_number-1):
	string += 'assign DELAY_LINE_OUT_OF_RANGE_'+str(i)+'_net_0['+str(i+1)+']         = DELAY_LINE_OUT_OF_RANGE_'+str(i)+';\n'
	string += 'assign DELAY_LINE_OUT_OF_RANGE['+str(i+1)+':'+str(i+1)+']               = DELAY_LINE_OUT_OF_RANGE_'+str(i)+'_net_0['+str(i+1)+'];\n'


for i in range (0, inp_number):
	string += 'assign DELAY_LINE_DIRECTION_slice_'+str(i)+'['+str(i)+']      = DELAY_LINE_DIRECTION['+str(i)+':'+str(i)+'];\n'

for i in range (0, inp_number):
	string += 'assign DELAY_LINE_LOAD_slice_'+str(i)+'['+str(i)+']      = DELAY_LINE_LOAD['+str(i)+':'+str(i)+'];\n'

for i in range (0, inp_number):
	string += 'assign DELAY_LINE_MOVE_slice_'+str(i)+'['+str(i)+']      = DELAY_LINE_MOVE['+str(i)+':'+str(i)+'];\n'
	
for i in range (0, inp_number):
	string += 'assign EYE_MONITOR_CLEAR_FLAGS_slice_'+str(i)+'['+str(i)+']      = EYE_MONITOR_CLEAR_FLAGS['+str(i)+':'+str(i)+'];\n'

string+='assign HS_IO_CLK_net_0 = { HS_IO_CLK_RX_Y , HS_IO_CLK_FIFO_Y };\n'
f.write (string)

###### Component instances ######

string='\n'
string+= '//--------INBUF\n'
string+='INBUF CLK_0(\n'
string+='        .PAD ( RX_CLK ),\n'
string+='        .Y   ( CLK_0_Y )\n' 
string+='        );\n'
f.write (string)

string='\n'
string+= '//--------CLKINT\n'
string+='CLKINT CLKINT_0(\n'
string+='        .A ( PF_CLK_DIV_FIFO_CLK_DIV_OUT ),\n'
string+='        .Y ( RX_CLK_G_net_0 )\n' 
string+='        );\n'
f.write (string)

string='\n'
string+='//--------HS_IO_CLK\n'
string+='HS_IO_CLK HS_IO_CLK_CASCADED(\n'
string+='        .A ( CLK_0_Y ),\n'
string+='        .Y ( HS_IO_CLK_CASCADED_Y )\n' 
string+='        );\n'
f.write (string)

string='\n'
string+='//--------HS_IO_CLK\n'
string+='HS_IO_CLK HS_IO_CLK_FIFO(\n'
string+='        .A ( PF_CLK_DIV_FIFO_CLK_OUT ),\n'
string+='        .Y ( HS_IO_CLK_FIFO_Y ) \n'
string+='        );\n'
f.write (string)

string='\n'
string+='//--------HS_IO_CLK\n'
string+='HS_IO_CLK HS_IO_CLK_RX(\n'
string+='        .A ( PF_CLK_DIV_RXCLK_CLK_OUT ),\n'
string+='        .Y ( HS_IO_CLK_RX_Y )\n' 
string+='        );\n'
f.write(string)

string='\n'
string+='//--------ides_'+str(inp_number)+'_PF_CLK_DIV_FIFO_PF_CLK_DIV_DELAY\n'
string+='ides_'+str(inp_number)+'_PF_CLK_DIV_FIFO_PF_CLK_DIV_DELAY PF_CLK_DIV_FIFO(\n'
string+='        .CLK_IN      ( HS_IO_CLK_CASCADED_Y ),\n'
string+='        .CLK_OUT     ( PF_CLK_DIV_FIFO_CLK_OUT ),\n'
string+='        .CLK_DIV_OUT ( PF_CLK_DIV_FIFO_CLK_DIV_OUT )\n' 
string+='        );\n'
f.write(string)

string='\n'
string+='//--------ides_'+str(inp_number)+'_PF_CLK_DIV_RXCLK_PF_CLK_DIV_DELAY \n'
string+='ides_'+str(inp_number)+'_PF_CLK_DIV_RXCLK_PF_CLK_DIV_DELAY PF_CLK_DIV_RXCLK(\n'
string+='        .CLK_IN      ( HS_IO_CLK_CASCADED_Y ),\n'
string+='        .CLK_OUT     ( PF_CLK_DIV_RXCLK_CLK_OUT ),\n'
string+='        .CLK_DIV_OUT (  ) \n'
string+='        );\n'
f.write(string)

string='\n'
string+= '//--------ides_'+str(inp_number)+'_PF_IOD_RX_PF_IOD\n'
string+='ides_'+str(inp_number)+'_PF_IOD_RX_PF_IOD PF_IOD_RX(\n'
string+='        .ARST_N                     ( PF_LANECTRL_0_ARST_N ),\n'
string+='        .RX_SYNC_RST                ( PF_LANECTRL_0_RX_SYNC_RST ),\n'
string+='        .TX_SYNC_RST                ( PF_LANECTRL_0_TX_SYNC_RST ),\n'
string+='        .HS_IO_CLK                  ( HS_IO_CLK_FIFO_Y ),\n'
string+='        .RX_DQS_90                  ( PF_LANECTRL_0_RX_DQS_90 ),\n'
string+='        .FIFO_WR_PTR                ( PF_LANECTRL_0_FIFO_WR_PTR ),\n'
string+='        .FIFO_RD_PTR                ( PF_LANECTRL_0_FIFO_RD_PTR ),\n'
string+='        .EYE_MONITOR_LANE_WIDTH     ( PF_LANECTRL_0_EYE_MONITOR_WIDTH_OUT ),\n'
for i in range (0, inp_number):
	string+='        .EYE_MONITOR_CLEAR_FLAGS_'+str(i)+' ( EYE_MONITOR_CLEAR_FLAGS_slice_'+str(i)+' ),\n'
for i in range (0, inp_number):
	string+='        .DELAY_LINE_MOVE_'+str(i)+' ( DELAY_LINE_MOVE_slice_'+str(i)+' ),\n'
for i in range (0, inp_number):
	string+='        .DELAY_LINE_DIRECTION_'+str(i)+' ( DELAY_LINE_DIRECTION_slice_'+str(i)+' ),\n'
for i in range (0, inp_number):
	string+='        .DELAY_LINE_LOAD_'+str(i)+' ( DELAY_LINE_LOAD_slice_'+str(i)+' ),\n'	
string+='        .FAB_CLK                    ( RX_CLK_G_net_0 ),\n'
string+='        .PAD_I                      ( RXD ),\n'
for i in range (0, inp_number):
	string+='        .ODT_EN_'+str(i)+'                   ( GND_net ),\n'
string+='        .DELAY_LINE_OUT_OF_RANGE_0  ( DELAY_LINE_OUT_OF_RANGE_net_0 ),\n'
for i in range (1, inp_number):
	string+='        .DELAY_LINE_OUT_OF_RANGE_'+str(i)+' (DELAY_LINE_OUT_OF_RANGE_'+str(i-1)+' ),\n'	
string+='        .EYE_MONITOR_EARLY_0        ( EYE_MONITOR_EARLY_net_0 ),\n'
for i in range (1, inp_number):
	string+='        .EYE_MONITOR_EARLY_'+str(i)+'        ( EYE_MONITOR_EARLY_'+str(i-1)+' ),\n'
string+='        .EYE_MONITOR_LATE_0        ( EYE_MONITOR_LATE_net_0 ),\n'
for i in range (1, inp_number):
	string+='        .EYE_MONITOR_LATE_'+str(i)+'        ( EYE_MONITOR_LATE_'+str(i-1)+' ),\n'	
for i in range (0, inp_number-1):
	string+='        .RX_DATA_'+str(i)+'        ( L'+str(i)+'_RXD_DATA_net_0 ),\n'	
string+='        .RX_DATA_'+str(inp_number-1)+'        ( L'+str(inp_number-1)+'_RXD_DATA_net_0 )\n'	
string+='        );\n'	
f.write(string)

string='\n'
string+='//--------ides_'+str(inp_number)+'_PF_LANECTRL_0_PF_LANECTRL\n'
string+='ides_'+str(inp_number)+'_PF_LANECTRL_0_PF_LANECTRL PF_LANECTRL_0(\n'
string+='        .HS_IO_CLK                  ( HS_IO_CLK_net_0 ),\n'
string+='        .DLL_CODE                   ( DLL_CODE_const_net_0 ),\n'
string+='        .FAB_CLK                    ( RX_CLK_G_net_0 ),\n'
string+='        .RESET                      ( RESET_IN_POST_INV0_0 ),\n'
string+='        .DELAY_LINE_SEL             ( GND_net ),\n'
string+='        .DELAY_LINE_LOAD            ( GND_net ),\n' 
string+='        .DELAY_LINE_DIRECTION       ( GND_net ),\n' 
string+='        .DELAY_LINE_MOVE            ( GND_net ),\n' 
string+='        .HS_IO_CLK_PAUSE            ( HS_IO_CLK_PAUSE ),\n'
string+='        .EYE_MONITOR_WIDTH_IN       ( EYE_MONITOR_WIDTH ),\n'
string+='        .EYE_MONITOR_WIDTH_OUT      ( PF_LANECTRL_0_EYE_MONITOR_WIDTH_OUT ),\n'
string+='        .RX_DQS_90                  ( PF_LANECTRL_0_RX_DQS_90 ),\n'
string+='        .TX_DQS                     (  ),\n'
string+='        .TX_DQS_270                 (  ),\n'
string+='        .FIFO_WR_PTR                ( PF_LANECTRL_0_FIFO_WR_PTR ),\n'
string+='        .FIFO_RD_PTR                ( PF_LANECTRL_0_FIFO_RD_PTR ),\n'
string+='        .ARST_N                     ( PF_LANECTRL_0_ARST_N ),\n'
string+='        .RX_SYNC_RST                ( PF_LANECTRL_0_RX_SYNC_RST ),\n'
string+='        .TX_SYNC_RST                ( PF_LANECTRL_0_TX_SYNC_RST ),\n'
string+='        .RX_DELAY_LINE_OUT_OF_RANGE (  ),\n'
string+='        .TX_DELAY_LINE_OUT_OF_RANGE (  ),\n'
string+='        .A_OUT_RST_N                (  ) \n'
string+='        );\n'
f.write(string)



f.write ('\nendmodule\n')
f.close()
print 'Done.'


#----------- Generating ides_(NN)_PF_CLK_DIV_FIFO_PF_CLK_DIV_DELAY.v and ides_(NN)_PF_CLK_DIV_RXCLK_PF_CLK_DIV_DELAY.v

filename_divfifo = 'ides_'+str(inp_number)+'_PF_CLK_DIV_FIFO_PF_CLK_DIV_DELAY.v'
filename_divrxclk= 'ides_'+str(inp_number)+'_PF_CLK_DIV_RXCLK_PF_CLK_DIV_DELAY.v'
print 'Generating ', filename_divfifo, ' and ', filename_divrxclk

f1= open (filename_divfifo,"w")
f1.write('// ')
f1.write(filename_divfifo)
f1.write('\n// Automatically generated by deser_filegen.py (D.Eliseev)\n')
now = datetime.now()
date_time = '// Timestamp: ' + now.strftime("%d.%m.%Y, %H:%M:%S") +'\n'
f1.write(date_time)
f1.write('\n`timescale 1 ns/100 ps\n\n')
string='module ides_'+str(inp_number)+'_PF_CLK_DIV_FIFO_PF_CLK_DIV_DELAY(\n'
f1.write(string)

f2= open (filename_divrxclk,"w")
f2.write('// ')
f2.write(filename_divrxclk)
f2.write('\n// Automatically generated by deser_filegen.py (D.Eliseev)\n')
now = datetime.now()
date_time = '// Timestamp: ' + now.strftime("%d.%m.%Y, %H:%M:%S") +'\n'
f2.write(date_time)
f2.write('\n`timescale 1 ns/100 ps\n\n')
string='module ides_'+str(inp_number)+'_PF_CLK_DIV_RXCLK_PF_CLK_DIV_DELAY(\n'
f2.write(string)

string='       CLK_IN,\n'
string+='       CLK_OUT,\n'
string+='       CLK_DIV_OUT\n'
string+='    );\n'
string+='input  CLK_IN;\n'
string+='output CLK_OUT;\n'
string+='output CLK_DIV_OUT;\n\n'
string+='    wire GND_net, VCC_net;\n\n'
string+='    ICB_CLKDIVDELAY #(\n'
string+='        .DIVIDER(3\'b101),\n'
string+='        .DELAY_LINE_EN(1\'b1),\n'
string+='        .DELAY_LINE_VAL(8\'b00000000),\n'
string+='        .DELAY_VAL_X2(1\'b1),\n'
string+='        .FB_SOURCE_SEL_0(1\'b0),\n'
string+='        .FB_SOURCE_SEL_1(1\'b1))\n'
string+='    I_CDD (\n'
string+='        .DELAY_LINE_OUT_OF_RANGE(),\n'
string+='        .DELAY_LINE_DIR(GND_net),\n'
string+='        .DELAY_LINE_MOVE(GND_net),\n'
string+='        .DELAY_LINE_LOAD(GND_net),\n' 
string+='        .RST_N(VCC_net),\n'
string+='        .BIT_SLIP(GND_net),\n' 
string+='        .A(CLK_IN),\n'
string+='        .Y_DIV(CLK_DIV_OUT),\n'
string+='        .Y(CLK_OUT),\n'
string+='        .Y_FB());\n\n'

string+='    VCC vcc_inst (.Y(VCC_net));\n'
string+='    GND gnd_inst (.Y(GND_net));\n'
string+='\nendmodule\n'

f1.write (string)
f2.write (string)
f1.close()
f2.close()
print 'Done.'


#----------- Generating ides_(NN)_PF_LANECTRL_0_PF_LANECTRL.v
filename= 'ides_'+str(inp_number)+'_PF_LANECTRL_0_PF_LANECTRL.v'
print 'Generating ', filename
f= open (filename,"w")

f.write('// ')
f.write(filename)
f.write('\n// Automatically generated by deser_filegen.py (D.Eliseev)\n')
now = datetime.now()
date_time = '// Timestamp: ' + now.strftime("%d.%m.%Y, %H:%M:%S") +'\n'
f.write(date_time)
f.write('\n`timescale 1 ns/100 ps\n\n')

string = 'module ides_'+str(inp_number)+'_PF_LANECTRL_0_PF_LANECTRL( \n'
string +='       HS_IO_CLK,\n'
string +='       DLL_CODE,\n'
string +='       EYE_MONITOR_WIDTH_OUT,\n'
string +='       RX_DQS_90,\n'
string +='       TX_DQS,\n'
string +='       TX_DQS_270,\n'
string +='       FIFO_WR_PTR,\n'
string +='       FIFO_RD_PTR,\n'
string +='       ARST_N,\n'
string +='       RX_SYNC_RST,\n'
string +='       TX_SYNC_RST,\n'
string +='       FAB_CLK,\n'
string +='       RESET,\n'
string +='       DELAY_LINE_SEL,\n'
string +='       DELAY_LINE_LOAD,\n'
string +='       DELAY_LINE_DIRECTION,\n'
string +='       DELAY_LINE_MOVE,\n'
string +='       HS_IO_CLK_PAUSE,\n'
string +='       EYE_MONITOR_WIDTH_IN,\n'
string +='       RX_DELAY_LINE_OUT_OF_RANGE,\n'
string +='       TX_DELAY_LINE_OUT_OF_RANGE,\n'
string +='       A_OUT_RST_N\n'
string +='    );\n\n'
string +='input  [1:0] HS_IO_CLK;\n'
string +='input  [7:0] DLL_CODE;\n'
string +='output [2:0] EYE_MONITOR_WIDTH_OUT;\n'
string +='output [0:0] RX_DQS_90;\n'
string +='output TX_DQS;\n'
string +='output TX_DQS_270;\n'
string +='output [2:0] FIFO_WR_PTR;\n'
string +='output [2:0] FIFO_RD_PTR;\n'
string +='output ARST_N;\n'
string +='output RX_SYNC_RST;\n'
string +='output TX_SYNC_RST;\n'
string +='input  FAB_CLK;\n'
string +='input  RESET;\n'
string +='input  DELAY_LINE_SEL;\n'
string +='input  DELAY_LINE_LOAD;\n'
string +='input  DELAY_LINE_DIRECTION;\n'
string +='input  DELAY_LINE_MOVE;\n'
string +='input  HS_IO_CLK_PAUSE;\n'
string +='input  [2:0] EYE_MONITOR_WIDTH_IN;\n'
string +='output RX_DELAY_LINE_OUT_OF_RANGE;\n'
string +='output TX_DELAY_LINE_OUT_OF_RANGE;\n'
string +='output A_OUT_RST_N;\n\n'

string +='    wire GND_net, VCC_net;\n\n'
    
string +='    LANECTRL #( \n'
string +='        .DATA_RATE(1200.0), \n'
string +='        .FORMAL_NAME(\"RX%DUPLICATE\"), \n'
string +='        .INTERFACE_NAME(\"RX_DDRX_B_G_DYN\"),\n'
string +='        .DELAY_LINE_SIMULATION_MODE(\"DISABLED\"), \n'
string +='        .RESERVED_0(1\'b0), \n'
string +='        .RESERVED_1(1\'b0), \n'
string +='        .RESERVED_2(1\'b0), \n'
string +='        .SOFTRESET_EN(1\'b0), \n'
string +='        .SOFTRESET(1\'b0), \n'
string +='        .RX_DQS_DELAY_LINE_EN(1\'b1),\n'
string +='        .TX_DQS_DELAY_LINE_EN(1\'b0), \n'
string +='        .RX_DQS_DELAY_LINE_DIRECTION(1\'b1),\n'
string +='        .TX_DQS_DELAY_LINE_DIRECTION(1\'b1), \n'
string +='        .RX_DQS_DELAY_VAL(8\'b00000001),\n'
string +='        .TX_DQS_DELAY_VAL(8\'b00000001), \n'
string +='        .FIFO_EN(1\'b1), .FIFO_MODE(1\'b0),\n'
string +='        .FIFO_RD_PTR_MODE(3\'b011), \n'
string +='        .DQS_MODE(3\'b010), \n'
string +='        .CDR_EN(2\'b01),\n'
string +='        .HS_IO_CLK_SEL(9\'b111001000), \n'
string +='        .DLL_CODE_SEL(2\'b00), \n'
string +='        .CDR_CLK_SEL(12\'b000000000000),\n'
string +='        .READ_MARGIN_TEST_EN(1\'b1), \n'
string +='        .WRITE_MARGIN_TEST_EN(1\'b0), \n'
string +='        .CDR_CLK_DIV(3\'b101), \n'
string +='        .DIV_CLK_SEL(2\'b00), \n'
string +='        .HS_IO_CLK_PAUSE_EN(1\'b1), \n'
string +='        .QDR_EN(1\'b0), \n'
string +='        .DYN_ODT_MODE(1\'b0),\n' 
string +='        .DIV_CLK_EN_SRC(2\'b11),\n' 
string +='        .RANK_2_MODE(1\'b0))\n'
string +='    I_LANECTRL (\n'
string +='        .RX_DATA_VALID(),\n' 
string +='        .RX_BURST_DETECT(), \n'
string +='        .RX_DELAY_LINE_OUT_OF_RANGE(RX_DELAY_LINE_OUT_OF_RANGE), \n'
string +='        .TX_DELAY_LINE_OUT_OF_RANGE(TX_DELAY_LINE_OUT_OF_RANGE), \n'
string +='        .CLK_OUT_R(), \n'
string +='        .A_OUT_RST_N(A_OUT_RST_N),\n'
string +='        .FAB_CLK(FAB_CLK), \n'
string +='        .RESET(RESET), \n'
string +='        .DDR_READ(GND_net), \n'
string +='        .READ_CLK_SEL({GND_net, GND_net, GND_net}), \n'
string +='        .DELAY_LINE_SEL(DELAY_LINE_SEL), \n'
string +='        .DELAY_LINE_LOAD(DELAY_LINE_LOAD), \n'
string +='        .DELAY_LINE_DIRECTION(DELAY_LINE_DIRECTION), \n'
string +='        .DELAY_LINE_MOVE(DELAY_LINE_MOVE), \n'
string +='        .HS_IO_CLK_PAUSE(HS_IO_CLK_PAUSE), \n'
string +='        .DIV_CLK_EN_N(VCC_net), \n'
string +='        .RX_BIT_SLIP(GND_net), \n'
string +='        .CDR_CLK_A_SEL({GND_net, GND_net, GND_net, GND_net, GND_net, GND_net, GND_net, GND_net}), \n'
string +='        .EYE_MONITOR_WIDTH_IN({EYE_MONITOR_WIDTH_IN[2], EYE_MONITOR_WIDTH_IN[1], EYE_MONITOR_WIDTH_IN[0]}), \n'
string +='        .ODT_EN(GND_net), \n'
string +='        .CODE_UPDATE(GND_net), \n'
string +='        .DQS(GND_net), \n'
string +='        .DQS_N(GND_net), \n'
string +='        .HS_IO_CLK({GND_net, GND_net, GND_net, GND_net, HS_IO_CLK[1], HS_IO_CLK[0]}), \n'
string +='        .DLL_CODE({DLL_CODE[7], DLL_CODE[6], DLL_CODE[5], DLL_CODE[4], DLL_CODE[3], DLL_CODE[2], DLL_CODE[1], DLL_CODE[0]}), \n'
string +='        .EYE_MONITOR_WIDTH_OUT({EYE_MONITOR_WIDTH_OUT[2], EYE_MONITOR_WIDTH_OUT[1], EYE_MONITOR_WIDTH_OUT[0]}), \n'
string +='        .ODT_EN_SEL(), \n'
string +='        .RX_DQS_90({nc0, RX_DQS_90[0]}), \n'
string +='        .TX_DQS(TX_DQS), \n'
string +='        .TX_DQS_270(TX_DQS_270), \n'
string +='        .FIFO_WR_PTR({FIFO_WR_PTR[2], FIFO_WR_PTR[1], FIFO_WR_PTR[0]}), \n'
string +='        .FIFO_RD_PTR({FIFO_RD_PTR[2], FIFO_RD_PTR[1], FIFO_RD_PTR[0]}), \n'
string +='        .CDR_CLK(), \n'
string +='        .CDR_NEXT_CLK(), \n'
string +='        .ARST_N(ARST_N), \n'
string +='        .RX_SYNC_RST(RX_SYNC_RST), \n'
string +='        .TX_SYNC_RST(TX_SYNC_RST), \n'
string +='        .ODT_EN_OUT(), \n'
string +='        .DDR_DO_READ(GND_net), \n'
string +='        .CDR_CLK_A_SEL_8(GND_net), \n'
string +='        .CDR_CLK_A_SEL_9(GND_net), \n'
string +='        .CDR_CLK_A_SEL_10(GND_net), \n'
string +='        .CDR_CLK_B_SEL({GND_net, GND_net, GND_net, GND_net, GND_net, GND_net, GND_net, GND_net, GND_net, GND_net, GND_net}), \n'
string +='        .SWITCH(GND_net), \n'
string +='        .CDR_CLR_NEXT_CLK_N(GND_net));\n'

string +='    VCC vcc_inst (.Y(VCC_net));\n'
string +='    GND gnd_inst (.Y(GND_net));\n\n'
    
string +='endmodule\n'

f.write (string)
f.close()
print 'Done.'



#----------- Generating ides_(NN)_instantiation_prepacks.vhd
filename= 'ides_'+str(inp_number)+'_instantiation_prepacks.vhd'
print 'Generating ', filename
f= open (filename,"w")

#--- component declaration
string= '-------------------------------------------------------------------------------\n'
string= '-- Component\'s declaration. Copy-paste it from here and put to the\n'
string+= '-- \"architecture\" section of the module higher hierarchy\n'
string+= '-- check that no components of the same kind are already declared\n'
string+= '-------------------------------------------------------------------------------\n'
string+= '    component ides_'+str(inp_number)+'\n'
string+= '    -- Port list\n'
string+= '    port(\n'
string+= '    -- Inputs\n'
string+= '    ARST_N                  : in  std_logic;\n'
string+= '    DELAY_LINE_DIRECTION    : in  std_logic_vector('+str(inp_number-1)+' downto 0);\n'
string+= '    DELAY_LINE_LOAD         : in  std_logic_vector('+str(inp_number-1)+' downto 0);\n'
string+= '    DELAY_LINE_MOVE         : in  std_logic_vector('+str(inp_number-1)+' downto 0);\n'
string+= '    EYE_MONITOR_CLEAR_FLAGS : in  std_logic_vector('+str(inp_number-1)+' downto 0);\n'
string+= '    EYE_MONITOR_WIDTH       : in  std_logic_vector(2 downto 0);\n'
string+= '    HS_IO_CLK_PAUSE : in  std_logic;\n'
string+= '    RXD             : in  std_logic_vector('+str(inp_number-1)+' downto 0);\n'
string+= '    RX_CLK          : in  std_logic;\n'
string+= '    -- Outputs\n'
string+= '    DELAY_LINE_OUT_OF_RANGE : out  std_logic_vector('+str(inp_number-1)+' downto 0);\n'
string+= '    EYE_MONITOR_EARLY       : out  std_logic_vector('+str(inp_number-1)+' downto 0);\n'
string+= '    EYE_MONITOR_LATE        : out  std_logic_vector('+str(inp_number-1)+' downto 0);\n'
for i in range (0,inp_number):
	string+='    L'+str(i)+'_RXD_DATA     : out std_logic_vector(9 downto 0);\n'
string+= '    RX_CLK_G        : out std_logic\n'
string+= '    );\n'
string+= '    end component;\n\n\n'
f.write (string)

#--- component instantiation
string= '-------------------------------------------------------------------------------\n'
string+= '-- Instantiation of the component. Copy-paste it from here and put to the\n'
string+= '-- body section of the target module\n'
string+= '-------------------------------------------------------------------------------\n'
string+='NAME_HERE : ides_'+str(inp_number)+'\n'
string+='   port map(\n'
string+='    -- Inputs\n'
string+='    ARST_N                  =>   ,\n'
string+='    DELAY_LINE_DIRECTION    =>   ,\n'
string+='    DELAY_LINE_LOAD         =>   ,\n'
string+='    DELAY_LINE_MOVE         =>   ,\n'
string+='    EYE_MONITOR_CLEAR_FLAGS =>   ,\n'
string+='    EYE_MONITOR_WIDTH       =>   ,\n'
string+='    HS_IO_CLK_PAUSE         =>   ,\n'
string+='    RXD                     =>   ,\n'
string+='    RX_CLK                  =>   ,\n'
string+='    -- Outputs \n'
string+='    DELAY_LINE_OUT_OF_RANGE =>   ,\n'
string+='    EYE_MONITOR_EARLY       =>   ,\n'
string+='    EYE_MONITOR_LATE        =>   ,\n'
for i in range (0,inp_number):
	string+='    L'+str(i)+'_RXD_DATA             =>   ,\n'
string+='    RX_CLK_G                 =>   );\n\n'  


f.write (string)
f.close()
print 'Done.'



