import sys

varhash = {}
labelhash = {}
varidx = 0
instructions_out = []
instruction_cnt = 0
for line in sys.stdin :
    if '#' in line :
        line = line[:line.index('#')]
    tokens = line.strip().split()
    if len(tokens)==0 :
        continue
    if tokens[0] == 'DEF' :
        varhash[tokens[1]]=varidx
        varidx+=1
        continue
    #
    # at this point we have a bona fide
    # instruction to deal with
    #
    if len(tokens)>1 and tokens[-1] in varhash :
        tokens[-1]=varhash[tokens[-1]]

    instruction_cnt+=1
    if tokens[0][-1]==':' :
        labelhash[tokens[0]]=instruction_cnt
        tokens=tokens[1:]
        
    instructions_out.append(tokens)

for i,instr in enumerate(instructions_out) :
    if instr[0]=='GTO' :
        instr[1] = labelhash.get(instr[1],instr[1])
    print '%02d'%(i+1,), ' '.join(map(str,instr))
        
