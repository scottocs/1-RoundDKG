import time
from py_ecc import bn128, optimized_bn128


lib =optimized_bn128
pairing, neg = lib.pairing, lib.neg
G1, G2, G12, b, b2, b12, is_inf, is_on_curve, eq, add, double, curve_order, multiply = \
      lib.G1, lib.G2, lib.G12, lib.b, lib.b2, lib.b12, lib.is_inf, lib.is_on_curve, lib.eq, lib.add, lib.double, lib.curve_order, lib.multiply
FQ, FQ2, FQ12, field_modulus = lib.FQ, lib.FQ2, lib.FQ12, lib.field_modulus

print('Starting pairing tests')
a = time.time()
p1 = pairing(G2, G1)
pn1 = pairing(G2, neg(G1))
assert p1 * pn1 == FQ12.one()
for i in range(0, 100):
    pairingRes=pairing(G2, multiply(G1, i))    
    print(pairingRes)
    print(pairingRes.coeffs[0])