
import setting
bn128=setting.getBn128()

import util
import random
import re
from abeutils import Utils
import hashlib
# import optimized_curve
# from charm.toolbox.pairinggroup import PairingGroup
# import newjson
lib=bn128
FQ, FQ2, FQ12, field_modulus = lib.FQ, lib.FQ2, lib.FQ12, lib.field_modulus
pairing,G1, G2, G12, b, b2, b12, is_inf, is_on_curve, eq, add, double, curve_order, multiply = \
      lib.pairing,lib.G1, lib.G2, lib.G12, lib.b, lib.b2, lib.b12, lib.is_inf, lib.is_on_curve, lib.eq, lib.add, lib.double, lib.curve_order, lib.multiply


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def FQ12ToInt(fq12value):
    # (2421572130728995776966111225896962453619921797707709996809563916572643662968, 17597669113497198503743549746221204610554807092054855309459603004045023729206, 6808099643203508867535121604680299872213567506732374554311995409561205588434, 20025038805775319672168534746658411053237712056380191928175913333560165995460, 229731873704813733254464584553986182279125791426847734113154846709141667703, 15164045160012650235884986075993103685827469362115071397686828810584571044239, 20589711274383952032836025308858471335299207129121936034661870760293858608322, 10736647173781131293519746348193571250385196827748347896963402121636455740763, 3562776870626562607436017013136855967750414971220044562927491099632443892614, 15469551818407474514163670492590988300440249779914596449375411725189831980606, 21562754573273249085847279209463097911104658328348822858012614416489264329871, 2936009288700626504404857756638695686919241885607318830341540210932700674080)
    return [g**fq12.coeffs[i] for i in range(0, fq12.degree)]

def gPowFQ12(h, fq12,mod=field_modulus):
    return [h**int(fq12.coeffs[i]) for i in range(0, fq12.degree)]

def minusFQ12(fq121, fq122):
    return [int(fq121.coeffs[i] - fq122.coeffs[i]) for i in range(0, fq121.degree)]


def hash(str):
    x = hashlib.sha256()
    x.update(str.encode())
    return x.hexdigest()

def hash2(str):
    x = hashlib.sha256()
    x.update((str+"2").encode())
    return x.hexdigest()

def powFQ12(g, fq12):
    # for i in range(0,fq12.degree):
    #   print(fq12.coeffs[i])
    return [g**fq12.coeffs[i] for i in range(0, fq12.degree)]
def multiplyEta(eta, hz):
    return [eta[i]*hz for i in range(0, len(eta))]


