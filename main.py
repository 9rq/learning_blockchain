from BlockChain import *
if __name__ == '__main__':
    bc = BlockChain(INITIAL_BITS)
    print('generating genesis block ...')
    bc.create_genesis()
    for i in range(30):
        print('generating {}th block ...'.format(i+2)) # genesis + 1-origin
        bc.add_new_block(i)
