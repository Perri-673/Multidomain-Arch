import os

def to_head( projectpath ):
    pathlayers = os.path.join( projectpath, 'layers/' ).replace('\\', '/')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone} 
\usepackage{import}
\subimport{"""+ pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} %for including external image 
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

# layers definition

def to_input( pathfile, to='(-3,0,0)', width=8, height=8, name="temp" ):
    return r"""
\node[canvas is zy plane at x=0] (""" + name + """) at """+ to +""" {\includegraphics[width="""+ str(width)+"cm"+""",height="""+ str(height)+"cm"+"""]{"""+ pathfile +"""}};
"""

# Conv
def to_Conv( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """ 
    {Box={
        name=""" + name +""",
        caption=""" + caption +r""",
        xlabel={{""" + str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# Conv,Conv,relu - Bottleneck Layer
def to_ConvConvRelu( name, s_filer=256, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={ """+ offset +""" }] at """ + to + """ 
    {RightBandedBox={
        name=""" + name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(n_filer[0]) +""", """+ str(n_filer[1]) +""" }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""

# Activation Layer (ReLU) to separate Conv layers
def to_Activation( name, offset="(0,0,0)", to="(0,0,0)", caption="ReLU" ):
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """ 
    {Box={
        name=""" + name +""",
        caption=""" + caption +r""",
        fill=\ConvReluColor,
        height=20,
        width=1,
        depth=1
        }
    };
"""

# Pool
def to_Pool(name, offset="(0,0,0)", to="(0,0,0)", height=40, depth=40, width=1):
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """ 
    {Box={
        name=""" + name +""",
        caption="POOL",
        fill=\PoolColor,
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""

# Self-Attention Block
def to_SelfAttention(name, offset="(0,0,0)", to="(0,0,0)", width=2, height=2, depth=2):
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """ 
    {Box={
        name=""" + name +""",
        caption="Self-Attention",
        fill={rgb:blue,3;green,3;red,1},
        height=""" + str(height) + """,
        width=""" + str(width) + """,
        depth=""" + str(depth) + """
        }
    };
"""

def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""

# Architecture Code
def generate_architecture():
    arch = [
        to_head( '..' ),
        to_cor(),
        to_begin(),
        to_Conv("from_rgb", 3, 64, offset="(0,0,0)", to="(0,0,0)", height=64, depth=64, width=2 ),
        to_Activation("activation1", offset="(0,0,0)", to="(from_rgb-east)", caption="ReLU"),
        
        to_ConvConvRelu("encode1", s_filer=64, n_filer=(64,128), offset="(1,0,0)", to="(activation1-east)", width=(2,2), height=32, depth=32, caption="Encode Layer 1"),
        to_Activation("activation2", offset="(0,0,0)", to="(encode1-east)", caption="ReLU"),
        
        to_ConvConvRelu("encode2", s_filer=128, n_filer=(128,256), offset="(1,0,0)", to="(activation2-east)", width=(2,2), height=16, depth=16, caption="Encode Layer 2"),
        to_Activation("activation3", offset="(0,0,0)", to="(encode2-east)", caption="ReLU"),
        
        to_ConvConvRelu("encode3", s_filer=256, n_filer=(256,512), offset="(1,0,0)", to="(activation3-east)", width=(2,2), height=8, depth=8, caption="Encode Layer 3"),
        
        to_SelfAttention("self_attention", offset="(1.5,0,0)", to="(encode3-east)", width=2, height=2, depth=2),

        to_ConvConvRelu("decode1", s_filer=512, n_filer=(512,256), offset="(2,0,0)", to="(self_attention-east)", width=(2,2), height=8, depth=8, caption="Decode Layer 1"),
        to_Activation("activation4", offset="(0,0,0)", to="(decode1-east)", caption="ReLU"),
        
        to_ConvConvRelu("decode2", s_filer=256, n_filer=(256,128), offset="(2,0,0)", to="(activation4-east)", width=(2,2), height=16, depth=16, caption="Decode Layer 2"),
        to_Activation("activation5", offset="(0,0,0)", to="(decode2-east)", caption="ReLU"),
        
        to_ConvConvRelu("decode3", s_filer=128, n_filer=(128,64), offset="(2,0,0)", to="(activation5-east)", width=(2,2), height=32, depth=32, caption="Decode Layer 3"),
        
        to_Conv("to_rgb", 64, 3, offset="(2,0,0)", to="(decode3-east)", height=64, depth=64, width=2),
        to_end()
    ]

    namefile = 'generator_architecture'
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    generate_architecture()
