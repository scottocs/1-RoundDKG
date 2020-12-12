
# from py_ecc import optimized_bn128
# bn128=optimized_bn128
from typing import Dict, List, Tuple, Set, Optional
import setting
bn128=setting.getBn128()
lib=bn128

import random as rand
import re
from abeutils import Utils
import util
# import maabe as abe
import hashlib
import ma_abe
from ma_abe2 import MaabeRW15

FQ, FQ2, FQ12, field_modulus = lib.FQ, lib.FQ2, lib.FQ12, lib.field_modulus
pairing,G1, G2, G12, b, b2, b12, is_inf, is_on_curve, eq, add, double, curve_order, multiply = \
      lib.pairing,lib.G1, lib.G2, lib.G12, lib.b, lib.b2, lib.b12, lib.is_inf, lib.is_on_curve, lib.eq, lib.add, lib.double, lib.curve_order, lib.multiply


# secret_key: int  # the node's personal secret key
# public_key: PointG1  # the node's personal public key (from group G1)
# public_keys: Dict[int, PointG1]  # the public keys for all registered nodes
# C0:
# def enc_and_proof(maabe,gp,pks,message,acp) -> Tuple[Dict[int, int], List[PointG1]]:
# Dict[int, int]


def hash(str):
    x = hashlib.sha256()
    x.update(str.encode())
    return x.hexdigest()

def hash2(str):
    x = hashlib.sha256()
    x.update((str+"2").encode())
    return x.hexdigest()


def enc_and_proof():
    maabe = MaabeRW15()
    gp = maabe.setup() 
    pks = {} 
    n=10
    print("n=",n)
    for i in range(0, n):
        (pk, sk) = maabe.authsetup(gp, "AU"+str(i)) 
        # user_attributes1 = ['STUDENT@UT', 'PHD@UT'] 
        # user_keys1 = maabe.multiple_attributes_keygen(gp, sk1, "bob", user_attributes1) 
        pks["AU"+str(i)]=pk
    # print(pk, sk)
    print("done authority setup")

    # print(user_keys1)    

    # (pk2, sk2) = maabe.authsetup(gp, "OU") 
    # user_attributes2 = ['STUDENT@OU'] 
    # user_keys2 = maabe.multiple_attributes_keygen(gp, sk2, "bob", user_attributes2) 
    # print(user_keys2)
    # print("done keygen")
    t=int(n/2)+1
    acp="("+str(t)+" of (";
    for i in range(0, n):
        acp+="gid@AU"+str(i)
        if i<n-1:
            acp=acp+", "
    acp=acp+"))"
    print(acp)
    # acp = '('+str(t)+' of (STUDENT@UT, PROFESSOR@OU, (XXXX@UT or PHD@UT))) and (STUDENT@UT or MASTERS@OU)'
    message = maabe.random()

    # print((gp['egg']** 123))
    # print(type(message))
    g=FQ(maabe.random())
     # multiply(G2,maabe.random())
    # h=FQ(maabe.random())
    # multiply(G2,maabe.random())

    M=(gp["egg"][0],multiply(gp["egg"][1],message))
    ct = maabe.encrypt(gp, pks, M, acp)     
    j=ct["j"]
    k=ct["k"]
    h=ct["h"]
    zhat = ct["zhat"]
    # etap= ct["etap"]
    # eta= ct["eta"]
    quotient=ct["quotient"]
    Mhat=ct["Mhat"]
    c=ct["c"]

    # for i in range(0, len(quotient)):            
    #     assert(etap[i] == j**int(Mhat.coeffs[i])* j**quotient[i] * k**zhat * eta[i]**c )
    # print("eta check, passed")

    dkg_pkp=ct["dkg_pkp"]
    dkg_pk=ct["dkg_pk"]
    # for i in range(0, 12):
    #     assert(dkg_pkp[i] == h**(int(Mhat.coeffs[i]))* h**quotient[i] * dkg_pk[i]**c )
    # print("dkg_pk check, passed")
            
    ztilde=ct["ztilde"]
    Mtilde=ct["Mtilde"]
    C0p=ct["C0p"]
    C0=ct["C0"]
    # print(C0)
    cp=ct["cp"]
    
    # assert(eq(C0p[1], add(add(Mtilde, multiply(gp['egg'][1],ztilde)), multiply(C0[1],cp))))    
    # print("C0 check, passed")
    

    C1=ct["C1"]
    C2=ct["C2"]
    CHat2=ct["CHat2"]
    C3=ct["C3"]    
    CHat3=ct["CHat3"]
    C4=ct["C4"]
    C1p=ct["C1p"]
    C2p=ct["C2p"]
    CHat2p=ct["CHat2p"]
    C3p=ct["C3p"]
    CHat3p=ct["CHat3p"]
    C4p=ct["C4p"]
    secret_shareshat=ct["secret_shareshat"]
    zero_shareshat=ct["zero_shareshat"]
    txhat=ct["txhat"]
    ct["egga"]={}
    ct["gy"]={}
    ct["g2y"]={}
    ct["attr_unpacked"]=[]
    for i in C1p:
        
        attribute_name, auth, _ = maabe.unpack_attribute(i)
        attr = "%s@%s" % (attribute_name, auth)        
        ct["egga"][i]=pks[auth]['egga']
        ct["gy"][i]=pks[auth]['gy']
        ct["g2y"][i]=pks[auth]['g2y']
        ct["attr_unpacked"].append(attr)
        # print(CHat2p[i],gp["g2"])
        # print(gp["g1"])
        # print(C2p[i])
        # print("    ",pairing(CHat2p[i], gp['g1'] ), pairing(gp["g2"],C2p[i]))
        # assert(eq(pairing(gp['g1'], CHat2p[i]), pairing(C2p[i], gp["g2"])))       

        # assert(eq(C1p[i][1], add(\
        #                         add(multiply(gp['egg'][1],(secret_shareshat[i]%curve_order)), \
        #                             multiply(pks[auth]['egga'][1],(txhat[i]))),\
        #                         multiply(C1[i][1], (cp%curve_order)))))        
        # print("C1 "+attr+" check, passed")
        # assert(eq(C2p[i],add(multiply(gp['g1'], curve_order-txhat[i]), multiply(C2[i], cp))))
        # # print(multiply(gp['g1'], curve_order-txhat[i]))
        # print("C2 "+attr+" check, passed")
        # assert(eq(C3p[i],\
        #     add(add(multiply(pks[auth]['gy'], txhat[i]), multiply(gp['g1'], zero_shareshat[i])),\
        #         multiply(C3[i],cp))))
        # print("C3 "+attr+" check, passed")
        # assert(eq(C4p[i],add(multiply(gp['F'](attr), txhat[i]), multiply(C4[i], cp))))
        # print("C4 "+attr+" check, passed")
        # print(add(multiply(gp['F'](attr), txhat[i]), multiply(C4[i], cp)))


        
    print("encrypt done")
    ct["egg"]=gp["egg"]
    ct["g1"]=gp["g1"]
    ct["g2"]=gp["g2"]
    

    # print(ct["g1"])
    # print(ct["g2"])
    # for key in gp:
    #     print(key,type(gp[key]))
    #     ct[key]=gp[key]
    # ct["gp"]=gp
    # print(gp)
    return ct
if __name__ == "__main__":
    # cipher_text = maabe.encrypt(gp, pks, message, access_policy) 
    # print(type(message))
    enc_and_proof()


