import sys
import math
from math import floor, exp, log, sqrt, log
import numpy as np
import operator

class RPNRuntime(object) :

    def __init__(self,stacksize=4,nregisters=20,ndigits=10) :

        self.STACKSIZE=stacksize
        self.NREGISTERS=nregisters
        self.NDIGITS=ndigits

        self.stack=np.array([0]*self.STACKSIZE,dtype=float)
        self.registers=np.array([0]*self.NREGISTERS,dtype=float)

        self.stack[0] = math.pi/24.0   
        self.registers[0]=math.pi
        
        self.display_state = 0 # 0 means start a new number with 0123456789., 1 means add to existing number

        self.operators1 = {'SQRT' : math.sqrt,
                           'e^x'  : math.exp,
                           'LN'   : math.log,
                           'FRAC' : lambda _ : _ - math.floor(_),
                           'INTG' : math.floor,
                           'CHS'  : operator.neg,
                           '1/x'  : lambda x : 1./x,
                           '12x'  : lambda x : 12.*x,
                           '12/'  : lambda x : x/12. }

        self.operators2 = {'+'    : operator.add,
                           '-'    : operator.sub,
                           'x'    : operator.mul,
                           '/'    : operator.div,
                           'y^x'  : operator.pow,
                           '%'    : lambda y,x : y*x/100.}

        self.test1      = {'x=0'  : lambda _ : _==0}
        self.test2      = {'x<=y'  : lambda x,y : x<=y}

        self.program=[['END']]
        self.display = str(self.stack[0])
        self.traceflag = False
        
    def read_program(self,fp) :
        program = [['END']]
        for line in fp :
            program.append(line.split()[1:])
        return program

    def trace(self,msg) :
        if self.traceflag :
            sys.stdout.write(msg)
            
    def run(self,program) :
        cnt = 0
        i = 1
        while program[i] != ['END'] and cnt < 10000 :
            cnt += 1
            self.trace('\n')
            self.trace('%5d %02d>> %12s' % (cnt,i,program[i]))
            toks = program[i]
            t0 = toks[0]
            if t0 == 'GTO' :
                i = int(toks[1])
                continue
            if t0 in self.test1 :
                if not self.test1[t0](self.stack[0]) :
                    i += 2
                    continue
            if t0 in self.test2 :
                if not self.test2[t0](self.stack[0],self.stack[1]) :
                    i += 2
                    continue
            if t0 == 'Enter' :
                self.stack[1:] = self.stack[0:-1]
            elif t0 == 'RCL' :
                # the contents of the storage register gets pushed
                # on our stack.
                if toks[1] == '.' :
                    idx = 10 + int(toks[2])
                else :
                    idx = int(toks[1])
                self.stack[1:] = self.stack[:-1]
                self.stack[0] = self.registers[idx]
            elif t0 == 'STO' :
                idxloc = 2 if (toks[1] in '+-x/') else 1
                if toks[idxloc] == '.' :
                    idx = 10 + int(toks[idxloc+1])
                else :
                    idx = int(toks[idxloc])
                if toks[1] in '+-x/' :
                    self.registers[idx] = self.operators2[toks[1]](self.registers[idx],self.stack[0])
                else :
                    self.registers[idx] = self.stack[0]
            elif t0 == 'x<->y' :
                self.stack[:2] = self.stack[1::-1]
            elif t0 == 'ROT' :
                self.stack[:] = np.array(list(self.stack[1:-1])+[self.stack[0]])
            elif t0 in self.operators1 :
                self.stack[0] = self.operators1[t0](self.stack[0])
            elif t0 in self.operators2 :
                # note the reversed order here, so that
                # subtraction, division and exponentiation
                # work the way we want.
                self.stack[0] = self.operators2[t0](self.stack[1],self.stack[0])
                self.stack[1:-1] = self.stack[2:]
            elif t0 in '.0123456789' :
                if self.display_state == 0 :
                    # we are starting a new entry in the x-register.
                    # this pushes the rest of the stack down
                    self.stack[1:] = self.stack[:-1]
                    self.display = ''
                    self.display_state = 1
                if len(self.display)<self.NDIGITS :
                    self.display = self.display+t0
                self.stack[0] = float(self.display)

            if t0 not in '.123456789' :
                self.display = str(self.stack[0])
                self.display_state=0
                    
            self.trace('%12s %s' % (self.display, '['+' '.join(map(lambda _ : '%10.6f' % _, self.stack)) + ']'))

            i += 1


