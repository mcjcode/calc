# Assumptions
# R0 contains 3.141592654
# The x register contains theta, the angle whose cosine
# and sine we are trying to compute.
#
DEF pi
DEF theta
DEF alpha
DEF c1
DEF s1
DEF c2
DEF s2

STO theta
RCL pi
STO alpha
# initialize (c1,s1) and (c2,s2) so that
# e^{i theta} = c2+is2, e^{i alpha} = c1+is1
0
STO s1 # tracks sin(alpha)
STO s2 # tracks sin(theta)
1
STO c2 # tracks cos(theta)
CHS
STO c1 # tracks cos(alpha)
LOOP: 1
2
CHS
e^x
RCL 2
x<=y
GTO ENDLOOP:
RCL 1
x<->y
x<=y # is alpha<=theta?
GTO PL:
GTO POSTPL:
PL: RCL c2  # angle addition formula for cosine
RCL c1
x
RCL s2
RCL s1
x
- # x now has c(1+2)=c2c1-s2s1
STO c2
2
y^x
1
x<->y
-
SQRT # x now has s2=sqrt(1-c2^2)
STO s2
# subtract alpha from theta
RCL alpha
STO - theta
# divide alpha by 2
POSTPL: 2
STO / alpha
# Half angle formula for sin
1
RCL c1
-
2
/
SQRT
STO s1
# Half angle formula for cos
1
RCL c1
+
2
/
SQRT
STO c1
GTO LOOP:
ENDLOOP: RCL s2
RCL c2
GTO 00



