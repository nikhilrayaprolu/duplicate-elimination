from SqlException import SqlException

import sys
import btree
import hash


def printmessage(message):
    # print message
    pass


def main():
    try:
        if len(sys.argv) < 6:
            raise SqlException("Usage: python main.py filename numAttributes~3 numBuffers~10 blockSize~144 typeOfIndex")
            printmessage("raised sql error")
        elif sys.argv[4] == 0 or sys.argv[5] == "btree":
            btree.distinct(sys.argv[1:-1])
            printmessage("btree selected")
        elif sys.argv[4] == 1 or sys.argv[5] == "hash":
            hash.distinct(sys.argv[1:-1])
            printmessage("btee selected")
    except SqlException, e:
        print e.message


if __name__ == '__main__':
    main()
