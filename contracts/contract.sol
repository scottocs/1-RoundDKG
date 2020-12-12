pragma solidity ^0.5.17;
pragma experimental ABIEncoderV2;
// import "../contracts/BN256G2.sol";
// import { StringUtils } from "	../contracts/stringUtil.sol";

contract StoreVar {
	struct G1 {
	    uint x;
	    uint y;
	  }
	G1 g1 = G1(1,2);

	struct G2 {
	    uint xr;
	    uint xi;
	    uint yr;
	    uint yi;	    
	}
	G2 g2 = G2(
	    10857046999023057135944570762232829481370756359578518086990519993285655852781,
	    11559732032986387107991004021392285783925812861821192530917403151452391805634,
	    8495653923123431417604973247489272438418190587263600148770280649306958101930,
	    4082367875863433681332203403145435568316851327593401208105741076214120093531	    
	);
	uint256 field_modulus=21888242871839275222246405745257275088696311157297823662689037894645226208583;
	uint256 curve_order=21888242871839275222246405745257275088548364400416034343698204186575808495617;
	function modPow(uint256 base, uint256 exponent, uint256 modulus) internal returns (uint256) {
	    uint256[6] memory input = [32,32,32,base,exponent,modulus];
	    uint256[1] memory result;
	    assembly {
	      if iszero(call(not(0), 0x05, 0, input, 0xc0, result, 0x20)) {
	        revert(0, 0)
	      }
	    }
	    return result[0];
	}

	function compare(string memory _a, string memory _b)public returns (int) {
        bytes memory a = bytes(_a);
        bytes memory b = bytes(_b);
        uint minLength = a.length;
        if (b.length < minLength) minLength = b.length;
        //@todo unroll the loop into increments of 32 and do full 32 byte comparisons
        for (uint i = 0; i < minLength; i ++)
            if (a[i] < b[i])
                return -1;
            else if (a[i] > b[i])
                return 1;
        if (a.length < b.length)
            return -1;
        else if (a.length > b.length)
            return 1;
        else
            return 0;
    }
    /// @dev Compares two strings and returns true iff they are equal.
    function equal(string memory _a, string memory _b) public returns (bool) {
        return compare(_a, _b) == 0;
    }
    /// @dev Finds the index of the first occurrence of _needle in _haystack
    function indexOf(string memory _haystack, string memory _needle) public returns (int)
    {
    	bytes memory h = bytes(_haystack);
    	bytes memory n = bytes(_needle);
    	if(h.length < 1 || n.length < 1 || (n.length > h.length)) 
    		return -1;
    	else if(h.length > (2**128 -1)) // since we have to be able to return -1 (if the char isn't found or input error), this function must return an "int" type with a max length of (2^128 - 1)
    		return -1;									
    	else
    	{
    		uint subindex = 0;
    		for (uint i = 0; i < h.length; i ++)
    		{
    			if (h[i] == n[0]) // found the first char of b
    			{
    				subindex = 1;
    				while(subindex < n.length && (i + subindex) < h.length && h[i + subindex] == n[subindex]) // search until the chars don't match or until we reach the end of a or b
    				{
    					subindex++;
    				}	
    				if(subindex == n.length)
    					return int(i);
    			}
    		}
    		return -1;
    	}	
    }
    uint8 public _myVar;
    event MyEvent(uint indexed _var);
    event Ciphertext(
        address issuer,        
        // uint256[] C0, //(g1,g2)
        uint256 a,
        uint256 b,
        uint256 c,
        uint256 d
        // uint256[] C0_2 //(g1,g2)
        
    );
    function setVar(uint8 _var) public {
        _myVar = _var;
        emit MyEvent(_var);
    }

    function getVar() public view returns (uint8) {
        return _myVar;
    }


    address[] public addresses;
    // maps storing information required to perform in-contract validition for each registered node
    // mapping (address => uint256[2]) public public_keys;
    // mapping (address => bytes32) public abe_ciphertext;
    // mapping (address => uint256[2]) public commitments_1st_coefficient;
    // mapping (address => uint256[2]) public key_shares;
 //    struct G1 {
	//     uint x;
	//     uint y;
	// }
    
    // G2 g2 = G2(
    //     11559732032986387107991004021392285783925812861821192530917403151452391805634,
    //     10857046999023057135944570762232829481370756359578518086990519993285655852781,
    //     4082367875863433681332203403145435568316851327593401208105741076214120093531,
    //     8495653923123431417604973247489272438418190587263600148770280649306958101930
    // );
	uint256 pminus = field_modulus-1;
  	uint256 pplus = field_modulus+1;

    function hashToG1(uint[] memory b) internal returns (G1 memory) {
	    uint x = 0;
	    while (true) {
	      uint256 hx = uint256(keccak256(abi.encodePacked(b,byte(uint8(x)))))%field_modulus;
	      uint256 px = (modPow(hx,3,field_modulus) + 3);
	      if (modPow(px, pminus/2, field_modulus) == 1) {
	        uint256 py = modPow(px, pplus/4, field_modulus);
	        if (uint(keccak256(abi.encodePacked(b,byte(uint8(255)))))%2 == 0)
	          return G1(hx,py);
	        else
	          return G1(hx,field_modulus-py);
	      } else {
	        x++;
	      }
	    }
	}

  function bn128_check_pairing(uint256[12] memory input)
    public returns (bool) {
        uint256[1] memory result;
        bool success;
        assembly {
            // 0x08     id of precompiled bn256Pairing contract     (checking the elliptic curve pairings)
            // 0        number of ether to transfer
            // 384       size of call parameters, i.e. 12*256 bits == 384 bytes
            // 32        size of result (one 32 byte boolean!)
            success := call(sub(gas, 2000), 0x08, 0, input, 384, result, 32)
        }
        require(success, "elliptic curve pairing failed");
        return result[0] == 1;
    }
   	function testSimpleArray(string memory json) public  returns (bool) {
        // string memory json = '{"outerKey": [{"g2": 1}, {"innerKey2": "value"}]}';

  //       uint returnValue;
  //       JsmnSolLib.Token[] memory tokens;
  //       uint actualNum;

  //       (returnValue, tokens, actualNum) = JsmnSolLib.parse(json, 10);
  //       // uint256[] memory unfixedArr = new uint256[](2); 
  //       // unfixedArr[0]=(returnValue);
  //       // unfixedArr[1]=(actualNum);
		// // emit Ciphertext(msg.sender, unfixedArr);


  //       JsmnSolLib.Token memory t = tokens[2];
  //       string memory key="C0";
  //       string memory value="";
  //       bool found=false;
  //       for(uint i=0;i<tokens.length;i++){
  //       	JsmnSolLib.Token memory t1 = tokens[i];
  //   //     	if(equal(key, JsmnSolLib.getBytes(json, t1.start, t1.end))){
		// 		// found=true;
		// 		// continue;
  //   //     	}
  //   //     	if(found){
  //   //     		value=JsmnSolLib.getBytes(json, t1.start, t1.end);
		// 		// emit Ciphertext(msg.sender, value);	
		// 		// found=false;
  //   //     	}
  //       	value=JsmnSolLib.getBytes(json, t1.start, t1.end);
		// 	emit Ciphertext(msg.sender, value);
  //       }
        
  //       return t.jsmnType == JsmnSolLib.JsmnType.ARRAY;
  		return false;
        // Assert.equal(returnValue, RETURN_SUCCESS, 'Valid JSON should return a success.');
        // Assert.isTrue(t.jsmnType == JsmnSolLib.JsmnType.ARRAY, 'Not an array');
    }
    function addPoints(G1 memory a, G1 memory b) internal returns (G1 memory) {
	    uint256[4] memory input = [a.x, a.y, b.x, b.y];
	    uint[2] memory result;
	    assembly {
	      if iszero(call(not(0), 0x06, 0, input, 0x80, result, 0x40)) {
	        revert(0, 0)
	      }
	    }
	    return G1(result[0], result[1]);
	}
 //    function chkBit(bytes memory b, uint x) public pure returns (bool) {
	//     return uint(uint8(b[x/8]))&(uint(1)<<(x%8)) != 0;
	// }
 //    function sumPoints(G1[] memory points, bytes memory indices) internal returns (G1 memory) {
	//     G1 memory acc = G1(0,0);
	//     for (uint i = 0; i < points.length; i++) {
	//       if (chkBit(indices, i)) {
	//         acc = addPoints(acc, points[i]);
	//       }
	//     }
	//     return G1(acc.x, acc.y);
	// }

	function scalarMultiply(G1 memory point, uint256 scalar) internal returns(G1 memory) {
	    uint256[3] memory input = [point.x, point.y, scalar];
	    uint[2] memory result;
	    assembly {
	      if iszero(call(not(0), 0x07, 0, input, 0x60, result, 0x40)) {
	        revert(0, 0)
	      }
	    }
	    return G1(result[0], result[1]);
	}

   //  function writeCT(string memory C0) public{
   // 		bool r=testSimpleArray(C0);
   // // 		if(r){
   // // 			uint256[] memory unfixedArr = new uint[](1); 
   // // 			emit Ciphertext(msg.sender, unfixedArr);	
   // // 		}else{
			// // emit Ciphertext(msg.sender, C0);	
   // 		// }
        
   //  }
   // "policy","C0","C1","C2","C3","C4","C0p","C1p","C2p","C3p","C4p","c","cp","sp","txhat","secret_shareshat","zero_shareshat","ztilde","Mtilde","dkg_pk","dkg_pkp","h","k","j","eta","etap","Mhat","zhat","quotient"
   struct CT {

   		uint256 c;
		uint256 cp;
		string policy;
   		uint256 ztilde;
   		uint256[] Mtilde;
   		uint256[] dkg_pk;
   		uint256[] dkg_pkp;
		uint256 h;
		uint256 k;
		uint256 j;
		// uint256[] eta;
		// uint256[] etap;
		uint256[] Mhat;
		uint256 zhat;
		uint256[] quotient;
		uint256[] C0_1;
		uint256[] C0p_1;
		uint256[] egg_1;
		uint256[] egga_1;
		uint256[] g1;
		uint256[] g2;
		uint256[] C1_1;
		uint256[] C1p_1;
		uint256[] C2;
    uint256[] CHat2;
		uint256[] C2p;
    uint256[] CHat2p;
		uint256[] C3;
    uint256[] CHat3;
		uint256[] C3p;
    uint256[] CHat3p;
		uint256[] C4;
		uint256[] C4p;
		uint256[] zero_shareshat;
		uint256[] secret_shareshat;
		uint256[] txhat;
		string[] attr;
		string[] attr_unpacked;
		uint256[] gy;
		uint256[] g2y;

	    // address recipient;
	    // uint contributed;
	    // uint goal;
	    // uint deadline;
	    // uint num_contributions;
	    // mapping(uint => Contribution) contributions;
	}
	// function mulMod(uint256 a, uint256 b, uint256 mod)internal returns(uint256){
	// 	// def mulmod(a, b, mod):  
 //    	uint256 res = 0; 
 //    	a = a % mod; 
	//     while (b > 0){
	//         if (b % 2 == 1){
	//             res = (res + a) % mod;
	//         }
	//         a = (a * 2) % mod;         
	//         b = b/2; 
	//     }
	//     return res;
 //    // return res % mod; 
	// }

	
	// function checketa(CT memory ct) public{
 //   		uint256 k=ct.k;
 //   		uint256 j=ct.j;
 //   		uint256 c=ct.c;   		
 //   		uint256 zhat=ct.zhat;
 //   		uint256[] memory eta=ct.eta;
 //   		uint256[] memory etap=ct.etap;
 //   		uint256[] memory quo=ct.quotient;
 //   		uint256[] memory Mhat=ct.Mhat;
 //        for (uint256 i = 0; i < ct.quotient.length; i += 1) {        	
 //        	uint256 a1=modPow(j,Mhat[i],field_modulus);
 //        	uint256 a2=modPow(j,quo[i], field_modulus);
 //        	uint256 a3=modPow(k,zhat,field_modulus);
 //        	uint256 a4=modPow(eta[i], c, field_modulus);
 //        	uint256 b1=mulmod(a1,a2,field_modulus);
	//         uint256 b2=mulmod(a3,a4,field_modulus);	        	
 //        	require(etap[i] == mulmod(b1,b2,field_modulus),
 //        		"eta check failed");
 //        }
	// }
  struct CTPK {
      uint256 j;
      uint256 h;
      uint256 c;
      uint256[] Mhat;
      uint256[] quotient;
      uint256[] dkg_pk;
      uint256[] dkg_pkp;
    }
	function checkdkg_pk(CTPK memory ctpk) public{
   		uint256 j=ctpk.j;
   		uint256 h=ctpk.h;
   		uint256 c=ctpk.c;   		
   		uint256[] memory Mhat=ctpk.Mhat;
   		uint256[] memory quo=ctpk.quotient;
   		uint256[] memory dkg_pk=ctpk.dkg_pk;
   		uint256[] memory dkg_pkp=ctpk.dkg_pkp;
        for (uint256 i = 0; i < 12; i += 1) {        	
        	uint256 a1=modPow(h,Mhat[i],field_modulus);
        	uint256 a2=modPow(h,quo[i],field_modulus);
        	uint256 a3=modPow(dkg_pk[i],c,field_modulus);        	
        	uint256 b1=mulmod(a1,a2,field_modulus);	       	
        	require(dkg_pkp[i] == mulmod(b1,a3,field_modulus),"dkg_pk check failed");
        }
	}
  struct CT0 {
    uint256[] Mtilde;
    uint256[] egg_1;
    uint256[] C0_1;
    uint256[] C0p_1;
    uint256 ztilde;
    uint256 cp;
  }
	function checkC0(CT0 memory ct0) public{
		G1 memory Mtilde = G1(ct0.Mtilde[0],ct0.Mtilde[1]);
   		G1 memory egg_1 = G1(ct0.egg_1[0],ct0.egg_1[1]);
   		G1 memory C0_1 = G1(ct0.C0_1[0],ct0.C0_1[1]);
   		G1 memory left = G1(ct0.C0p_1[0],ct0.C0p_1[1]);
   		// G1 memory right = G1(ct0.C0p_1[0],ct0.C0p_1[1]);
   		// scalarMultiply(egg_1, 1);
   		G1 memory right =addPoints(addPoints(Mtilde, scalarMultiply(egg_1, ct0.ztilde)), scalarMultiply(C0_1, ct0.cp));
   		require(
            left.x==right.x && left.y == right.y,
            "C0 check failed"
        );
	}
  struct CT1 {
    uint256 cp;
    uint256[]  C1_1;
    uint256[]  C1p_1;
    uint256[]  secret_shareshat;
    uint256[]  txhat;
    uint256[]  egg_1;
    uint256[]  egga_1;
  }
	function checkC1(CT1 memory ct1) public{
		uint256 cp=ct1.cp;
   		uint256[] memory C1_1=ct1.C1_1;
	    uint256[] memory C1p_1=ct1.C1p_1;
	    uint256[] memory secret_shareshat=ct1.secret_shareshat;
	    uint256[] memory txhat=ct1.txhat;
	    G1 memory egg_1 = G1(ct1.egg_1[0],ct1.egg_1[1]);	    
	    
   		
        for (uint256 i = 0; i < C1_1.length; i += 2) {    
        	G1 memory eggai = G1(ct1.egga_1[i],ct1.egga_1[i+1]);    	
        	G1 memory C1i = G1(C1_1[i], C1_1[i+1]);
        	G1 memory left = G1(C1p_1[i], C1p_1[i+1]);
        	G1 memory p1=scalarMultiply(egg_1,secret_shareshat[i/2]);
        	G1 memory p2=scalarMultiply(eggai, txhat[i/2]);
        	G1 memory p3=scalarMultiply(C1i, cp);
        	G1 memory right =addPoints(addPoints(p1, p2), p3);
        	
        	require(left.x==right.x && left.y == right.y,
            		"C1 check failed");

        }
	}
	function stringToUintArray(string memory s) internal returns (uint256[] memory) {	    
	    bytes memory b = bytes(s);
	    uint256[] memory result = new uint256[](b.length);
	    
	    for (uint i = 0; i < b.length; i++) { 
	        result[i] = uint256(uint8(b[i]));
	    }
	    // emit Ciphertext(msg.sender, result[0],result[1]);
	    return result;
	}
	// function scalarMultiplyG2(uint256[] memory arr, uint256 sca) internal returns(G2 memory){
	// 	uint256 newxr;
 //   		uint256 newxi;
 //   		uint256 newyr;
 //   		uint256 newyi;
 //        (newxr,newxi,newyr,newyi)=BN256G2.ECTwistMul(sca, arr[0], arr[1], arr[2], arr[3]); 
 //        return G2(newxr,newxi,newyr,newyi);
	// }
	// function scalarMultiplyG2(G2 memory p, uint256 sca) internal returns(G2 memory){
	// 	uint256 newxr;
 //   		uint256 newxi;
 //   		uint256 newyr;
 //   		uint256 newyi;
 //        (newxr,newxi,newyr,newyi)=BN256G2.ECTwistMul(sca, p.xr, p.xi, p.yr, p.yi);   		
 //        return G2(newxr,newxi,newyr,newyi);
	// }
	// function addPointsG2(G2 memory p1, G2 memory p2) internal returns(G2 memory){
	// 	uint256 newxr;
 //   		uint256 newxi;
 //   		uint256 newyr;
 //   		uint256 newyi;
 //        (newxr,newxi,newyr,newyi)=BN256G2.ECTwistAdd(p1.xr, p1.xi, p1.yr, p1.yi, p2.xr, p2.xi, p2.yr, p2.yi);
 //        return G2(newxr,newxi,newyr,newyi);
	// }
	// function checkC2(CT memory ct, uint256 start, uint256 end) public{
	// 	uint256 cp=ct.cp;
	// 	uint256[] memory ct_g1=ct.g1;
 //   		uint256[] memory C2=ct.C2;
	//     uint256[] memory C2p=ct.C2p;
	//     uint256[] memory txhat=ct.txhat;
	    
 //        for (uint256 i = start; i < end; i += 4) {
 //        	G2 memory left = G2(C2p[i], C2p[i+1],C2p[i+2],C2p[i+3]);
 //        	G2 memory C2i = G2(C2[i], C2[i+1], C2[i+2], C2[i+3]);
 //        	G2 memory p1=scalarMultiplyG2(ct_g1, curve_order-txhat[i/4]);
 //        	G2 memory p2=scalarMultiplyG2(C2i, cp);
 //        	G2 memory right=addPointsG2(p1,p2);
 //        	emit Ciphertext(msg.sender, p1.xr,p1.xi,p1.yr,p1.yi);
 //        	require(left.xr ==right.xr && left.xi ==right.xi && left.yr == right.yr && left.yi == right.yi,
 //            		"C2 check failed");        	
        	
 //        }        
	// }
// function checkC3(CT memory ct, uint256 start, uint256 end) public{
//     uint256 cp=ct.cp;
//     uint256[] memory ct_g1=ct.g1;
//       uint256[] memory C3=ct.C3;
//       uint256[] memory C3p=ct.C3p;
//       uint256[] memory txhat=ct.txhat;
//       uint256[] memory gy = ct.gy;
//       uint256[] memory zero_shareshat=ct.zero_shareshat;
      
      
//         for (uint256 i = start; i < end; i += 4) {    
          
//           G2 memory left = G2(C3p[i], C3p[i+1],C3p[i+2],C3p[i+3]);

//           G2 memory C3i = G2(C3[i], C3[i+1], C3[i+2], C3[i+3]);
//           G2 memory gyi = G2(gy[i], gy[i+1], gy[i+2], gy[i+3]);
//           G2 memory p1=scalarMultiplyG2(gyi, txhat[i/4]);
//           G2 memory p2=scalarMultiplyG2(ct_g1, zero_shareshat[i/4]);
//           G2 memory p3=scalarMultiplyG2(C3i, cp);
//           G2 memory right=addPointsG2(addPointsG2(p1,p2),p3);
//           emit Ciphertext(msg.sender, right.xr,right.xi,right.yr,right.yi);
//           require(left.xr ==right.xr && left.xi ==right.xi && left.yr == right.yr && left.yi == right.yi,
//                 "C3 check failed");         
//           // assert(eq(C3p[i],\
//          //    add(add(multiply(pks[auth]['gy'], txhat[i]), multiply(gp['g1'], zero_shareshat[i])),\
//          //        multiply(C3[i],cp))))
        
//         }        
//   }
  struct CT2 {
    uint256 cp;
    uint256[] g1;
    uint256[] g2;
    uint256[] C2;
    uint256[] C2p;
    uint256[] CHat2;
    uint256[] CHat2p;
    uint256[] txhat;
  }
  function checkC2New(CT2 memory ct2) public{
      // uint256[] memory myG1=ct.g2;
      uint256[] memory myG2=ct2.g1; 
      G1 memory ct_g2=G1(ct2.g2[0], ct2.g2[1]);
         
      // uint256[] memory C2=ct2.C2;
      uint256[] memory C2p=ct2.C2p;
      uint256[] memory CHat2=ct2.CHat2;
      uint256[] memory CHat2p=ct2.CHat2p;
      uint256[] memory txhat=ct2.txhat;
      
        for (uint256 i = 0; i < C2p.length; i += 4) {
          G1 memory left = G1(CHat2p[i/2],CHat2p[i/2+1]);      
          G1 memory C2Hati = G1(CHat2[i/2], CHat2[i/2+1]);        
          G1 memory p1=scalarMultiply(ct_g2, curve_order-txhat[i/4]);
          G1 memory p2=scalarMultiply(C2Hati, ct2.cp);
          G1 memory right=addPoints(p1,p2);
          
          require(bn128_check_pairing([left.x, left.y,
                myG2[1], myG2[0],myG2[3],myG2[2],
                ct_g2.x, field_modulus - ct_g2.y,
                C2p[i+1],C2p[i],C2p[i+3],C2p[i+2]]), "C2New Pairing check failed" );
          require(left.x ==right.x && left.y == right.y, "C2New G1 check failed");         
          
        }        
  }
    struct CT3 {
      uint256 cp;
      uint256[] g1;
      uint256[] g2;
      uint256[] C3p;
      uint256[] CHat3;
      uint256[] CHat3p;
      uint256[] txhat;
      uint256[] g2y;
      uint256[] zero_shareshat;
    }
    function checkC3New(CT3 memory ct3) public{
      // uint256[] memory myG1=ct.g2;
      uint256 cp=ct3.cp;
      uint256[] memory myG2=ct3.g1; 
      G1 memory ct_g2=G1(ct3.g2[0], ct3.g2[1]);

      uint256[] memory C3p=ct3.C3p;
      uint256[] memory CHat3=ct3.CHat3;
      uint256[] memory CHat3p=ct3.CHat3p;
      uint256[] memory txhat=ct3.txhat;
      uint256[] memory g2y = ct3.g2y;
      uint256[] memory zero_shareshat=ct3.zero_shareshat;
      
      for (uint256 i = 0; i < C3p.length; i += 4) {
        G1 memory left = G1(CHat3p[i/2],CHat3p[i/2+1]);      
        // G1 memory C3Hati = G1(CHat3[i/2], CHat3[i/2+1]); 
        // G1 memory g2yi = G1(g2y[i/2], g2y[i/2+1]);       
        G1 memory p1=scalarMultiply(G1(g2y[i/2], g2y[i/2+1]), txhat[i/4]);
        G1 memory p2=scalarMultiply(ct_g2, zero_shareshat[i/4]);
        G1 memory p3=scalarMultiply(G1(CHat3[i/2], CHat3[i/2+1]), cp);
        G1 memory right=addPoints(addPoints(p1,p2),p3);        
        require(left.x ==right.x && left.y == right.y, "C3New G1 check failed");         
        
      }  
      for (uint256 i = 0; i < C3p.length; i += 4) {
        G1 memory left = G1(CHat3p[i/2],CHat3p[i/2+1]);      
        require(bn128_check_pairing([left.x, left.y,
              myG2[1], myG2[0],myG2[3],myG2[2],
              ct_g2.x, field_modulus - ct_g2.y,
              C3p[i+1],C3p[i],C3p[i+3],C3p[i+2]]), "C3New Pairing check failed" );        
      }        
  }


	struct CT4 {
      uint256 cp;
      string[] attr_unpacked;
      uint256[] C4;
      uint256[] C4p;
      uint256[] txhat;
    }

	function checkC4(CT4 memory ct4) public{
		// string[] memory attr = ct.attr;
		string[] memory attr_unpacked = ct4.attr_unpacked;
		uint256 cp=ct4.cp;
 		uint256[] memory C4=ct4.C4;
    uint256[] memory C4p=ct4.C4p;
    uint256[] memory txhat=ct4.txhat;
    
      for (uint256 i = 0; i < C4.length; i += 2) {    
      	
      	G1 memory left = G1(C4p[i], C4p[i+1]);

      	G1 memory C4i = G1(C4[i], C4[i+1]);
      	G1 memory p1=scalarMultiply(hashToG1(stringToUintArray(attr_unpacked[i/2])), txhat[i/2]);
      	G1 memory p2=scalarMultiply(C4i, cp);
      	G1 memory right=addPoints(p1,p2);
      	require(left.x==right.x && left.y == right.y, "C4 check failed");        	
      }
	}

	

    function writeCT(CT memory ct) public{
   		
   		// checkdkg_pk(ct);
   		// checkC0(ct);
   		// checkC1(ct);
   		// checkC2New(ct);
   		// checkC2New(ct);
   		// checkC4(ct);
   		
   		
    }


}