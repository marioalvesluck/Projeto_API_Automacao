import time
#
from_p= "01/10/2019 00:00:00"
to_futuro= "23/10/2019 21:59:59"
#to_futuro= "18/10/2019 21:47:00"

# passado 1569899400.000000
# Futuro 1570935540.000000

help(time.gmtime(761100))
print("{0.tm_mday}".format(time.gmtime(761100)))

# print()
#
#passado_timestamp = time.mktime(time.strptime(from_p, "%d/%m/%Y %H:%M:%S"))
#futuro_timestamp = time.mktime(time.strptime(to_futuro, "%d/%m/%Y %H:%M:%S"))
#Incidente = time.strftime("%Hd %Mh %Sm", time.localtime(16531))

passado_timestamp = time.mktime(time.strptime(from_p, "%d/%m/%Y %H:%M:%S"))
futuro_timestamp = time.mktime(time.strptime(to_futuro, "%d/%m/%Y %H:%M:%S"))

#agora = 1569898800
#to = 1571835288
#ok = 1711469
#problemTime = 225019

##print(time.strftime("%Hd %Mh %Sm", time.localtime(a)))
#print(a)
#print(int(time.strftime("%A %d/%m/%Y %H:%M:%S", time.localtime(a))))
#resultado = (int(agora + to + ok))
#print(int(resultado - problemTime))
#print(resultado)
#print(time.strftime("%Hd %Mh %Sm", time.localtime(resultado)))
#print(time.strftime("%A %d/%m/%Y %H:%M:%S", time.localtime(resultado)))



#
#
# print("from {}".format(passado_timestamp))
# print("to {}".format(futuro_timestamp))
# print(time.strftime("%d/%m/%Y %H:%M:%S",time.localtime(761100)))
# print(time.strftime("%A %d/%m/%Y %H:%M:%S", time.localtime(passado_timestamp)))
# print(time.strftime("%A %d/%m/%Y %H:%M:%S", time.localtime(futuro_timestamp)))

#print(time.strftime("%A %d/%m/%Y %H:%M:%S", time.localtime(16531)))
#print(time.strftime("%Hd %Mh %Sm", time.localtime(16531)))

# print(time.strftime("%H:%M:%S", time.localtime(39351)))
# print(time.strftime("%H:%M:%S", time.localtime(16531)))


# 01/10/2019 00:00:00
# 08/10/2019 23:00:00

