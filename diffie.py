#!/usr/bin/python3.5
import random, binascii, os, threading
"""This script is intended to test the Diffie-Hellman Key
exchange.

I've added the ability to run the key exchange multiple times,
concatenating the results until the key is >= 256 bits.

-codeDirtyToMe"""

#These values are used to control the key exchange loop and to store the final key.
sharedBinKey = []
sharedDecKey = []

#Repeat the key exchange until the binary key is greater or equal to 256 bits.
while len("".join(sharedBinKey)) < 256:
    #Create a random Y and P
    ourY = random.randint(2, 99999)
    ourP = random.randint(3, 99999)
    myX = random.randint(2, 999)
    hisX = random.randint(2, 999)

    #Make sure Y is < P
    while ourY >= ourP:
        ourY = random.randint(2, 99999)

    print("Shared Y: " + str(ourY))
    print("Shared P: " + str(ourP))
    print("My X: " + str(myX) + " (Private)")
    print("His X: " + str(hisX) + " (Private)")

    print("\nY to the X mod P || (Y ** X) % P")
    myAns = (ourY ** myX) % ourP
    print("My answer: " + str(myAns))

    hisAns = (ourY ** hisX) % ourP
    print("His answer: " + str(hisAns))

    print("\nHis answer raised to my X mod P")
    myKey = (hisAns ** myX) % ourP
    myKeyBin = list(bin(myKey))
    del myKeyBin[0:2]
    print("My key: decimal/ " + str(myKey) + " binary/ " + "".join(myKeyBin))

    print("\nMy answer raised to his X mod P")
    hisKey = (myAns ** hisX) % ourP
    hisKeyBin = list(bin(hisKey))
    del hisKeyBin[0:2]
    print("His key: decimal/ " + str(hisKey) + " binary/ " + "".join(hisKeyBin))
    print("\nThe key is: " + "".join(myKeyBin))
    print("The length of the key is: " + str(len("".join(myKeyBin))) + " bits.\n")

    #If the keys match, append to list for concatenation.
    if "".join(hisKeyBin) == "".join(myKeyBin):
        sharedBinKey.append("".join(myKeyBin))
        sharedDecKey.append(myKey)
    else:
        print("Error. Keys are not equal.") #This should, in theory, never occur.
        exit(1)

#Clear the screen from the previous data
os.system("clear")
#Let's print out some admin data to see what we're working with here.
#Decimal key data
sharedDecKey = int("".join(map(str,sharedDecKey)))
lengthOfDecKey = str(len(str(sharedDecKey)))
strDecKey = str(sharedDecKey)
print("The length of the decimal key is: " + lengthOfDecKey)
print("The decimal key is: " + str(sharedDecKey))

#Binary key data
lengthOfBinKey = str(len("".join(sharedBinKey)))
strBinKey = "".join(sharedBinKey)
listBinKey = list(strBinKey)
print("\nThe length of the binary key is: " + lengthOfBinKey)
print("The binary key is: " + strBinKey)

#Let's work on removing excess bits if needed.
if len(strBinKey) > 256:
    print("There are too many bits in the key.")
    del listBinKey[256 - int(len(strBinKey)) - 1:-1]
    print("\nThe binary key now has " + str(len(listBinKey)) + " bits.")
    print(str("".join(listBinKey)))
elif len(strBinKey) == 256:
    print("\nThe binary key already has 256 bits.")
else:
    print("Serious fucking error.")
    exit(1)

###################################################################################################################
#Let's try to encipher some text. It's about the get dirty.
print("\n****************************\nGetting into encryption now.")
#Here's a test string to mess around with.
plainTextMessage = list("Here isastextsesntencelestuss kil ass")
plainTextBin = list()

#Loop that loads a list with the binary values of the plain text message.
for q in plainTextMessage:
    plainTextBin.append(bin(ord(q)))

#Loop that removes the '0b' from the front of every binary value in the list.
#WARNING, this shit is about to get dirty, like really dirty....
for h in range(len(plainTextBin)):
    holder = list(plainTextBin[h]) #A temporary place holder for each binary value in the plain text binary var.
    del holder[0:2] #Delete the '0b'
    del plainTextBin[h] #Remove the original '0b' containing value.
    plainTextBin.insert(h, "".join(holder)) #Replace with the new non-'0b' value.

print("\nThe test sentence in binary list is: " + str(plainTextBin))
print("\nThe plain text binary value is: " + "".join(plainTextBin))
print("The length of the plain text binary value is: " + str(len("".join(plainTextBin))) + " bits.")

#Encrypt the plain text to cipher text.

#Convert plaintext to decimal integer value.
plainTextBin = "".join(plainTextBin)
plainTextBin = int(plainTextBin, 2)
print("\nThe plain text message in decimal format is: " + str(plainTextBin))

#Convert key to decimal integer value.
listBinKey = "".join(listBinKey)
int256DecKey = int(listBinKey, 2)
print("The 256 bit key back in decimal format is: " + str(int256DecKey))

#XOR of plaintext message and key.
cipherBin = bin(plainTextBin ^ int256DecKey)
print("\nThe ciphertext binary value is: " + str(cipherBin))
print("The length of the ciphertext binary value is: " + str(len(cipherBin) - 2))

#Strip the '0b' off the front.
if len(cipherBin) - 2 < 256:
    print("\nStrip the '0b' and pad the left with zeros.")
    cipherBin = list(cipherBin)
    del cipherBin[0:2]
    # Add '0' padding to left of ciphertext binary if needed
    for x in range(256 - len(cipherBin)):
        cipherBin.insert(x, '0')
    print("".join(cipherBin))
else:
    print("This isn't normal")
    exit(1)

#Make a list out of the 256 bit ciphertext
cipherBin = list(cipherBin)
#Combine 8 bit values for char conversion later.
cipherByte = []
p = 0
q = 8
for g in range(32):
    cipherByte.insert(g, "".join(cipherBin[p:q]))
    p += 8
    q += 8
print("\nSplit the string into 8 bit values.\n" + str(cipherByte))

#Convert to chars
listCipherASCII = list()
for g in range(len(cipherByte)):
    listCipherASCII.insert(g, chr(int(cipherByte[g], 2))) #Not sure if chr() converts to ASCII or unicode...
print("\nThe encrypted data is: " + str("".join(listCipherASCII)))
print("\t\t\t\t\t\t\t\t\t\u2191")
print("\t\t\t\t\tThat's a decent start to encryption")

exit(0)
