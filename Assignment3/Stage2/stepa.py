import sys
import Stage2

if len(sys.argv) != 1:
    print("Invalid number of args")

sb=Stage2.stage2()
sb.stepa()
