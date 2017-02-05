# -*- coding: utf-8 -*-

from Cp949ToUniTable import uni_conv_table
import sys
import os.path

is_p3 = sys.hexversion >= 0x03000000


def getch_uni_wide(byteH, byteL):
	ch = uni_conv_table[(byteH << 8) | byteL]

	if is_p3:
		return chr(ch)
	else:
		return unichr(ch)


def getch_uni(byteL):
	if is_dbcs_lead(byteL):
		raise ValueError

	ch = uni_conv_table[byteL]

	if is_p3:
		return chr(ch)
	else:
		return unichr(ch)


def is_dbcs_lead(byteL):
	c = uni_conv_table[byteL]
	if c == "LEAD":
		return True
	else:
		return False


if not is_p3:
    reload(sys)
    sys.setdefaultencoding('utf8')

if len(sys.argv) != 3:
	print("Usage: python Cp949_to_UTF8.py source_file target_file")
	print("사용법: python Cp949_to_UTF8.py 입력_파일 출력_파일")
	sys.exit()

if os.path.exists(sys.argv[2]):
	print("Target file already exists.")
	print("출력 파일이 이미 존재합니다.")
	sys.exit()

byte_high = 0x00
is_wide = False

out_file = open(sys.argv[2], "a")

with open(sys.argv[1], "rb") as f:
    byte = f.read(1)
    while byte != "":
        byte = f.read(1)

        if len(byte) == 0:
        	break

        ord_byte = ord(byte)

        if is_dbcs_lead(ord_byte):
        	byte_low = ord(f.read(1))
        	out_file.write(getch_uni_wide(ord_byte, byte_low))
        else:
        	out_file.write(getch_uni(ord_byte))

out_file.close()
