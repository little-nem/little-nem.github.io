# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import networkx as nx
import network2tikz as n2t
import numpy as np
import matplotlib.pyplot as plt

# +
# my colors

blue = 255 * np.array([0.38, 0.51,0.71])
darkblue = [17,42,60]
red = [175,49,39]
orange=[217, 156, 55] 
green=[144, 169, 84] 
palegreen=[197, 184, 104] 
yellow=[250, 199, 100] 
brokenwhite=[218, 192, 166] 
brokengrey = 255 * np.array([0.77, 0.76, 0.82])


# +
# from https://bsou.io/posts/color-gradients-with-python
def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def color_dict(gradient):
    ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
    return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [int(s[j] + (float(t)/(n-1))*(f[j]-s[j])) for j in range(3)]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return color_dict(RGB_list)



# -

def s(t):
    coeffs = [0.5, 0.25, 0.1, 0.2]
    pulses = [5., 9., 10, 20.]
    phases = [100., 100., 10, 0]
    print("\t\\addplot[color=darkblue, ultra thin] {"+"+".join(["{}*cos(deg({}*x + {}))".format(c,w,p) for c,w,p in zip(coeffs,pulses,phases)]) + "};")
    return sum([c*np.cos(w*t+phi) for c,w,phi in zip(coeffs,pulses,phases)])


plt.plot(s(np.linspace(0,2,100)))

X = np.linspace(0.1,2,25)

# +
print("\\begin{axis} [domain=0:2.1,samples=200,no markers,hide y axis,xtick=\empty,axis lines=middle,xlabel=$t$,]")

low = yellow
high = red
bins_nb = 30
Y = s(X)
eps = 1e-6
bins = np.linspace(Y.min()-eps,Y.max()+eps,bins_nb-1)
colors = np.array([hex_to_RGB(linear_gradient(RGB_to_hex(low), RGB_to_hex(high), bins_nb)['hex'][i]) for i in range(bins_nb)])
colors_tuples = [(c[0],c[1], c[2]) for c in colors[np.digitize(Y,bins)]]


for i,(x,y, col) in enumerate(zip(X,Y, colors_tuples)):
    #print("{}: {},{}".format(i,x,y))
    print("\t\\coordinate (p{}) at ({:.2f},{:.2f});".format(i,x,y))
    print("\t\\coordinate (p{}_orig) at ({:.2f},{:.2f});".format(i,x,0.0))
    print("\t\\draw[dotted, thin] (p{}) -- (p{}_orig);".format(i,i)) 
    print("\t\definecolor{{tempcolor_line_graph_{}}}{{RGB}}{{ {}, {}, {} }};".format(i, *col))
    print("\t\\node[ultra thick, color=tempcolor_line_graph_{}] at (p{}) {{$\\bullet$}};".format(i,i))
    
print("\\end{axis}")
# -

# now print the corresponding line graph
import networkx as nx

n = X.shape[0]
G = nx.path_graph(25)

nx.draw_spring(G)

visual_style = {}
visual_style['vertex_color'] = colors_tuples
visual_style['vertex_size'] = 0.2
visual_style['edge_curved'] = 0.1

# +
layout = nx.spectral_layout(G)
#layout = {i:np.array([2*i, 0]) for i in range(n)}
#layout

n2t.plot(G, "test.tex", standalone=False, layout=layout, **visual_style)
# -

for i,c in enumerate(colors_tuples):
    print("\\Vertex[x={:.2f},y=0.,size=0.2,color={{{},{},{}}},RGB]{{{}}}".format(0.7+i/1.95,*c,i))
for i,c in enumerate(colors_tuples[:-1]):
    print("\\Edge[lw=0.5,Direct]({})({})".format(i, i+1))


