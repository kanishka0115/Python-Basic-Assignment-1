
fruits=("apple","bannana","cherry")
print("1st way:")
fruits=fruits[:1]+("bannana",)+fruits[1:]
print(fruits)
print("2nd way:")
tup=(0,[1,2,3])
tup[1][0]=5
print(tup[1][0:])