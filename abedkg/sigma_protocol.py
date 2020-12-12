# from py_ecc import optimized_bn128
# bn128=optimized_bn128
# from py_ecc import bn128
import setting
bn128=setting.getBn128()
lib=bn128

import util
import random as rand
import re
from abeutils import Utils
# import maabe as abe
import hashlib
import ma_abe
from ma_abe import MaabeRW15

FQ, FQ2, FQ12, field_modulus = lib.FQ, lib.FQ2, lib.FQ12, lib.field_modulus
pairing,G1, G2, G12, b, b2, b12, is_inf, is_on_curve, eq, add, double, curve_order, multiply = \
      lib.pairing,lib.G1, lib.G2, lib.G12, lib.b, lib.b2, lib.b12, lib.is_inf, lib.is_on_curve, lib.eq, lib.add, lib.double, lib.curve_order, lib.multiply
    



def hash(str):
    x = hashlib.sha256()
    x.update(str.encode())
    return x.hexdigest()

def hash2(str):
    x = hashlib.sha256()
    x.update((str+"2").encode())
    return x.hexdigest()


def enc_and_proof(maabe,gp,pks,message,acp):
    # print((gp['egg']** 123))
    # print(type(message))
    g=FQ(maabe.random())
     # multiply(G2,maabe.random())
    # h=FQ(maabe.random())
    # multiply(G2,maabe.random())

    M=gp["egg"]**message
    ct = maabe.encrypt(gp, pks, M, acp)     
    j=ct["j"]
    k=ct["k"]
    h=ct["h"]
    zhat = ct["zhat"]
    etap= ct["etap"]
    eta= ct["eta"]
    quotient=ct["quotient"]
    Mhat=ct["Mhat"]
    c=ct["c"]

    for i in range(0, len(quotient)):            
        if zhat<0:
            assert(etap[i]* j**(-quotient[i]) * k**(-zhat) == j**(int(Mhat.coeffs[i]))  * eta[i]**c )
        else:
            assert(etap[i]* j**(-quotient[i]) == j**(int(Mhat.coeffs[i])) * k**zhat * eta[i]**c )
    print("eta check, passed")

    dkg_pkp=ct["dkg_pkp"]
    dkg_pk=ct["dkg_pk"]
    for i in range(0, 12):
        assert(dkg_pkp[i]* h**(-quotient[i]) == h**(int(Mhat.coeffs[i])) * dkg_pk[i]**c )
    print("dkg_pk check, passed")
            
    ztilde=ct["ztilde"]
    Mtilde=ct["Mtilde"]
    C0p=ct["C0p"]
    C0=ct["C0"]
    cp=ct["cp"]
    assert(C0p == Mtilde * (gp["egg"]**ztilde) * (C0**cp))
    print("C0 check, passed")
    
    C1=ct["C1"]
    C2=ct["C2"]
    C3=ct["C3"]
    C4=ct["C4"]
    C1p=ct["C1p"]
    C2p=ct["C2p"]
    C3p=ct["C3p"]
    C4p=ct["C4p"]
    secret_shareshat=ct["secret_shareshat"]
    zero_shareshat=ct["zero_shareshat"]
    txhat=ct["txhat"]
    for i in C1p:
        attribute_name, auth, _ = maabe.unpack_attribute(i)
        attr = "%s@%s" % (attribute_name, auth)
            
        assert(C1p[i] == gp['egg']**(secret_shareshat[i]%curve_order) * pks[auth]['egga']**(txhat[i]) *C1[i] ** (cp%curve_order))            
        print("C1 "+attr+" check, passed")
        assert(eq(C2p[i],add(multiply(gp['g1'], (-txhat[i]) %curve_order), multiply(C2[i], cp))))
        print("C2 "+attr+" check, passed")
        assert(eq(C3p[i],\
            add(add(multiply(pks[auth]['gy'], txhat[i]), multiply(gp['g1'], zero_shareshat[i])),\
                multiply(C3[i],cp))))
        print("C3 "+attr+" check, passed")
        assert(eq(C4p[i],add(multiply(gp['F'](attr), txhat[i]), multiply(C4[i], cp))))
        print("C4 "+attr+" check, passed")



maabe = MaabeRW15()
gp = maabe.setup() 
(pk1, sk1) = maabe.authsetup(gp, "UT") 
# print(pk1, sk1)
user_attributes1 = ['STUDENT@UT', 'PHD@UT'] 
# user_keys1 = maabe.multiple_attributes_keygen(gp, sk1, "bob", user_attributes1) 
print(user_keys1)

(pk2, sk2) = maabe.authsetup(gp, "OU") 
user_attributes2 = ['STUDENT@OU'] 
user_keys2 = maabe.multiple_attributes_keygen(gp, sk2, "bob", user_attributes2) 
# print(user_keys2)

pks = {'UT': pk1, 'OU': pk2} 
access_policy = '(2 of (STUDENT@UT, PROFESSOR@OU, (XXXX@UT or PHD@UT))) and (STUDENT@UT or MASTERS@OU)'
message = maabe.random()

# cipher_text = maabe.encrypt(gp, pks, message, access_policy) 
# print(type(message))
enc_and_proof(maabe,gp,pks,message,access_policy)