class MaabeRW15():

    def __init__(self):
        # ABEncMultiAuth.__init__(self)
        # self.group = group

        self.abeutils = Utils()

        return
    def random(self):
        # return 2
        return int(random.random()*(2**256)) % bn128.curve_order

    def unpack_attribute(self, attribute):
        parts = re.split(r"[@_]", attribute)
        assert len(parts) > 1, "No @ char in [attribute@authority] name"
        # print(parts[0], parts[1])
        return parts[0], parts[1], None if len(parts) < 3 else parts[2]


    def setup(self):
        g1 = bn128.multiply(bn128.G2,self.random())
        g2 = bn128.multiply(bn128.G1,self.random())
        # print("example g2",bn128.multiply(g1,self.random()))
        egg = bn128.pairing(g1, g2)
        # egg=bn128.multiply(bn128.G12,self.random())
        # print(egg)
        H = lambda x: util.hashToG1(x)
        F = lambda x: util.hashToG1(x)
        # print(H("123"),F("123"))
        # print(type(g1[0]))
        # print(type(gp[""]))
        gp = {'g1': g1, 'g2': g2, 'egg': egg, 'H': H, 'F': F}
        if debug:
            print("Global Setup=========================")
            print(gp["egg"])
            print("\n")
        return gp
    
    def authsetup(self, gp, name):
        """
        Setup an attribute authority.
        :param gp: The global parameters
        :param name: The name of the authority
        :return: The public and private key of the authority
        """
        alpha, y = self.random(), self.random()
        # egga = bn128.multiply(gp['egg'], alpha)
        egga = gp['egg'] ** alpha

        # gy={}
        gy=bn128.multiply(gp['g1'],y)      
        # print("11111111")  
        # print(type(gy["g1"][0]),type(gp["g1"][0]))
        # print(bn128.is_on_curve(gy, bn128.b2))
        # print(bn128.is_on_curve(egga, bn128.b12))
        pk = {'name': name, 'egga': egga, 'gy': gy}
        sk = {'name': name, 'alpha': alpha, 'y': y}
        if debug:
            print("Authsetup: =======================%s" % name)
            print(pk)
            print(sk)

        return pk, sk

    def keygen(self, gp, sk, gid, attribute):
        """
        Generate a user secret key for the attribute.
        :param gp: The global parameters.
        :param sk: The secret key of the attribute authority.
        :param gid: The global user identifier.
        :param attribute: The attribute.
        :return: The secret key for the attribute for the user with identifier gid.
        """
        _, auth, _ = self.unpack_attribute(attribute)
        assert sk['name'] == auth, "Attribute %s does not belong to authority %s" % (attribute, sk['name'])

        t = self.random()
        # print(bn128.multiply(gp['g2'],sk['alpha']))
        r=bn128.multiply(gp['H'](gid), sk['y'])
        # print(type(r[0]))
        # print(bn128.multiply(gp['F'](attribute), t))
        # K = gp['g2'] ** sk['alpha'] * gp['H'](gid) ** sk['y'] * gp['F'](attribute) ** t
        # KP = gp['g1'] ** t
        k1=bn128.multiply(gp['g2'],sk['alpha'])
        k2=bn128.multiply(gp['H'](gid), sk['y'])
        k3=bn128.multiply(gp['F'](attribute), t)
        K=bn128.add(k1,k2)
        K=bn128.add(K,k3)
        # K = bn128.add(\
        #     bn128.add(bn128.multiply(gp['g2'],sk['alpha']),\
        #         	bn128.multiply(gp['H'](gid), sk['y'])),\
        #     bn128.multiply(gp['F'](attribute), t))
        # print("........",bn128.is_on_curve(K, bn128.b))
        # KP = gp['g1'] ** t
        KP = bn128.multiply(gp['g1'], t)
        # print("11111111",bn128.is_on_curve(KP, bn128.b2))

        if debug:
            print("Keygen")
            print("User: %s, Attribute: %s" % (gid, attribute))
            print({'K': K, 'KP': KP})

        return {'K': K, 'KP': KP}

    def multiple_attributes_keygen(self, gp, sk, gid, attributes):
        """
        Generate a dictionary of secret keys for a user for a list of attributes.
        :param gp: The global parameters.
        :param sk: The secret key of the attribute authority.
        :param gid: The global user identifier.
        :param attributes: The list of attributes.
        :return: A dictionary with attribute names as keys, and secret keys for the attributes as values.
        """
        uk = {}
        for attribute in attributes:
            uk[attribute] = self.keygen(gp, sk, gid, attribute)
        return uk
    

    def encrypt(self, gp, pks, message, policy_str):       
        z = self.random()  # secret to be shared
        zp = self.random()  # secret to be shared
        w = 0  # 0 to be shared
        wp= 0

        policy = self.abeutils.createPolicy(policy_str)
        attribute_list = self.abeutils.getAttributeList(policy)
        secret_shares = self.abeutils.calculateSharesDict(z, policy)  # These are correctly set to be exponents in Z_p
        zero_shares = self.abeutils.calculateSharesDict(w, policy)
        # print(secret_shares)

        secret_sharesp = self.abeutils.calculateSharesDict(zp, policy)  # These are correctly set to be exponents in Z_p
        zero_sharesp = self.abeutils.calculateSharesDict(wp, policy)
        
        M=message
        Mp=gp["egg"]**self.random()
        # print(type(M))
        C0 = (gp['egg'] ** z) * M
        C0p= (gp['egg'] ** zp) * Mp
        C1, C2, C3, C4 = {}, {}, {}, {}
        C1p, C2p, C3p, C4p = {}, {}, {}, {}
        tx, txp={},{}
        cp=int(hash2(str(C0)+"||"+str(C1)+"||"+str(C2)+"||"+str(C3)+"||"+str(C4)),16)

        ztilde=(zp-cp*z)%curve_order#for egg
        Mtilde=(Mp/(M**cp))#%curve_order#egg
        assert(C0p == Mtilde * (gp["egg"]**ztilde) * (C0**cp))    

        txhat,secret_shareshat,zero_shareshat={},{},{}
        for i in attribute_list:
            attribute_name, auth, _ = self.unpack_attribute(i)
            attr = "%s@%s" % (attribute_name, auth)
            
            tx[i] = self.random()
            C1[i] = (gp['egg']**secret_shares[i]) * (pks[auth]['egga']**tx[i])
            C2[i] = multiply(gp['g1'], (curve_order-tx[i]))
            C3[i] = add(multiply(pks[auth]['gy'], tx[i]), multiply(gp['g1'], zero_shares[i]))
            C4[i] = multiply(gp['F'](attr), tx[i])
            
            txp[i] = self.random()
            C1p[i] = (gp['egg']**secret_sharesp[i]) * (pks[auth]['egga']**txp[i])
            C2p[i] = multiply(gp['g1'], (curve_order-txp[i]))
            C3p[i] = add(multiply(pks[auth]['gy'], txp[i]), multiply(gp['g1'], int(zero_sharesp[i])))
            C4p[i] = multiply(gp['F'](attr), txp[i])
            

            txhat[i]=(txp[i]-cp*tx[i])%curve_order
            secret_shareshat[i]=(secret_sharesp[i]-cp*secret_shares[i])%curve_order
            zero_shareshat[i]=(zero_sharesp[i]-cp*zero_shares[i])%curve_order
            assert(C1p[i] == gp['egg']**(secret_shareshat[i]%curve_order) * pks[auth]['egga']**(txhat[i]) *C1[i] ** (cp%curve_order))            
            # print("C1 "+attr+" check, passed")
            assert(eq(C2p[i],add(multiply(gp['g1'], (-txhat[i]) %curve_order), multiply(C2[i], cp))))
            # print("C2 "+attr+" check, passed")
            assert(eq(C3p[i],\
                add(add(multiply(pks[auth]['gy'], txhat[i]), \
                        multiply(gp['g1'], zero_shareshat[i])),\
                    multiply(C3[i],cp))))
            # print("C3 "+attr+" check, passed")
            assert(eq(C4p[i],add(multiply(gp['F'](attr), txhat[i]), multiply(C4[i], cp))))
            # print("C4 "+attr+" check, passed")

        c =int(hash(str(C0)+"||"+str(C1)+"||"+str(C2)+"||"+str(C3)+"||"+str(C4)),16)
        quotient=[0 for i in range(0,12)]
        dkg_pk=[0 for i in range(0,12)]
        dkg_pkp=[0 for i in range(0,12)]
        eta=[0 for i in range(0,12)]
        etap=[0 for i in range(0,12)]
        Mhat = (Mp - c*M)      
        zhat=zp-c*z  
        h=FQ(int(2**256*random.random())% field_modulus)
        k=FQ(int(2**256*random.random())% field_modulus)
        j=FQ(int(2**256*random.random())% field_modulus)
        for i in range(0, len(quotient)):            
            dkg_pk[i] = h ** (int(M.coeffs[i]))
            dkg_pkp[i] = h ** (int(Mp.coeffs[i]))                
            Mp_M=int(Mp.coeffs[i]) - c*int(M.coeffs[i])            
            quotient[i]=int((Mp_M - int(Mhat.coeffs[i]))//field_modulus)            
            # assert(dkg_pkp[i]* h**(-quotient[i]) == h**(int(Mhat.coeffs[i])) * dkg_pk[i]**c )
            eta[i]=j ** (int(M.coeffs[i])) * k ** z
            etap[i]=j ** (int(Mp.coeffs[i])) * k ** zp
            if zhat<0:
                assert(etap[i]* j**(-quotient[i]) * k**(-zhat) == j**(int(Mhat.coeffs[i]))  * eta[i]**c )
            else:
                assert(etap[i]* j**(-quotient[i]) == j**(int(Mhat.coeffs[i])) * k**zhat * eta[i]**c )
        
        # print({'policy': policy_str, 'C0': C0, 'C1': C1, 'C2': C2, 'C3': C3, 'C4': C4})
        return {'policy': policy_str, 'C0': C0, 'C1': C1, 'C2': C2, 'C3': C3, 'C4': C4,\
                                'C0p': C0p, 'C1p': C1p, 'C2p': C2p, 'C3p': C3p, 'C4p': C4p,\
                                "c": c,
                                "cp":cp,
                                # "Mp":Mp,
                                "sp":zp,
                                "txhat":txhat,  
                                "secret_shareshat":secret_shareshat,  
                                "zero_shareshat":zero_shareshat,  
                                "ztilde":ztilde,
                                "Mtilde":Mtilde,
                                "dkg_pk":dkg_pk,
                                "dkg_pkp":dkg_pkp,
                                "h":h,
                                "k":k,
                                "j":j,
                                "eta":eta,
                                "etap":etap,
                                "Mhat":Mhat,
                                "zhat":zhat,
                                "quotient":quotient,#element in FQ12 are in [0, field_modulus-1], the divi
                }

    def decrypt(self, gp, sk, ct):
        policy = self.abeutils.createPolicy(ct['policy'])
        # coefficients = self.abeutils.newGetCoefficients(policy)
        pruned_list = self.abeutils.prune(policy, sk['keys'].keys())
        coefficients = self.abeutils.newGetCoefficients(policy, pruned_list)
        # print(pruned_list)
        # print(coefficients)
        if not pruned_list:
            raise Exception("You don't have the required attributes for decryption!")

        B = bn128.FQ12([1] + [0] * 11)
        Bp = bn128.FQ12([1] + [0] * 11)
        
        for i in range(len(pruned_list)):
            x = pruned_list[i].getAttribute()  # without the underscore
            y = pruned_list[i].getAttributeAndIndex()  # with the underscore
            exp=int(coefficients[y])
            if exp < 0:
                exp+=bn128.curve_order

            a=bn128.pairing(ct['C2'][y], sk['keys'][x]['K'])
            b=bn128.pairing(ct['C3'][y], gp['H'](sk['GID']))
            c=bn128.pairing(sk['keys'][x]['KP'], ct['C4'][y])
            B = B*((ct['C1'][y]*a*b*c) ** exp)

            a=bn128.pairing(ct['C2p'][y], sk['keys'][x]['K'])
            b=bn128.pairing(ct['C3p'][y], gp['H'](sk['GID']))
            c=bn128.pairing(sk['keys'][x]['KP'], ct['C4p'][y])
            Bp = Bp*((ct['C1p'][y]*a*b*c) ** exp)
        # print("B===",B)
        if debug:
            print("Decrypt")
            print("SK:")
            print(sk)
            print("Decrypted Message:")
            print(ct['C0'] / B)
        # print(ct["C0"]/B == ct["C0p"]/Bp)
        return ct['C0'] / B


debug = False
if __name__ == '__main__':

    maabe = MaabeRW15()
    gp = maabe.setup() 
    (pk1, sk1) = maabe.authsetup(gp, "UT") 
    # print(pk, sk)
    user_attributes1 = ['STUDENT@UT', 'PHD@UT'] 
    user_keys1 = maabe.multiple_attributes_keygen(gp, sk1, "bob", user_attributes1) 
    # print(user_keys1)

    (pk2, sk2) = maabe.authsetup(gp, "OU") 
    user_attributes2 = ['STUDENT@OU'] 
    user_keys2 = maabe.multiple_attributes_keygen(gp, sk2, "bob", user_attributes2) 
    # print(user_keys2)



    public_keys = {'UT': pk1, 'OU': pk2} 
    # private_keys = {'UT': sk1, 'OU': sk2} 
    access_policy = '(2 of (STUDENT@UT, PROFESSOR@OU, (XXXX@UT or PHD@UT))) and (STUDENT@UT or MASTERS@OU)'
    # access_policy = 'STUDENT@UT and STUDENT@OU'
    # access_policy = 'STUDENT@UT'
    # access_policy = 'STUDENT@OU'
    message = gp["egg"]**maabe.random()
    print("message",message)
    cipher_text = maabe.encrypt(gp, public_keys, message, access_policy) 

    user_keys = {'GID': "bob", 'keys': merge_dicts(user_keys1, user_keys2)}
    decrypted_message = maabe.decrypt(gp, user_keys, cipher_text) 
    print("decrypted_message",decrypted_message)
    
    print(decrypted_message == message)












