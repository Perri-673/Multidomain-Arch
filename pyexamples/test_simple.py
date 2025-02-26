import sys
sys.path.append('../')
from pycore.tikzeng import *

# Define the architecture
arch = [
    to_head('..'),
    to_cor(),
    to_begin(),
    
    # Input RGB Layer
    to_Conv("from_rgb", 256, 64, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=2, caption="from_rgb"),
    
    # Encoding Blocks (Downsampling)
    to_Conv("resblk1", 64, 128, offset="(1,0,0)", to="(from_rgb-east)", height=48, depth=48, width=3, color="\ResBlkColor", caption="ResBlk1"),
    to_connection("from_rgb", "resblk1"),
    
    to_Conv("resblk2", 128, 256, offset="(1.5,0,0)", to="(resblk1-east)", height=32, depth=32, width=4, color="\ResBlkColor", caption="ResBlk2"),
    to_connection("resblk1", "resblk2"),
    
    # Decoding Blocks (Upsampling)
    to_Conv("adain1", 256, 128, offset="(2,0,0)", to="(resblk2-east)", height=48, depth=48, width=3, color="\FcColor", caption="AdainResBlk1"),
    to_connection("resblk2", "adain1"),
    
    to_Conv("adain2", 128, 64, offset="(2.5,0,0)", to="(adain1-east)", height=64, depth=64, width=2, color="\FcColor", caption="AdainResBlk2"),
    to_connection("adain1", "adain2"),
    
    # Output RGB Layer
    to_Conv("to_rgb", 256, 3, offset="(3,0,0)", to="(adain2-east)", height=64, depth=64, width=2, caption="to_rgb"),
    to_connection("adain2", "to_rgb"),
    
    to_end()
]

# Generate TikZ file
def main():
    with open("test_simple.tex", "w") as f:
        f.write("\n".join(arch))

if __name__ == "__main__":
    main()
