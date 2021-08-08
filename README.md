Created to check STACK when reversing, system hacking, etc..
This Program Create Imaginary STACK Container.
And you can push, pop, pop to variable from stack, and print stack/popped variable.

ps. I will update this code to support functions like set(set stack(insert)/variable), print by esp(rsp), etc..

***SUMMERY***
What can I do? (ISTACK := Imaginary STACK)
1. push data to ISTACK
2. pop data from ISTACK
3. pop data from ISTACK to variable
4. print ISTACK
5. print VARIABLE(s)

***DETAIL(commands)***
* {name} is where you can put string.
* { #name } is where you can put string or omit
eg. push {data} {#length} 
=> push testdata 12
=> push testdata

Push data to ISTACK
push {data} {#length} // length must be number.

Pop data from ISTACK
pop

Pop data from ISTACK to variable
pop {variable_name}
* you can't use {#num}:{#num} as {variable_name}
* you can't use 'all' as {variable_name}

Print ISTACK
print {# #num1:#num2} // most like python's list slicing
eg. print
eg. print 1:2
eg. print :2
eg. print 2:
eg. print :

Print VARIABLE(s)
print all //print all variables you set
print {varialbe_name} // print variable which name is {variable_name}
