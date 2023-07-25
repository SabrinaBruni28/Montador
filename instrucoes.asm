add x1, x2, x3
lb x2, 0(x10)
sub x4, x2, x5
and x8, x4, x6
ori x2, x7, 8
add x6, x8, x4
beq x4, x8, -4
srl x10, x10, x4
sb x8, 0(x10)
