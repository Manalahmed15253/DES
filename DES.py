import numpy as np
import time
import string

#some useful variables and their values in a dictionary, all the standared given DES tables
useful_tables = {
	"IP" : [
			58, 50, 42, 34, 26, 18, 10, 2,
			60, 52, 44, 36, 28, 20, 12, 4,
			62, 54, 46, 38, 30, 22, 14, 6,
			64, 56, 48, 40, 32, 24, 16, 8,
			57, 49, 41, 33, 25, 17, 9, 1,
			59, 51, 43, 35, 27, 19, 11, 3,
			61, 53, 45, 37, 29, 21, 13, 5,
			63, 55, 47, 39, 31, 23, 15, 7
			],

	"FP" : [  
			40, 8, 48, 16, 56, 24, 64, 32,
			39, 7, 47, 15, 55, 23, 63, 31,
			38, 6, 46, 14, 54, 22, 62, 30,
			37, 5, 45, 13, 53, 21, 61, 29,
			36, 4, 44, 12, 52, 20, 60, 28,
			35, 3, 43, 11, 51, 19, 59, 27,
		 	34, 2, 42, 10, 50, 18, 58, 26,
			33, 1, 41, 9, 49, 17, 57, 25  
			],

	"EBox" : [
				32, 1, 2, 3, 4, 5,
			  	4, 5, 6, 7, 8, 9,
			  	8, 9, 10, 11, 12, 13,
		      	12, 13, 14, 15, 16, 17,
			  	16, 17, 18, 19, 20, 21,
			  	20, 21, 22, 23, 24, 25,
			  	24, 25, 26, 27, 28, 29,
			  	28, 29, 30, 31, 32, 1
			  ],
	
	"SBox" : [
		# S1
		[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
		 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
		 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
		 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

		# S2
		[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
		 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
		 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
		 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

		# S3
		[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
		 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
		 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
		 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

		# S4
		[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
		 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
		 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
		 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

		# S5
		[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
		 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
		 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
		 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

		# S6
		[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
		 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
		 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
		 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

		# S7
		[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
		 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
		 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
		 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

		# S8
		[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
		 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
		 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
		 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
	],

	"F_Box" : [16, 7, 20, 21, 29, 12, 28, 17,
              1, 15, 23, 26, 5, 18, 31, 10,
              2, 8, 24, 14, 32, 27, 3, 9,
              19, 13, 30, 6, 22, 11, 4, 25 ],

	"pc2" : [14,    17,   11,    24,     1,    5,
                  3,    28,   15,     6,    21,   10,
                 23,    19,   12,     4,    26,    8,
                 16,     7,   27,    20,    13,    2,
                 41,    52,   31,    37,    47,   55,
                 30,    40,   51,    45,    33,   48,
                 44,    49,   39,    56,    34,  53,
                 46,    42,   50,    36,    29,   32],

	"pc1" : [ 
				57, 49, 41, 33, 25, 17, 9,
				1, 58, 50, 42, 34, 26, 18,
				10, 2, 59, 51, 43, 35, 27,
				19, 11, 3, 60, 52, 44, 36,
				63, 55, 47, 39, 31, 23, 15,
				7, 62, 54, 46, 38, 30, 22,
				14, 6, 61, 53, 45, 37, 29,
				21, 13, 5, 28, 20, 12, 4
				],

}

"""Key formatting helper functions"""
#1st we get the 64 bits key as an input and use permutation choice 1 to get only 56 bits as an output
def key_permutation1(key):
	#empty array to caryy the 56 bits
    permute1 = np.empty_like(useful_tables["pc1"])
    for i in range(56):
		#taking the corresponding bits from the input key
        permute1[i]=key[useful_tables["pc1"][i]-1]   
    return(permute1)
#2nd we do the left shift using left shift round table
def key_circular_shift(toshift,n):
	#if we look at the table we shift by 1 in the round number 1,2,9 and 16. 
    if (n == 1) or (n == 2) or (n == 9) or (n == 16):
        toshift= np.roll(toshift,-1)
        return toshift
	#the rest round numbers are shifted by 2
    else:
        toshift = np.roll(toshift, -2)
        return toshift
#3rd get the 16-56 bits keys as an input and use permutation choice 2 to get only 16-48 bits keys as an output
def key_permutation2(keys):
    permute2 = np.empty([16,48])
    l = 0
    for k in keys:
        j = 0
        for i in useful_tables["pc2"]:
            permute2[l][j] = k[i - 1]
            j += 1
        l += 1
    return permute2
#The function that generates the 16 keys, it takes the 64 bit key and output the 16-48 bits keys
#by using the helper functions above
def Key_Generator(key):
	#64bit key is now 56 bit key
    key=key_permutation1(key)  
	#spliting the key to right and left each is 28 bit 
    left = key[0:28]
    right = key[28:56]
	#empty numpy arrays to carry the keys
    shifted = np.zeros(56)
    key16 = np.zeros([16,56])
	#to generate the 16 keys
    for i in range(1,17):
        shifted[0:28] = key_circular_shift(left,i)
        shifted[28:56] = key_circular_shift(right,i)
        left = shifted[0:28]
        right = shifted[28:56]
    #saving the key in the array key16
        key16[i - 1] = shifted
    #the 16-56 bits keys is now 16-48 bits keys
    key16 = key_permutation2(key16)
    key16 = [list(map(int, x)) for x in key16]
    key16 = np.array(key16)
    return key16

"""data formatting helper functions"""
#we take the input in Hexadecimal and the operations needs binary bits so we need to convert
def HexaToBinary(s): 
    Mapping = {'0' : "0000",  
          '1' : "0001", 
          '2' : "0010",  
          '3' : "0011", 
          '4' : "0100", 
          '5' : "0101",  
          '6' : "0110", 
          '7' : "0111",  
          '8' : "1000", 
          '9' : "1001",  
          'A' : "1010", 
          'B' : "1011",  
          'C' : "1100", 
          'D' : "1101",  
          'E' : "1110", 
          'F' : "1111",
		  'a' : "1010", 
          'b' : "1011",  
          'c' : "1100", 
          'd' : "1101",  
          'e' : "1110", 
          'f' : "1111",
		  } 
    binary = "" 
    for i in range(len(s)): 
        binary = binary + Mapping[s[i]] 
    return binary
#1st we take the 64 bits data and do the initial permutaion, output is 64 bits data but in different arrangement
def initial_permutation(data):  
	permute1 = np.empty_like(useful_tables["IP"])
	j = 0
	for i in useful_tables["IP"]:
		permute1[j] = data[i-1]
		j += 1
	return permute1
#2nd we divide the data to left and right parts each is 32bit and apply function F on the right part with the key
"""Function F helper functions"""
#the function F takes the right part but after expansion, let's write the function F helper functions
#Expansion takes the 32 bits and produce 48 bits using the expansion table
def E_Box_Operation(righ_part):
    right_expanded = np.empty(48)
    j = 0
    for i in useful_tables["EBox"]:
        right_expanded[j] = righ_part[i - 1]
        j += 1
    right_expanded = list(map(int,right_expanded))
    right_expanded = np.array(right_expanded)
    return right_expanded
#we need to xor the right part with the key, also the left part with the output of the function F
def xor(arg1,arg2):
    Xored = np.logical_xor(arg1,arg2)
    Xored  = Xored.astype(int)
    return Xored
#to get the correct sbox table from the useful dict
def SBox_Looping(sinput,x):
    tableno = x - 1
    row = int((np.array2string(sinput[0]) + np.array2string(sinput[5])),2)
    column = sinput[1:5]
    column = np.array2string(column)
    column = column[1:8].replace(" ", "")
    column = int(column,2)
    
    elementno = (16 * row) + column
    soutput = useful_tables["SBox"][tableno][elementno]
    soutput = list(np.binary_repr(soutput, width=4))

    soutput= np.array(list(map(int, soutput)))
    return soutput
#SBox operation on the 48 bits key, it returns 32 bits key by using the 8 Sbox tables
def sbox(sboxin):
    sboxin1 = sboxin[0:6]
    sboxout1 = SBox_Looping(sboxin1,1)
    sboxin2 = sboxin[6:12]
    sboxout2 = SBox_Looping(sboxin2,2)
    sboxin3 = sboxin[12:18]
    sboxout3 = SBox_Looping(sboxin3, 3)
    sboxin4 = sboxin[18:24]
    sboxout4 = SBox_Looping(sboxin4, 4)
    sboxin5 = sboxin[24:30]
    sboxout5 = SBox_Looping(sboxin5, 5)
    sboxin6 = sboxin[30:36]
    sboxout6 = SBox_Looping(sboxin6, 6)
    sboxin7 = sboxin[36:42]
    sboxout7 = SBox_Looping(sboxin7, 7)
    sboxin8 = sboxin[42:48]
    sboxout8 = SBox_Looping(sboxin8, 8)
    sboxout = np.concatenate([sboxout1,sboxout2,sboxout3,sboxout4,sboxout5,sboxout6,sboxout7,sboxout8])
    return sboxout
#Function F permutation (last operation in the function F), takes the 32 bits and produce 32 bits with different arrangement
def F_permutation(topermute):
    permuted= np.empty(32)
    j = 0
    for i in useful_tables["F_Box"]:
        permuted[j] = topermute[i - 1]
        j += 1
    return permuted
#Now we can create our function F using the helper function abovr
def F(right,key):
	#1st expansion
    expanded = E_Box_Operation(right)
	#2nd xor with the key
    xored = xor(expanded,key)
	#3rd apply sbox
    sboxed = sbox(xored)
	#4th do the prmutation
    output_F = F_permutation(sboxed)
    return output_F
#Implementing the round function, which will be called 16 times
def round(data,rkey):
	#dividing the data to left and right parts
    l0 = data[0:32]
    r0 = data[32:64]
	#applying the F function
    output_F = F(r0,rkey)
	#the output of the round
    r1 = xor(l0,output_F)
    l1 = r0
    returndata = np.empty_like(data)
    returndata[0:32] = l1
    returndata[32:64] = r1
    return(returndata)
#after finishing we need to do the Final permutation which is the inverse of the initial permutation
def Final_permutation(data):  
	permute2 = np.empty_like(useful_tables["FP"])
	k = 0
	for l in useful_tables["FP"]:
		permute2[k] = data[l-1]
		k += 1
	return(permute2)
#we produce the output in hexadecimal so we need to convert the binary to hexa
def BinaryToHexa(s): 
    Mapping = {
		  "0000" : '0',  
          "0001" : '1', 
          "0010" : '2',  
          "0011" : '3', 
          "0100" : '4', 
          "0101" : '5',  
          "0110" : '6', 
          "0111" : '7',  
          "1000" : '8', 
          "1001" : '9',  
          "1010" : 'A', 
          "1011" : 'B',  
          "1100" : 'C', 
          "1101" : 'D',  
          "1110" : 'E', 
          "1111" : 'F' 
		  } 
    hexa = "" 
    for i in range(0,len(s),4): 
        ch = "" 
        ch = ch + s[i] 
        ch = ch + s[i + 1]  
        ch = ch + s[i + 2]  
        ch = ch + s[i + 3]  
        hexa = hexa + Mapping[ch] 
          
    return hexa
"""The DES encryption function which uses all the above helper functions"""
def DES_Encryption(data,key16,no_of_encryption):  
    for k in range(int (no_of_encryption)):
        data = initial_permutation(data)
        for i in range(16):
            data = round(data,key16[i])
        #the swapping before the next round
        data = np.roll(data,32)
        data = (Final_permutation(data))
	#to output the data in the form of string
    encrypted=""
    encrypted = np.array_str(data)
    encrypted= encrypted.replace(" ","")
    encrypted = encrypted.replace('[','')
    encrypted = encrypted.replace(']','')
    encrypted = encrypted.replace('\n','')
    #convert from binary to hexa
    encrypted=BinaryToHexa(encrypted)           
    return encrypted
"""The DES decryption function which uses all the above helper functions"""
def DES_Decryption(data,key16):
    data = initial_permutation(data)
    for i in range(16):
        data = round(data, key16[16 - (i + 1)])
    data = np.roll(data, 32)
    data = (Final_permutation(data))
    #convert from array to string
    decrypted=""
    decrypted = np.array_str(data)
    decrypted= decrypted.replace(" ","")
    decrypted = decrypted.replace('[','')
    decrypted = decrypted.replace(']','')
    decrypted = decrypted.replace('\n','')
    #convert from binary to hexa
    decrypted=BinaryToHexa(decrypted)
    return decrypted

def main():
    print("Enter your desired 16 Hex characters key for DES: ")
    key=input()
    print("Enter your desired 16 Hex characters block for DES: ")
    data=input()
    print("Enter 0 For Encryption, 1 For Decryption: ")   
    enc_or_dec =input()
    enc_or_dec = int(enc_or_dec)
    key=HexaToBinary(key)
    data=HexaToBinary(data)
    key_array=[]
    data_array=[]
    for i in range(64):
        key_array.append(key[i])   
    for i in range(64):
        data_array.append(data[i])    
    key16= Key_Generator(key_array)
    if enc_or_dec == 0:
        print("Enter your desired number of times (1 is the minimum) to run the encryption: ")
        no_of_encryption=input()
        encrypted = DES_Encryption(data_array,key16,no_of_encryption)
        print("Your Encrypted Block of Data is : " + encrypted )	
    elif enc_or_dec == 1:
        print("The Decrypted Data is : " + DES_Decryption(data_array,key16))
    else:
        print("Error, Read the instructions again")
    print("want another operation?, Enter Yes or No")
    answer = input()
    answer = answer.lower()
    if answer == "no":
        print("Bye!")
    elif answer == "yes":
        main()
    else:
        print("Error!!")
main()
