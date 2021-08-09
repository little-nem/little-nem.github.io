points = [[0.5, 0., 1.4], [0.9, 0., 2.4], [1.2,0.,0.2], [3.1,0.,2.2],
          [6., 0., 4.1], [7.2, 0., 4.4], [9.,0., 7.6]]
colors = ['blue', 'darkblue', 'red', 'green', 'palegreen', 'yellow', 'blue']
weights = [1., 0.2, 0.4, 0.9, 1.2, 0.4, 0.5]

print("\\begin{scope}[canvas is xz plane at y = 0]")
for p, c in zip(points, colors):
    print("\t\\draw[fill={}] ({:03.1f},{:03.1f}) circle (0.2);".format(c, p[0], p[2]))    
print("\\end{scope}")

for p,c,w in zip(points, colors, weights):
    print("\\coordinate ({}) at ({:03.1f}, {:03.1f},{:03.1f});".format(c, p[0], p[1], p[2]))
    print("\\draw[ultra thick, {}] ({:03.1f}, {:03.1f},{:03.1f}) -- ({:03.1f}, {:03.1f},{:03.1f});".format(c, p[0],p[1],p[2],p[0],p[1]+w,p[2]))
