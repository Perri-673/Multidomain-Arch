import sys
sys.path.append('../')
from pycore.tikzeng import *

# defined your arch
arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_Conv("from_rgb", 3, 64, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=2 ),
    
    # Encoding blocks (ResBlk down-sampling)
    to_Conv("encode1", 64, 128, offset="(1,0,0)", to="(from_rgb-east)", height=32, depth=32, width=2),
    to_Conv("encode2", 128, 256, offset="(1,0,0)", to="(encode1-east)", height=16, depth=16, width=2),
    to_Conv("encode3", 256, 512, offset="(1,0,0)", to="(encode2-east)", height=8, depth=8, width=2),

    # Self-attention block
    to_Box("self_attention", width=2, height=2, depth=2, offset="(2,0,0)", to="(encode3-east)", opacity=0.5, caption="Self-Attention"),

    # Decoding blocks (ResBlk up-sampling)
    to_Conv("decode1", 512, 256, offset="(3,0,0)", to="(self_attention-east)", height=8, depth=8, width=2),
    to_Conv("decode2", 256, 128, offset="(3,0,0)", to="(decode1-east)", height=16, depth=16, width=2),
    to_Conv("decode3", 128, 64, offset="(3,0,0)", to="(decode2-east)", height=32, depth=32, width=2),

    # Output layer (to_rgb)
    to_Conv("to_rgb", 64, 3, offset="(3,0,0)", to="(decode3-east)", height=64, depth=64, width=2),
    to_end()
]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
