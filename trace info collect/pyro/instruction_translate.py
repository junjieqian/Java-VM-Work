import string
import sys
import matplotlib.pyplot as plt
from time import gmtime, strftime
from numpy import binary_repr

# def helper():
#     print "*************************************************************"
#     print "**** find-addr-range: to find the address range of different "
#     print "****                  generations in heap"
#     print "**** USAGE:python find-addr-range.py trace-file-name"
#     print "*************************************************************"

def inst_trans(instruction):
    ''' translate the instructions
    @param ins_binary, binary presentation of the instructions
    @param ins_opcode, operation code of the instructions
    @param ins_function, function of the instructions
    @param ins, the instruction going to present later
    '''
    inst_dicts()
    try:
        ins_dec=int(instruction, 0)
    except:
        print >> sys.stderr, 'instruction not decodbale'
	return ' '
    ins_binary=str(binary_repr(ins_dec))
    ins_opcode=str(binary_repr(int(ins_binary[:6], 2), 6))
    ins_function=str(binary_repr(int(ins_binary[-6:], 2), 6))
    ins=' '
    if ins_opcode=='000000':
        if ins_function in R_dict:
            ins=R_dict[ins_function]
        else:
            print >> sys.stderr, 'R type function not found, ', ins_function
    elif ins_opcode[:5]=='00001':
        if ins_opcode in J_dict:
            ins=J_dict[ins_opcode]
        else:
            print >> sys.stderr, 'J type opcode not found, ', ins_opcode
    elif ins_opcode[:4]=='0100':
        ins_format=str(binary_repr(int(ins_binary[6:11], 2), 5))
        if (ins_format+ins_function) in C_dict:
            ins=C_dict[ins_format+ins_function]
        else:
            print >> sys.stderr, 'C type function and format pair not found, format is, ', ins_format, ' function is ', ins_function
    else:
        if ins_opcode in I_dict:
            ins=I_dict[ins_opcode]
        else:
            print >> sys.stderr, 'I type opcode not found, ', ins_opcode
    return ins

def inst_dicts():
    '''
    Following are for different instructions, refer to http://www.cs.sunysb.edu/~lw/spim/MIPSinstHex.pdf
    R-type, opcode(000000)+rs(5)+rt(5)+rd(5)+sa(5)+function(6)
    I-type, opcode(6)+rs(5)+rt(5)+immediate(16)
    J-type, opcode(00001x)+target(26)
    Coprocessor, opcode(0100xx)+format(5)+ft(5)+fs(5)+fd(5)+function(6)
    '''
    global J_dict
    J_dict={}    # J-type Instructions
    global I_dict
    I_dict={}    # I-type Instructions
    global R_dict
    R_dict={}    # R-type Instructions
    global C_dict
    C_dict={}    # Coprocessor Instructions
    R_dict['100000']='add'
    R_dict['100001']='addu'
    R_dict['100100']='and'
    R_dict['001101']='break'
    R_dict['011010']='div'
    R_dict['011011']='divu'
    R_dict['001001']='jalr'
    R_dict['001000']='jr'
    R_dict['010000']='mfhi'
    R_dict['010010']='mflo'
    R_dict['010001']='mthi'
    R_dict['010011']='mtlo'
    R_dict['011000']='mult'
    R_dict['011001']='multu'
    R_dict['100111']='nor'
    R_dict['100101']='or'
    R_dict['000000']='sll'
    R_dict['000100']='sllv'
    R_dict['101010']='slt'
    R_dict['101011']='sltu'
    R_dict['000011']='sra'
    R_dict['000111']='srav'
    R_dict['000010']='srl'
    R_dict['000110']='srlv'
    R_dict['100010']='sub'
    R_dict['100011']='subu'
    R_dict['001100']='syscall'
    R_dict['100110']='xor'
    ######################## I type
    I_dict['001000']='addi'
    I_dict['001001']='addiu'
    I_dict['001100']='andi'
    I_dict['000100']='beq'
    I_dict['000001']='bgez'
    I_dict['000111']='bgtz'
    I_dict['000110']='blez'
    I_dict['000001']='bltz'
    I_dict['000101']='bne'
    I_dict['100000']='lb'
    I_dict['100100']='lbu'
    I_dict['100001']='lh'
    I_dict['100101']='lhu'
    I_dict['001111']='lui'
    I_dict['100011']='lw'
    I_dict['110001']='lwc1'
    I_dict['001101']='ori'
    I_dict['101000']='sb'
    I_dict['001010']='slti'
    I_dict['001011']='sltiu'
    I_dict['101001']='sh'
    I_dict['101011']='sw'
    I_dict['111001']='swc1'
    I_dict['001110']='xori'
    ###################### J type
    J_dict['000010']='j'
    J_dict['000011']='jal'
    ##################### C type, format+function as the key
    C_dict['10000000000']='add.s'
    C_dict['10100100000']='cvt.s.w'
    C_dict['10000100100']='cvt.w.s'
    C_dict['10000000011']='div.s'
    C_dict['00000000000']='mfc1'
    C_dict['10000000110']='mov.s'
    C_dict['00100000000']='mtc1'
    C_dict['10000000010']='mul.s'
    C_dict['10000000001']='sub.s'

# def trace_reg():
#     '''
#     regulate the trace, get rid of the noise records
#     '''
#     try:
#         script, trace_name=sys.argv
#     except:
#         helper()
#         sys.exit()
#     new_trace_name=trace_name+'_formatted_'+strftime('%b_%d', gmtime())
#     fp=open(trace_name, 'r')
#     fw=open(new_trace_name, 'w')
#     for line in fp:
#         try:
#             word=line.split(': ')
#         except:
#             pass
#         rw='0'
#         if word[0]=='1':
#             rw='1'
#         elif word[0]=='0':
#             rw='0'
#         addr=hex(int((word[1].split('\n'))[0], 0))
#         if int(addr, 0)>0:
#             fw.write(rw+' '+addr+'\n')
#     fp.close()
#     fw.close()
#     return new_trace_name

# def find(record):
#     global up_boundry
#     global nearest_addr
#     try:
#         word=record.split(': ')
#         addr=int((word[1].split('\n'))[0],0)
# #        global up_boundry
#         up_boundry=3.0*(10**9)
# #    global nearest_addr
#         nearest_addr=0
#         if addr<3.0*(10**9):
#             if addr>nearest_addr:
#                 nearest_addr=addr
#     except:
#         pass
