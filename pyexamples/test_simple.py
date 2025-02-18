import os
import sys
sys.path.append('../')
from pycore.tikzeng import *

def to_head(projectpath):
    pathlayers = os.path.join(projectpath, 'layers/').replace('\\', '/')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone} 
\usepackage{import}
\subimport{""" + pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} % for including external image 
"""

def to_cor():
    return r"""
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:magenta,5;black,7}   
\def\SumColor{rgb:blue,5;green,15}
"""

def to_begin():
    return r"""
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
"""

def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""

def to_Conv(name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "):
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """ 
    {Box={
        name=""" + name + """,
        caption=""" + caption + r""",
        xlabel={{""" + str(n_filer) + """, }},
        zlabel=""" + str(s_filer) + """,
        fill=\ConvColor,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""

def to_ResBlk(name, dim_in, dim_out, offset="(0,0,0)", to="(0,0,0)", caption=" "):
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """ 
    {Box={
        name=""" + name + """,
        caption=""" + caption + r""",
        xlabel={{""" + str(dim_in) + """, }},
        zlabel=""" + str(dim_out) + """,
        fill=\ConvColor,
        height=40,
        width=1,
        depth=40
        }
    };
"""

# Define blocks for the Generator network
def generate_architecture():
    arch = [
        to_head('..'),
        to_cor(),
        to_begin(),
        to_Conv("conv1", 512, 64, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=2),
        to_ResBlk("resblk1", 64, 128, offset="(1,0,0)", to="(conv1-east)", caption="ResBlk1"),
        to_ResBlk("resblk2", 128, 256, offset="(2,0,0)", to="(resblk1-east)", caption="ResBlk2"),
        to_ResBlk("resblk3", 256, 512, offset="(3,0,0)", to="(resblk2-east)", caption="ResBlk3"),
        to_ResBlk("resblk4", 512, 512, offset="(4,0,0)", to="(resblk3-east)", caption="ResBlk4"),
        to_ResBlk("resblk5", 512, 512, offset="(5,0,0)", to="(resblk4-east)", caption="ResBlk5"),
        to_ResBlk("resblk6", 512, 512, offset="(6,0,0)", to="(resblk5-east)", caption="ResBlk6"),
        to_ResBlk("resblk7", 512, 512, offset="(7,0,0)", to="(resblk6-east)", caption="ResBlk7"),
        to_ResBlk("resblk8", 512, 512, offset="(8,0,0)", to="(resblk7-east)", caption="ResBlk8"),
        to_end()
    ]
    return arch

def main():
    arch = generate_architecture()
    namefile = "generator_architecture"
    to_generate(arch, namefile + '.tex')

if __name__ == '__main__':
    main()
